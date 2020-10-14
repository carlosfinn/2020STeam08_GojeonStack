
import requests, json, pymysql
import heat

## 작성자 : 전민규
## 기능 : 수강신청에 관련된 api 기능
## 주로 openstack의 api 호출 보다 mysql과의 연동 관계가 큰 것 위주

localhost = "http://164.125.70.19"

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
        cursor.execute(query)
    else:
        info = getEnrolledCount(student_id, stack_id)
        if info["person"] > 0: 
            instance_id = getEnrolledInfo(student_id, stack_id).get("vm_id", None)
            print(instance_id)
        else:
            next_instance = lecture_resources[0]
            if current_count >= heat.getLecturePersoneel(stack_id): return ''
            instance_id = next_instance.get("physical_resource_id", None)
            query = '''insert into sign_up_list(lecture_id, student_id, lecture_order, vm_id) values('%s', '%s', %d, '%s')''' % (stack_id, student_id, current_count, instance_id)
            cursor.execute(query)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return getInstanceConsole(X_AUTH_TOKEN, instance_id)