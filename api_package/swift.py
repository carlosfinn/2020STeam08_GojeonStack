import requests, json, pymysql
from localhost import localhost


##initContainer
def initContainer(X_AUTH_TOKEN: str, tenant_id: str, name: str):
    url = "%s:8080/v1/AUTH_%s/%s" % (localhost(), tenant_id, name)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.put(url, headers=rHeader)
    return result.status_code

## uploadFile
## 기능 : 파일을 저장하는 기능
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 

def uploadFile(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str, content):
    url = "%s:8080/v1/AUTH_%s/test/%s/%s/%s" % (localhost(), tenant_id, student_id, foldername, filename)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.put(url, headers=rHeader, data=content)
    result.raise_for_status()


## fetchFile
## 기능 : 파일을 저장하는 기능
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 

def fetchFile(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str):
    url = localhost() + ":8080/v1/AUTH_%s/test/%s/%s/%s" % (tenant_id, student_id, foldername, filename)
    print(url)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.get(url, headers=rHeader)
    result.raise_for_status()
    return result


## uploadPost
## 기능 : 게시물을 게재하는 기능
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 
## 글은 기본적으로 첨부파일 + 글의 텍스트 파일로 구성되어 Swift 안에 한 폴더에 저장됩니다. 

def uploadPost(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str, title:str, content: str, upload_filename: str):
    initContainer(X_AUTH_TOKEN, tenant_id, "test")
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

    return { 'filename': upload_filename, 'foldername': foldername }


## modifyPost
## 기능 : 게시물을 수정하는 기능
def modifyPost(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, threadname: str, title:str, content: str, dbid: int):
    uploadFile(X_AUTH_TOKEN, student_id, tenant_id, foldername, threadname, content)
    print("second step finished")

    lecture_sign_up_list = pymysql.connect(
        user='root',
        passwd='8nkujc3rf',
        host='localhost',
        db='lecture_sign_up_list',
        charset='utf8'
    )

    cursor = lecture_sign_up_list.cursor(pymysql.cursors.DictCursor)
    query = '''update threads set title='{title}', written=NOW() WHERE id={id}'''.format(title=title, id=dbid)
    cursor.execute(query)

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return {}

## fetchPost
## 기능 : 글 목록 가져오기
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 

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


## deletePost
## 기능 : 글 삭제하기
## 관련 : mysql 데이터베이스
## 게시물이 표시되지 않도록 글 목록의 데이터베이스에서 해당 글 삭제

def deletePost(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, post_id: int):
    url = localhost() + ":8080/v1/AUTH_%s/test/%s/%s" % (tenant_id, student_id, foldername)
    ##rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }
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


## uploadKeyPair
## 기능 : 파일을 저장하는 기능
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 

def uploadKeyPair(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str, content: str):
    url = "%s:8080/v1/AUTH_%s/keypairs/%s" % (localhost(), tenant_id, "keypair-%s.pem" % (stack_name))
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.put(url, headers=rHeader, data=content)
    result.raise_for_status()

    return url


## createKeypair
## 입력 : 강의에 ssh 접속을 위한 기능을 제공
## 기능 : 강의를 위한 접속 기능 제공
## 관련 : mysql 데이터베이스
## 특정 강의의 생성자 id를 확인한다. 

def createKeypair(X_AUTH_TOKEN: str, stack_name: str, tenant_id: str) -> dict:
    url = localhost() + "/compute/v2.1/os-keypairs"
    rBody = {
        "keypair": {
            "name": "keypair-%s" % (stack_name)
        }
    }
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.post(url, headers=rHeader, data=json.dumps(rBody))
    result.raise_for_status()

    keypair = result.json().get("keypair", None)
    pem_content = keypair.get("private_key", None)

    initContainer(X_AUTH_TOKEN, tenant_id, "keypairs")
    return uploadKeyPair(X_AUTH_TOKEN, tenant_id, stack_name, pem_content)

## fetchKeypair
## 기능 : keypair을 저장하는 기능
## Openstack에서의 가상머신에는 간접적으로 ssh를 통해서 접속하는 것이 가능합니다. 
## 이 때 접속을 하기 위해서는 인스턴스 내에 keypair라고 하는 ssh 보안을 위한 인증서를 설정합니다. 
## 그렇기 때문에 인증서가 필요한데 그 인증서를 제공해주는 것입니다. 

def fetchKeypair(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str):
    url = localhost() + ":8080/v1/AUTH_%s/keypairs/keypair-%s.pem" % (tenant_id, stack_name)
    print(url)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.get(url, headers=rHeader)
    result.raise_for_status()
    return result

## deleteKeypair
## 기능 : keypair을 삭제하는 기능

def deleteKeypair(X_AUTH_TOKEN: str, tenant_id: str, stack_name: str):
    url = localhost() + "/compute/v2.1/os-keypairs/keypair-%s" % (stack_name)
    swifturl = localhost() + ":8080/v1/AUTH_%s/keypairs/keypair-%s.pem" % (tenant_id, stack_name)
    print(url)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.delete(url, headers=rHeader)
    result.raise_for_status()
    result = requests.delete(swifturl, headers=rHeader)
    result.raise_for_status()
    return result