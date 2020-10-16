
import requests, json, pymysql
import heat

## 작성자 : 전민규
## 기능 : 수강신청에 관련된 api 기능
## 주로 openstack의 api 호출 보다 mysql과의 연동 관계가 큰 것 위주
## Openstack에서 자원들을 총괄하여 하나로 묶은 단위를 stack이라고 하는데,
## 본 시스템에서는 강의의 단위가 stack이므로 stack은 강의 하나를 뜻하게 됩니다. 

localhost = "http://164.125.70.19"


## getCurrnetStudent
## 기능 : 해당하는 강의의 현재 수강인원이 얼마인지 호출
## 관련 : mysql 데이터베이스
## 데이터베이스에 기록된 데이터를 조회하여 stack_id (강의 id)를 확인한다. 

def getCurrentStudent(stack_id: str) -> dict:
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''SELECT COUNT(*) as person FROM sign_up_list where lecture_id = '%s';''' % (stack_id)
    cursor.execute(query)

    result = cursor.fetchall()
    lecture_sign_up_list.close()
    return result[0]


## getInstanceConsole
## 입력 : 강의의 id가 아닌 강의를 위한 '가상머신'의 id를 제공해야함. 
## 기능 : 해당하는 강의를 접속하기 위한 콘솔을 생성
## 관련 : Openstack Nova
## 강의에 대한 GUI 접속을 허용하는 콘솔을 생성하고 이것의 링크를 통해 접속할 수 있다. 

def getInstanceConsole(X_AUTH_TOKEN: str, instance_id: str):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    rBody = {
        "os-getVNCConsole": {
            "type": "novnc"
        }
    }

    url = localhost + "/compute/v2.1/servers/" + instance_id + "/action"
    requestResult = requests.post(url, headers=rHeaders, data=json.dumps(rBody))
    requestResult.raise_for_status()
    console_info = requestResult.json()
    print("여기는 콘솔 정보입니다. ")
    print(console_info)

    url_info = console_info.get("console", {})
    url_split = url_info.get('url', '').split(':')
    port_info = url_split[-1]

    return {'url': localhost + ':' + port_info }

    
## getEnrolledCount
## 입력 : 특정 학생의 id와 강의의 id가 있어야함. 
## 기능 : 특정 학생의 강의에 등록된 횟수 확인
## 관련 : mysql 데이터베이스
## 어떠한 강의를 신청하고자 할 때 해당 학생이 등록되어있는지 여부를 그 횟수로 확인한다. 

def getEnrolledCount(student_id: str, stack_id: str):
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''SELECT COUNT(*) as person FROM sign_up_list where lecture_id = '%s' AND student_id = '%s';''' % (stack_id, student_id)
    cursor.execute(query)

    result = cursor.fetchall()
    lecture_sign_up_list.close()

    enroll_info = dict()
    if len(result) == 0: enroll_info = None
    else: enroll_info = result[0] 

    return enroll_info


## getEnrolledInfo
## 입력 : 특정 학생의 id와 강의의 id가 있어야함. 
## 기능 : 특정 학생의 강의에 등록 내역 확인
## 관련 : mysql 데이터베이스
## 어떠한 강의를 신청하고자 할 때 해당 학생이 등록된 내역을 반환한다. 이 때 위의 내용과 달리 강의의 정보, 학생의 ID 등의 정보를 반환한다. 

def getEnrolledInfo(student_id: str, stack_id: str):
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''SELECT * FROM sign_up_list where lecture_id = '%s' AND student_id = '%s';''' % (stack_id, student_id)
    cursor.execute(query)

    result = cursor.fetchall()
    lecture_sign_up_list.close()

    enroll_info = dict()
    if len(result) == 0: enroll_info = None
    else: enroll_info = result[0] 

    return enroll_info


## enrollStudent
## 기능 : 특정 학생의 강의 수강신청으로 인한 수강신청 정보를 추가한다. 
## 관련 : mysql 데이터베이스, mysql 데이터베이스
## 특정 학생이 강의의 수강신청 버튼을 누르면 수강등록이 되는데 이 때 sign_up_list라는 수강신청 정보를 저장하는 데이터베이스에 등록되고, 
## 강의의 가상머신의 id를 통하여 콘솔을 발급받는다. 
## 이미 수강신청이 등록되어있으면 데이터베이스의 등록과정 없이 바로 콘솔을 발급받는다. 

def enrollStudent(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, stack_id: str, student_id: str):
    lecture_resources = heat.getInstanceInfo(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    current_count = heat.getCurrentStudent(stack_id).get("person", 0)

    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    instance_id = str()

    if current_count == 0:
        first_instance = lecture_resources[0]
        instance_id = first_instance.get("physical_resource_id", "")
        query = '''insert into sign_up_list(lecture_id, student_id, lecture_order, vm_id) values('%s', '%s', %d, '%s')''' % (stack_id, student_id, current_count, instance_id)
        ## 강의 등록 시 강의의 id 뿐만 아니라 강의의 가상머신의 id도 같이 받아와서 접속용 콘솔의 링크 발급을 쉽게 한다. 
        cursor.execute(query)
    else:
        info = getEnrolledCount(student_id, stack_id)
        if info["person"] > 0: 
            instance_id = getEnrolledInfo(student_id, stack_id).get("vm_id", None)
        else:
            next_instance = lecture_resources[0]
            if current_count >= heat.getLecturePersoneel(stack_id): return ''
            instance_id = next_instance.get("physical_resource_id", None)
            query = '''insert into sign_up_list(lecture_id, student_id, lecture_order, vm_id) values('%s', '%s', %d, '%s')''' % (stack_id, student_id, current_count, instance_id)
            cursor.execute(query)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return getInstanceConsole(X_AUTH_TOKEN, instance_id) ## 수강신청이 등록이 이상없으면 자동으로 콘솔을 반환한다. 


def getOwner(stack_id: str) -> str:
    lecture_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_list.cursor(pymysql.cursors.DictCursor)
    query = "select creator_id from lectures where lecture_id='%s'" % (stack_id)
    cursor.execute(query)

    result = cursor.fetchall()
    first = result[0]

    return first.get("creator_id", None)