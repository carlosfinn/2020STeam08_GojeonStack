from flask import Flask, request, make_response, flash, redirect
from flask_cors import CORS
import json, os, api
import random, string, time

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

app = Flask(__name__)
UPLOAD_FOLDER = '../imageBuffer'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'x9@Q!2vC8o*'

cors = CORS(
    app, resources={
        r"/*": {"origin": "*"},
        r"/api/*": {"origin": "*"},
        r"/api/vm/*": {"origin": "*"},
        r"/api/stack/*": {"origin": "*"},
        r"/api/image/*": {"origin": "*"}
    }
)

@app.route('/api/flavors', methods=['GET'])
def getFlavor():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get('X-Auth-Token', None)

    result = api.getFlavors(X_AUTH_TOKEN)
    print(json.dumps(result))

    return json.dumps(result)

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

    result = api.createInstance(X_AUTH_TOKEN, tenant_id, stack_name, image, vcpus, ram, disk, int(personeel))
    print(X_AUTH_TOKEN, tenant_id, stack_name, image, vcpus, ram, disk)
    return json.dumps(result)

@app.route('/api/stack/details', methods=['GET'])
def getStackDetails():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)

    result = api.getStackStatus(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    print(result)

    return json.dumps(result)

@app.route('/api/stack/list', methods=['GET'])
def listStack():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    result = api.getStackList(X_AUTH_TOKEN, tenant_id)
    print(result)

    return json.dumps(result)

@app.route('/api/stack/delete', methods=['DELETE'])
def deleteStack():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    requestBody = json.loads(request.get_data())

    stack_name = requestBody.get("stack_name", None)
    stack_id = requestBody.get("stack_id", None)

    result = api.deleteStack(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)

    return json.dumps(result)

### image api start

@app.route('/api/image/delete', methods=['DELETE'])
def deleteImage():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    image_id = requestHeader.get("image_id", None)

    result = api.deleteImage(X_AUTH_TOKEN, image_id)

    return json.dumps(result)

@app.route('/api/image/list', methods=['GET'])
def listImage():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)

    result = api.getImageList(X_AUTH_TOKEN)
    image_table = list()

    for image in result: 
        image_info = [ image.get("name", ""), image.get("min_ram", 0), image.get("min_disk", 0), image.get("disk_format", ""), image.get("status", ""), image.get("id", "") ]
        image_table.append(image_info)

    return json.dumps(image_table)

@app.route('/api/image/create', methods=['POST'])
def createImage():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    disk_format = requestHeader.get("disk_format", "qcow2")
    min_disk = requestHeader.get("min_disk", 0)
    min_ram = requestHeader.get("min_ram", 0)
    name = requestHeader.get("name", get_random_string(16))

    filename = ''
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            filename = file.filename

    os.system('source ../../')
    create_command = '''openstack image create --disk-format %s --min-disk %d --min-ram %d --file %s --public %s''' % (disk_format, int(min_disk), int(min_ram), UPLOAD_FOLDER + '/' + filename, name)
    os.system(create_command)
    
    return {}

@app.route('/api/stack/console', methods=['POST'])
def getInstanceConsole():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)
    tenant_id = requestHeader.get("tenant_id", None)

    instance_list = api.getInstanceInfo(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    instance = instance_list[0]
    console_info = api.getInstanceConsole(X_AUTH_TOKEN, instance.get("physical_resource_id", None))

    return json.dumps(console_info)

@app.route('/api/stack/enrollcheck', methods=['GET'])
def getEnrolledInformation():
    requestHeader = request.headers

    stack_id = requestHeader.get("stack_id", None)
    student_id = requestHeader.get("student_id", None)
    info = api.getEnrolledInfo(student_id, stack_id)
    print("등록정보 확인 부분")
    print(info)

    return json.dumps({"enrolled": info != None})

@app.route('/api/stack/enrollconsole', methods=['POST'])
def enroll():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)
    tenant_id = requestHeader.get("tenant_id", None)
    student_id = requestHeader.get("student_id", None)

    return json.dumps(api.enrollStudent(X_AUTH_TOKEN, tenant_id, stack_name, stack_id, student_id))


if __name__ == '__main__':
    app.run('0.0.0.0', port=16384)

