
import requests, json, pymysql

localhost = "http://164.125.70.19"

## 시스템을 사용하기 전에 데이터베이스를 세팅해줘야합니다. 
## 그 과정을 수행하는 것입니다. 

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
        '''create table threads(id int(16) not null auto_increment primary key, title varchar(255) not null, content varchar(255) not null, filename varchar(255), foldername varchar(255) not null, student_id varchar(255) not null, written Datetime(6));'''
    )
    cursor.execute(
        '''create table sign_up_list (lecture_id varchar(255) not null, student_id varchar(255) not null, lecture_order int(16) unsigned not null, vm_id varchar(255) not null);'''
    )
    cursor.execute(
        '''create table lectures (lecture_id varchar(64) not null, personeel int not null, creator_id varchar(255) not null);'''
    )

    lecture_sign_up_list.commit()
    lecture_sign_up_list.close()

    return {}

