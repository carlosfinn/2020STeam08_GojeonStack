
import requests, json, pymysql

## 작성자 : 전민규
## 기능 : 강의생성 및 관리, 강의삭제에 관련된 api 기능

localhost = "http://164.125.70.19"

def accountSettingCMD(personeel: int) -> str:
    result = ''
    for x in range(personeel):
        result += "  - useradd -m student%03d\n  - echo \"0000\\n0000\" | passwd student%03d\n  - echo \"0000\\n0000\"\n" % (x + 1, x + 1)
    return result


## 기능 : 강의생성을 시행합니다
## 필요한 정보 : 가상머신용 이미지, vcpus, RAM, disk의 용량, 수강하는 사람들의 수, 프로그램을 위한 언어

def createInstance(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, image: str, vcpus: int, ram: int, disk: int, personeel: int, language: str, creator_id: str):
    url = localhost + "/heat-api/v1/" + tenant_id + "/stacks"

    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    flavor_name = stack_name + "_flavor"
    volume_name = stack_name + "_volume"
    instance_name = stack_name + "_server"

    env_setting = ""
    initial_command = "#cloud-config\nruncmd: \n  - apt-get update\n  - apt-get upgrade\n"

    ## 프로그램 언어를 위한 세팅 작업, 필요 시 변경할 수 있습니다. 
    if language == "C/C++": env_setting = '''  - apt-get install gcc -y\n  - apt-get install g++ -y\n'''
    elif language == "Java": env_setting = '''  - apt-get install openjdk-11-jre-headless -y\n'''

    print(env_setting)
    rBody = {
        "stack_name": stack_name,
        "template": {
            "heat_template_version": "2015-04-30",
            "resources": {
                (flavor_name): {
                    "type": "OS::Nova::Flavor",
                    "properties": {
                        "ram": ram, "vcpus": vcpus, "disk": disk
                    }
                }, 
                (volume_name): {
                    "type": "OS::Cinder::Volume",
                    "properties": {
                        "size": disk, "image": image, "volume_type": "lvmdriver-1"
                    }
                }, (instance_name): {
                    "type": "OS::Nova::Server",
                    "properties": {
                        "flavor": { "get_resource": flavor_name },
                        "networks": [{"network": "public"}], "block_device_mapping": [{
                            "device_name": "vda",
                            "volume_id": { "get_resource": volume_name },
                            "delete_on_termination": False
                        }], 
                        "config_drive": True, "user_data_format": "RAW", 
                        "user_data": initial_command + env_setting + accountSettingCMD(personeel), 
                        "key_name": "babo"
                    }
                }
            }
        }
    }
    print("cmdrum dump :", initial_command + env_setting + accountSettingCMD(personeel))

    requestResult = requests.post(url, headers=rHeaders, data=json.dumps(rBody))
    requestResult.raise_for_status()
    stack_info = requestResult.json()
    stack = stack_info.get("stack", {})
    lecture_id = stack.get("id", "")

    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )
    
    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''insert into lectures(lecture_id, personeel, creator_id) values('%s', '%d', '%s')''' % (lecture_id, personeel, creator_id)
    cursor.execute(query)
    
    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return requestResult.json()



def getStackList(X_AUTH_TOKEN: str, tenant_id: str):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost + "/heat-api/v1/" + tenant_id + "/stacks"

    requestResult = requests.get(url, headers=rHeaders)
    requestResult.raise_for_status()

    resultJson = requestResult.json()
    stacks = resultJson.get("stacks", None)

    return stacks

def getStackStatus(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, stack_id: str):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost + "/heat-api/v1/" + tenant_id + "/stacks/" + stack_name + "/" + stack_id
    requestResult = requests.get(url, headers=rHeaders)
    stack_info = requestResult.json().get("stack", None)
    requestResult.raise_for_status()

    return stack_info

def deleteStack(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, stack_id: str):
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost + "/heat-api/v1/" + tenant_id + "/stacks/" + stack_name + "/" + stack_id
    requestResult = requests.delete(url, headers=rHeaders)
    requestResult.raise_for_status()

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    sql_query = '''delete from sign_up_list where lecture_id = '%s';''' % (stack_id)
    cursor.execute(sql_query)
    sql_query_02 = '''delete from lectures where lecture_id = '%s';''' % (stack_id)
    cursor.execute(sql_query_02)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()
    return { "result_code": requestResult.status_code }

def getStackResources(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, stack_id: str):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost + "/heat-api/v1/" + tenant_id + "/stacks/" + stack_name + "/" + stack_id + "/resources"
    requestResult = requests.get(url, headers=rHeaders)
    requestResult.raise_for_status()
    resources_info = requestResult.json()

    return resources_info.get("resources", [])

def getInstanceInfo(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, stack_id: str) -> list:
    resources = getStackResources(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    instance_list = list()

    for resource in resources:
        if resource.get("resource_type", "") == "OS::Nova::Server":
            instance_list.append(resource)
    
    return instance_list

def getLecturePersoneel(lecture_id: str) -> int:
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )
    
    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''SELECT personeel FROM lectures where lecture_id = '%s';''' % (lecture_id)
    cursor.execute(query)

    result = cursor.fetchall()
    print(result)
    lecture_sign_up_list.close()
    print(result)

    return result[0].get("personeel", 0)


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
