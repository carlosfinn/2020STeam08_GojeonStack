## 필요한 패키지를 import합니다. 가급적 건드리지 마시기 바랍니다. 
from flask import Flask, request, make_response, flash, redirect, Response
from flask_cors import CORS
import requests, json, os
import random, string, time, uuid, subprocess
import api, auth, heat, glance, lecture, swift


## random_string을 생성합니다. 
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


## api서버를 구동하기 위한 기본설정을 수행합니다. 
app = Flask(__name__)
UPLOAD_FOLDER = '../imageBuffer'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'x9@Q!2vC8o*'


## chrome 등등의 대다수의 브라우저들은 CORS라는 출처동일의 원칙을 적용하므로 이에 대한 사전설정을 수행해야합니다. 
## 각 api의 url별로 CORS를 설정하는 것입니다. 
cors = CORS(
    app, resources={
        r"/*": {"origin": "*"},
        r"/auth/*": {"origin": "*"},
        r"/auth/login/*": {"origin": "*"},
        r"/auth/register/*": {"origin": "*"},
        r"/auth/password/*": {"origin": "*"},
        r"/api/*": {"origin": "*"},
        r"/api/vm/*": {"origin": "*"},
        r"/api/stack/*": {"origin": "*"},
        r"/api/image/*": {"origin": "*"},
        r"/api/board/*": {"origin": "*"}
    }
)

## 로그인을 수행하고 dashboard (web)에서 그 결과를 통해 다음 화면으로 넘겨줄 수 있도록 한다. 
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    id = data['id']
    pw = data['pw']
    
    scopedToken, userId = auth.getScopedToken(id, pw, 'admin')
    projectId = auth.getAdminProjectId(scopedToken)

    if id == 'admin':
        jsonResult = {
            'token': scopedToken,
            'role': 'Teacher',
            'tenant_id': projectId,
            'student_id': id,
            'loginResult': True            
        }

    else:
        role = auth.listUsers(scopedToken, userId)
        jsonResult = {
            'token': scopedToken,
            'role': role,
            'tenant_id': projectId,
            'student_id': id,
            'user_id': userId,
            'loginResult': True            
        }
    
    resJson = json.dumps(jsonResult)
    return resJson

## 학생, 선생님의 유형에 맞게 회원가입을 할 수 있습니다. 
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    role = data['role']
    name = data['name']
    pw = data['pw']
    email = data['email']
    

    scopedToken, userId = auth.getScopedToken('admin', '8nkujc3rf', 'admin')
    projectId = auth.getAdminProjectId(scopedToken)  #admin project
    role_id = auth.getUserRole(scopedToken, projectId, userId)  #admin role
    
    user, character = auth.createUser(scopedToken, projectId, name, pw, email, role)

    if user == 'Conflict':
        jsonResult = {
            'registerResult': False,
            'userID': user
        }
        resJson = json.dumps(jsonResult)
        return resJson

    auth.assignRoletoUser(scopedToken, projectId, user, role_id)
    jsonResult = {
        'registerResult': True,
        'name': name,
        'password': pw,
        'userID': user,
        'character': character
    }

    resJson = json.dumps(jsonResult)
    return resJson

## 사용자는 원할경우 언제나 패스워드를 변경할 수 있습니다. 
@app.route('/auth/password', methods=['GET', 'POST'])
def changePW():
    requestHeader = request.headers
    data = request.get_json()

    token = requestHeader.get('X-Auth-Token', None)
    pw = data['pw']
    newPW = data['newPW']
    user_id = data['user_id']
    # token = 'gAAAAABfaikq4qrtcE8hYQRev_MVXz5_6UicTX3XtAVtwRq2IUGwsRtP3FIU8UNHLNMpKVlp7-ILyR24AGeI1teJlarsJqamy4r9KK1Cjs4arQP4YpDDX0dDEzch1l-3e4kBkMvr66W_d-BrNkP6UsWpkr-a_-NlWVub-M-vnu7lnJosd0zl49g'
    # pw = 'newtest5'
    # newPW = 'newtest6'
    # user_id = 'f2d68408d18942f2847c1d074a09dedb'

    result = auth.changePassword(token, user_id, pw, newPW)
    print(result)
    if result == 'Complete':
        jsonResult = {
            'passwordChanged': True,
            'newPW': newPW
        }

    if result == 'Conflict':
        jsonResult = {
            'passwordChanged': False,
            'message': 'conflict'
        }

    
    resJson = json.dumps(jsonResult)
    return resJson
    
## 강의를 생성합니다. 
## 입력받는 내용 : 가상머신에 사용하는 이미지, vcpu의 수, ram 용량, disk의 용량, 강의 이름, 접속하는 학생들의 수, 코딩에 사용하는 언어, 강의를 생성하는 강사의 id
@app.route('/api/stack/create', methods=['POST'])
def createStack():
    requestHeader = request.headers
    requestBody = json.loads(request.get_data())
    print(requestBody)

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    image = requestBody.get("image", None)
    vcpus = requestBody.get("vcpus", 1)
    ram = requestBody.get("ram", 2048)
    disk = requestBody.get("disk", 24)
    stack_name = requestBody.get("stack_name", get_random_string(16))
    personeel = requestBody.get("personeel", 0)
    language = requestBody.get("language", '')
    creator_id = requestBody.get("creator_id", '')

    result = heat.createInstance(X_AUTH_TOKEN, tenant_id, stack_name, image, vcpus, ram, disk, int(personeel), language, creator_id)
    print(X_AUTH_TOKEN, tenant_id, stack_name, image, vcpus, ram, disk)
    return json.dumps(result)

## 강의(stack)에 대한 정보를 추출합니다. 이 때 정보란 강의에 대한 데이터베이스 정보가 아니라, Openstack 내에서의 자원의 단위인 stack으로써의 강의를 말합니다. 
@app.route('/api/stack/details', methods=['GET'])
def getStackDetails():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)

    result = heat.getStackStatus(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    print(result)

    return json.dumps(result)

## 강의(stack)의 목록을 부릅니다. 
@app.route('/api/stack/list', methods=['GET'])
def listStack():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    result = heat.getStackList(X_AUTH_TOKEN, tenant_id)

    return json.dumps(result)

## 특정 강의를 삭제합니다. 
@app.route('/api/stack/delete', methods=['DELETE'])
def deleteStack():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    requestBody = json.loads(request.get_data())

    stack_name = requestBody.get("stack_name", None)
    stack_id = requestBody.get("stack_id", None)

    result = heat.deleteStack(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)

    return json.dumps(result)

### 여기는 이미지와 관련된 웹 api 부분입니다. 
## 선택한 이미지를 삭제합니다. 
@app.route('/api/image/delete', methods=['DELETE'])
def deleteImage():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    image_id = requestHeader.get("image_id", None)

    result = glance.deleteImage(X_AUTH_TOKEN, image_id)

    return json.dumps(result)


## 이미지의 목록을 확인합니다. 
@app.route('/api/image/list', methods=['GET'])
def listImage():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)

    result =glance.getImageList(X_AUTH_TOKEN)

    return json.dumps(result)

## 이미지의 목록을 dashboard(웹 인터페이스)의 템플릿에서 사용할 수 있는 형태로 변환하여 돌려줍니다. 
@app.route('/api/image/table', methods=['GET'])
def tableImage():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)

    result = glance.getImageList(X_AUTH_TOKEN)
    image_table = list()
    for image in result: 
        img_size = image.get("size", 0)
        if not img_size: img_size = 0
        image_info = [ image.get("name", ""), image.get("min_ram", 0), image.get("min_disk", 0), image.get("disk_format", ""), image.get("status", ""), img_size / (1024 *1024), image.get("id", "") ]
        image_table.append(image_info)

    return json.dumps(image_table)

## 이미지를 생성합니다. 기본 구조는 이미지를 첨부해서 올리면 서버로 해당 파일을 불러와 저장하는 것입니다. 
@app.route('/api/image/create', methods=['POST'])
def createImage():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    disk_format = requestHeader.get("disk_format", "RAW")
    min_disk = requestHeader.get("min_disk", 0)
    min_ram = requestHeader.get("min_ram", 0)
    name = requestHeader.get("name", get_random_string(16))

    uploadurl = glance.createImageInfo(X_AUTH_TOKEN, disk_format, int(min_disk), int(min_ram), name)

    filename = ''
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
        uploadfile = request.files['file']
        filename = uploadfile.filename
        # if user does not select file, browser also
        # submit an empty part without filename
        if uploadfile.filename == '':
            flash('No selected file')
        if uploadfile:
            uploadfile.save(os.path.join(app.config['UPLOAD_FOLDER'], uploadfile.filename))

    filedir = UPLOAD_FOLDER + '/' + filename
    command = "openstack image create --disk-format %s --min-disk %d --min-ram %d --file %s --public %s" % (disk_format, int(min_disk), int(min_ram), filedir, name)
    os.system(command)

    print(command)
    upload_command = '''curl -i -X PUT -H "X-Auth-Token: %s" -H "Content-Type: application/octet-stream" -d '%s' %s''' \
        % (X_AUTH_TOKEN, request.files['file'].read(), uploadurl)
    os.system(upload_command)
    os.system('rm '+filedir)
    
    return {}

## 강의를 위해 마련된 가상환경에 접속하기 위해서 콘솔을 생성합니다. 
@app.route('/api/stack/console', methods=['POST'])
def getInstanceConsole():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)
    tenant_id = requestHeader.get("tenant_id", None)

    instance_list = heat.getInstanceInfo(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    instance = instance_list[0]
    console_info = lecture.getInstanceConsole(X_AUTH_TOKEN, instance.get("physical_resource_id", None))

    return json.dumps(console_info)

## 특정 사용자의 id와 강의의 id를 받아 해당 강의에 대해 수강신청한 사실이 있는지 확인합니다. 
@app.route('/api/stack/enrollcheck', methods=['GET'])
def getEnrolledInformation():
    requestHeader = request.headers

    stack_id = requestHeader.get("stack_id", None)
    student_id = requestHeader.get("student_id", None)
    info = lecture.getEnrolledInfo(student_id, stack_id)

    return json.dumps({"enrolled": info != None})

## 강의에 등록되어있는 경우 바로 콘솔의 링크를 되돌려주고 없으면 수강등록처리하고 돌려줍니다. 
@app.route('/api/stack/owner', methods=['GET'])
def getOwner():
    requestHeader = request.headers
    stack_id = requestHeader.get("stack_id", None)

    owner = lecture.getOwner(stack_id)

    return json.dumps({'owner': owner})


## 강의에 등록되어있는 경우 바로 콘솔의 링크를 되돌려주고 없으면 수강등록처리하고 돌려줍니다. 
@app.route('/api/stack/enrollconsole', methods=['POST'])
def enroll():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)
    tenant_id = requestHeader.get("tenant_id", None)
    student_id = requestHeader.get("student_id", None)

    return json.dumps(lecture.enrollStudent(X_AUTH_TOKEN, tenant_id, stack_name, stack_id, student_id))

## 글의 내용을 우선적으로 등록합니다. 파일 첨부 관련 기능은 별도로 나눴습니다. 
## 글의 내용만 텍스트 파일로 저장하고, 첨부파일은 이름만 데이터베이스에 저장해둔 뒤 다음 단계에서 저장한다. 
@app.route('/api/board/thread', methods=['POST'])
def boardWrite():
    requestHeader = request.headers
    requestBody = json.loads(request.get_data())

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    student_id = requestHeader.get("student_id", None)
    tenant_id = requestHeader.get("tenant_id", None)

    filename = requestBody.get("filename", None)

    title = requestBody.get("title", None)
    content = requestBody.get("content", None)
    result = swift.uploadPost(X_AUTH_TOKEN, student_id, tenant_id, str(uuid.uuid4()), str(uuid.uuid4()), title, content, filename)
    print(result)
    return json.dumps(result)

## 게시물의 첨부파일을 저장합니다. 
## 이미지 첨부와 동일하게 flask서버를 이용하여 서버 컴퓨터로 파일을 받아온 뒤에 swift에 저장합니다. 
@app.route('/api/board/file', methods=['POST', 'GET'])
def uploadFile():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    student_id = requestHeader.get("student_id", None)
    tenant_id = requestHeader.get("tenant_id", None)
    filename = requestHeader.get("filename", None)
    foldername = requestHeader.get("foldername", None)
    if request.method == "GET": 
        X_AUTH_TOKEN = request.args.get("token")
        student_id = request.args.get("student_id")
        tenant_id = request.args.get("tenant_id")
        filename = request.args.get("filename")
        foldername = request.args.get("foldername")

    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        filename = file.filename
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        filedir = UPLOAD_FOLDER + '/' + filename
        fbuffer = open(filedir, 'rb')
        swift.uploadFile(X_AUTH_TOKEN, student_id, tenant_id, foldername, filename, fbuffer.read())
        fbuffer.close()
        os.system('rm '+filedir)
        return {}
    else: 
        print(filename)
        result = swift.fetchFile(X_AUTH_TOKEN, student_id, tenant_id, foldername, filename)
        return Response(result, headers={"Content-Disposition": "attachment; filename=%s" % (filename)}, content_type="application/octet-stream")

## 작성된 게시글 내용과 첨부파일을 불러옵니다. 데이터베이스를 통해 추출합니다. 
@app.route('/api/board/fetchpost', methods=['GET'])
def fetchPost():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    student_id = requestHeader.get("student_id", None)
    tenant_id = requestHeader.get("tenant_id", None)
    filename = requestHeader.get("filename", None)
    foldername = requestHeader.get("foldername", None)
    
    result = swift.fetchFile(X_AUTH_TOKEN, student_id, tenant_id, foldername, filename)
    print(result.text)

    return result.text

## 게시판에 작성되었던 글 목록을 전부 호출합니다. 
@app.route('/api/board/fetchall', methods=['GET'])
def fetchAll():
    results = swift.fetchPost()
    for result in results:
        result['written'] = result['written'].strftime("%Y-%m-%d %H:%M")
    return json.dumps(results)

## 글을 삭제합니다. 이 때 파일은 남겨두고 데이터베이스에서만 삭제합니다. 
@app.route('/api/board/delete', methods=['DELETE'])
def deletePost():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    student_id = requestHeader.get("student_id", None)
    tenant_id = requestHeader.get("tenant_id", None)
    foldername = requestHeader.get("foldername", None)
    post_id = requestHeader.get("post_id", None)

    swift.deletePost(X_AUTH_TOKEN, student_id, tenant_id, foldername, int(post_id))

    return ''

## 데이터베이스를 설치합니다. 반드시 한 번 이 api를 호출한 뒤에 실행하셔야합니다. 
@app.route('/dbinit', methods=['POST', 'GET'])
def dbinit():
    return json.dumps(api.startDB())

## 0.0.0.0은 위 api가 실행되는 IP 주소를 의미하며 0.0.0.0은 자신을 뜻하므로 현재 이 컴퓨터의 인터넷 IP주소를 의미합니다. 
## Port는 이 api를 접속할 때 쓰는 "문"의 번호라고 보면 되며 보통 <IP>:<PORT>의 양식으로 표시됩니다. 
## 예를 들어 IP 주소가 164.125.70.19인데 Port 번호가 16384이면 외부에서는 이 컴퓨터로 접속할 시 164.125.70.19:16384라고 호출하시면 됩니다. 
if __name__ == '__main__':
    app.run('0.0.0.0', port=16384)

