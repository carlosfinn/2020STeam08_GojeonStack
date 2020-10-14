
import requests, json, pymysql

localhost = "http://164.125.70.19"

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
