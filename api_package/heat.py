
import requests, json, pymysql

## 작성자 : 전민규
## 기능 : 강의생성 및 관리, 강의삭제에 관련된 api 기능

localhost = "http://164.125.70.19"

def accountSettingCMD(personeel: int) -> str:
    result = ''
    for x in range(personeel):
        result += "  - useradd -m student%03d\n  - echo \"0000\\n0000\" | passwd student%03d\n  - echo \"0000\\n0000\"\n" % (x + 1, x + 1)
    return result


## 작성자 : 전민규
## 기능 : 강의생성을 시행합니다
## 필요한 정보 : 가상머신용 이미지, vcpus, RAM, disk의 용량, 수강하는 사람들의 수, 프로그램을 위한 언어
## Openstack에서 자원들을 총괄하여 하나로 묶은 단위를 stack이라고 하는데,
## 본 시스템에서는 강의의 단위가 stack이므로 stack은 강의 하나를 뜻하게 됩니다. 
## HOT라는 기본양식으로 자원의 상세한 설정을 보내줄 수 있으며 이를 통해 자신이 원하는 설정에 따라 자원들의 유기체를 형성합니다. 

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
                        ##"key_name": "babo"
                    }
                }
            }
        }
    }

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


## 작성자 : 전민규
## 기능 : 강의의 목록을 불러옵니다. 
## stack으로 대표되는 강의의 목록을 전부 호출합니다. 

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


## 작성자 : 전민규
## 기능 : 강의용 환경의 생성상태를 확인합니다. 
## Stack으로 대표되는 강의를 생성하면 그 강의의 생성되는 상태를 확인할 수 있는데, 이를 통해 이상없이 생성되고 있는지 확인이 가능합니다. 

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


## 작성자 : 전민규
## 기능 : 강의를 삭제합니다. 
## 강의를 삭제합니다. 

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


## 작성자 : 전민규
## 기능 : 강의에 대한 컴퓨팅 자원의 목록을 찾아옵니다. 
## 강의의 경우 결국 가상머신을 통해 학생들이 접속할 수 있어야하는데 이를 위해 구성되는 기본자원들이 있습니다. 
## 그 자원들의 목록을 추출합니다. 

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


## 작성자 : 전민규
## 기능 : 강의에 대한 가상머신의 정보를 찾아옵니다. 
## 특정 강의에 대한 가상머신 (Instance)에 해당하는 자원의 정보만 추출합니다. 

def getInstanceInfo(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, stack_id: str) -> list:
    resources = getStackResources(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    instance_list = list()

    for resource in resources:
        if resource.get("resource_type", "") == "OS::Nova::Server":
            instance_list.append(resource)
    
    return instance_list


## 작성자 : 전민규
## 기능 : 강의의 정원을 확인합니다. 
## 강의 목록에 대한 정보를 Database를 통해 찾아와 해당 강의의 정원 정보를 찾아옵니다. 

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


## 작성자 : 전민규
## 기능 : 현재 해당 강의를 수강하고 있는 학생의 수를 확인합니다. 
## 어떠한 강의를 수강하고 있는 학생의 수를 데이터베이스 내의 수강현황을 통해 확인합니다. 

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
