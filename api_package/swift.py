
import requests, json, pymysql

localhost = "http://164.125.70.19"


##initContainer
def initContainer(X_AUTH_TOKEN: str, tenant_id: str):
    url = "%s:8080/v1/AUTH_%s/test" % (localhost, tenant_id)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.put(url, headers=rHeader)

## uploadFile
## 기능 : 파일을 저장하는 기능
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 

def uploadFile(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str, content):
    url = "%s:8080/v1/AUTH_%s/test/%s/%s/%s" % (localhost, tenant_id, student_id, foldername, filename)
    rHeader = { 'X-Auth-Token': X_AUTH_TOKEN }

    result = requests.put(url, headers=rHeader, data=content)
    result.raise_for_status()


## fetchFile
## 기능 : 파일을 저장하는 기능
## Openstack에서는 파일 저장 및 관리를 담당하는 Swift라는 컴포넌트가 있는데 이를 통해 파일을 관리할 수 있습니다. 
## 이 때 계정 별로 컨테이너를 생성할 수 있고 여기에 파일을 저장할 수 있습니다. 
## 이 때 계정을 생성할 때 별도로 container를 생성해줘야 파일을 저장할 수 있습니다. 

def fetchFile(X_AUTH_TOKEN: str, student_id: str, tenant_id: str, foldername: str, filename: str):
    url = localhost + ":8080/v1/AUTH_%s/test/%s/%s/%s" % (tenant_id, student_id, foldername, filename)
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
    initContainer(X_AUTH_TOKEN, tenant_id)
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
    url = localhost + ":8080/v1/AUTH_%s/test/%s/%s" % (tenant_id, student_id, foldername)
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
