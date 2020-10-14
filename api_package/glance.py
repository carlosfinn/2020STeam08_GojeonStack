
import requests, json, pymysql

localhost = "http://164.125.70.19"

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