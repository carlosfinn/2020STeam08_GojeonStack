import requests, json, pymysql

localhost = "http://164.125.70.19"


def accountSettingCMD(personeel: int) -> str:
    result = ''
    for x in range(personeel):
        result += "  - useradd -m student%03d\n  - echo \"0000\\n0000\" | passwd student%03d\n  - echo \"0000\\n0000\"\n" % (x + 1, x + 1)
    return result

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
                        "user_data": initial_command + env_setting + accountSettingCMD(personeel)
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

def startDB():
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        '''create table threads(id int(16) not null auto_increment primary key, title varchar(255) not null, content varchar(255) not null, filename varchar(255), foldername varchar(255) not null, student_id varchar(255) not null);'''
    )
    cursor.execute(
        '''create table sign_up_list (lecture_id varchar(255) not null, student_id varchar(255) not null, lecture_order int(16) unsigned not null, vm_id varchar(255) not null);'''
    )
    
    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return {}

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


## image 관련 부분

def getImageList(X_AUTH_TOKEN: str):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost + "/image/v2/images"
    requestResult = requests.get(url, headers=rHeaders)
    requestResult.raise_for_status()

    resultJson = requestResult.json()
    imageInfo = resultJson.get("images", [])

    return imageInfo

def createImageInfo(X_AUTH_TOKEN :str, disk_format: str, min_disk: str, min_ram: str, name: str):
    rHeaders = {
        "X-Auth-Token": X_AUTH_TOKEN
    }
    rBody = {
        "container_format": "bare",
        "disk_format": disk_format,
        "name": name, 
        "min_disk": min_disk, 
        "min_ram": min_ram
    }

    url = localhost + "/image/v2/images"
    requestResult = requests.post(url, headers=rHeaders, data=json.dumps(rBody))
    requestResult.raise_for_status()
    resultJson = requestResult.json()
    fileuploadurl = localhost + "/image" + resultJson.get('file', None)
    print(resultJson)

    return fileuploadurl

def deleteImage(X_AUTH_TOKEN: str, image_id):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost + '/image/v2/images/%s' % (image_id)
    requestResult = requests.delete(url, headers=rHeaders)
    requestResult.raise_for_status()

    return {}

def searchforImage(X_AUTH_TOKEN: str, name: str):
    imagelist = getImageList(X_AUTH_TOKEN)

    for image in imagelist:
        if image.get("name", '') == name: return image.get("id", '')


## stack_resource 및 instance의 정보 추출 관련 부분

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
    lecture_resources = getInstanceInfo(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    current_count = getCurrentStudent(stack_id).get("person", 0)

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
            if current_count >= getLecturePersoneel(stack_id): return ''
            instance_id = next_instance.get("physical_resource_id", None)
            query = '''insert into sign_up_list(lecture_id, student_id, lecture_order, vm_id) values('%s', '%s', %d, '%s')''' % (stack_id, student_id, current_count, instance_id)
            cursor.execute(query)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return getInstanceConsole(X_AUTH_TOKEN, instance_id)

def uploadFile(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str, content):
    url = "%s:8080/v1/AUTH_%s/test/%s/%s/%s" % (localhost, tenant_id, student_id, foldername, filename)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.put(url, headers=rHeader, data=content)
    result.raise_for_status()

def fetchFile(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str):
    url = localhost + ":8080/v1/AUTH_%s/test/%s/%s/%s" % (tenant_id, student_id, foldername, filename)
    print(url)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.get(url, headers=rHeader)
    result.raise_for_status()
    return result

def uploadPost(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str, title:str, content: str, upload_filename: str):
    uploadFile(X_AUTH_TOKEN, student_id, tenant_id, foldername, filename, content)

    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''insert into threads(title, content, filename, foldername, student_id, written) values('%s', '%s', '%s', '%s', '%s', NOW())''' % (title, filename, upload_filename, foldername, student_id)
    cursor.execute(query)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    print({ 'filename': upload_filename, 'foldername': foldername })
    return { 'filename': upload_filename, 'foldername': foldername }


def fetchPost():
    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''select * from threads'''
    cursor.execute(query)

    result = cursor.fetchall()
    lecture_sign_up_list.close()

    return list(result)

def deletePost(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, post_id: int):
    url = localhost + ":8080/v1/AUTH_%s/test/%s/%s" % (tenant_id, student_id, foldername)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }
    print(url)
    ##result = requests.delete(url, headers=rHeader)
    ##result.raise_for_status()

    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''delete from threads where id = %d''' % (post_id)
    cursor.execute(query)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return {}


