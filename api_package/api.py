import requests, json, pymysql

localhost = "http://164.125.70.19"

def getFlavors(X_AUTH_TOKEN: str):
    url = localhost + "/compute/v2.1/flavors/detail"
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    RAW = requests.get(url, headers=rHeaders)
    RAW.raise_for_status()

    rBody = RAW.json()

    return rBody.get('flavors', None)

def createInstance(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, image: str, vcpus: int, ram: int, disk: int, personeel: int):
    url = localhost + "/heat-api/v1/" + tenant_id + "/stacks"

    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    flavor_name = stack_name + "_flavor"
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
                }
            }
        }
    }

    for x in range(personeel):
        volume_name = stack_name + "_volume" + "%2d" % (x)
        instance_name = stack_name + "_server" + "%2d" % (x)
        
        rBody["template"]["resources"].update({
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
                    }]
                }
            }
        })

    print(json.dumps(rBody))
    requestResult = requests.post(url, headers=rHeaders, data=json.dumps(rBody))
    requestResult.raise_for_status()

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
    print(imageInfo)

    return imageInfo

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
    sql_query = '''delete * from sign_up_list where lecture_id = '%s';''' % (stack_id)
    cursor.execute(sql_query)

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

def uploadImage(X_AUTH_TOKEN: str, fstream, name: str, disk_format: str, min_disk: int, min_ram: int):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }
    rBody = {
        "disk_format": disk_format,
        "min_disk": min_disk,
        "min_ram": min_ram,
        "name": name
    }

    print(rHeaders, "\n\n", rBody, "\n\n")

    url = localhost + "/image/v2/images"
    requestResult = requests.post(url, headers=rHeaders, data=json.dumps(rBody))
    requestResult.raise_for_status()

    image_info = requestResult.json()
    print(f"\033[94mFinished: You finished the first process. Continue?\033[0m")

    image_id = image_info.get("id", None)
    url = url + '/' + image_id + '/file'

    rHeaders = {
        'Content-Type': 'application/octet-stream',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    requestResult = requests.put(url, headers=rHeaders, data=fstream)
    requestResult.raise_for_status()
    print(f"\033[94mFinished: You finished the second process. Continue?\033[0m")

    return { "result_code": requestResult.status_code }

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

def getInstanceInfo(resources: list) -> list:
    instance_list = list()

    for resource in resources:
        if resource.get("resource_type", "") == "OS::Nova::Server":
            instance_list.append(resource)
    
    return instance_list


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

    return console_info.get("console", {})

def getCurrentStudent(stack_id: str):
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
    return result[0]