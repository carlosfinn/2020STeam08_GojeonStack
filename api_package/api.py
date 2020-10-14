
import requests, json, pymysql
##import heat

localhost = "http://164.125.70.19"

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
    cursor.execute(
        '''create table lectures (lecture_id varchar(64) not null, personeel int not null, creator_id varchar(255) not null;'''
    )

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return {}
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

