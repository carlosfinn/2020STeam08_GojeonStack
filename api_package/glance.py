#-*- coding:utf-8 -*-
import requests, json, pymysql
from localhost import localhost

## glance는 이미지를 관리하는 오픈스택 내의 구성요소입니다. 
## 이미지는 가상머신을 구동할 때 OS의 역할을 하는 파일입니다. 
## 이미지의 경우 아파치 서버의 문제 때문에 여기에 작성되지 않고 api 서버를 위한 파일인 dashboard.py 파일에 구현된 부분이 있습니다. 
## 이 부분의 경우 오픈스택 내의 웹API가 아닌 명령어 방식인 CLI를 사용했으므로 해당 사항에 대해서는 아래를 참고 바랍니다. 
## https://docs.openstack.org/python-openstackclient/latest/cli/command-objects/image-v2.html


## getImageList
## 기능 : 현재 등록된 이미지를 확인한다. 
## 관련 : Openstack Glance (이미지 컴포넌트)
## 현재 서비스 내에 등록되어있는 이미지를 확인한다. 

def getImageList(X_AUTH_TOKEN: str):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost() + "/image/v2/images"
    requestResult = requests.get(url, headers=rHeaders)
    requestResult.raise_for_status()

    resultJson = requestResult.json()
    imageInfo = resultJson.get("images", [])

    return imageInfo


## createImageInfo
## 기능 : 이미지의 정보를 등록한다. 
## 관련 : Openstack Glance (이미지 컴포넌트)
## 이미지 파일 원본을 제외한 이미지를 등록한다. 그 이후 이미지 파일에 대한 url를 반환하여 파일 첨부를 할 수 있게 한다. 

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

    url = localhost() + "/image/v2/images"
    requestResult = requests.post(url, headers=rHeaders, data=json.dumps(rBody))
    requestResult.raise_for_status()
    resultJson = requestResult.json()
    fileuploadurl = localhost() + "/image" + resultJson.get('file', None)
    print(resultJson)

    return fileuploadurl


## deleteImage
## 기능 : 이미지를 삭제한다. 
## 관련 : Openstack Glance (이미지 컴포넌트)
## 이미지를 삭제한다. 

def deleteImage(X_AUTH_TOKEN: str, image_id):
    rHeaders = {
        'Content-Type': 'application/json',
        "X-Auth-Token": X_AUTH_TOKEN
    }

    url = localhost() + '/image/v2/images/%s' % (image_id)
    requestResult = requests.delete(url, headers=rHeaders)
    requestResult.raise_for_status()

    return {}


## searchforImage
## 기능 : 어떠한 이름을 가지고 있는 이미지를 검색한다.  
## 관련 : Openstack Glance (이미지 컴포넌트)
## 어떠한 이름을 가지고 있는 이미지를 검색한다.  

def searchforImage(X_AUTH_TOKEN: str, name: str):
    imagelist = getImageList(X_AUTH_TOKEN)

    for image in imagelist:
        if image.get("name", '') == name: return image.get("id", '')