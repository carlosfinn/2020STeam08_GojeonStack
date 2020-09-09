import json
import requests

url_base = "http://164.125.70.19"

def getToken(id,pw):
    body = \
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": id,
                            "domain": {
                                "name": "Default"
                            },
                            "password": pw
                        }
                    }
                }   
            }
        }
    
    header = {
        'Content-Type': 'application/json',
    }

    print(json.dumps(body))
    result = requests.post(url_base + '/identity/v3/auth/tokens', headers=header, data=json.dumps(body), verify=True)
    resultCode = result.status_code
    # print("--------------")
    # print(resultCode)
    resultJson = result.json()
    print(resultJson)
    if int(resultCode) == 201:
        token = result.headers['X-Subject-Token']
        userId = resultJson['token']['user']['id']
    if int(resultCode) == 401:
        token = None
        userId = resultJson['error']['title']
    
    

    return token, userId

def getScopedToken(token, userId, pw):
    body = \
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "id": userId,
                            "password": pw
                        }
                    }
                },
                "scope": {
                    "system": {
                        "all": True
                    }
                }
            }
        }
        
    
    header = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    result = requests.post(url_base + '/identity/v3/auth/tokens', headers=header, data=json.dumps(body), verify=True)
    
    token = result.headers['X-Subject-Token']

    return token

 
def createUser(token, project_id, name, pw, email):
    body = \
        {
            "user": {
                "domain_id": "default",
                "default_project_id": project_id,
                "enabled": True,
                "name" : name,
                "password": pw,
                "email": email,
                "options": {
                    "ignore_password_expiry": True
                }
            }
        }
    
    header = {
        'Content-Type': 'application/json',
        'X-Auth-Token': token
    }

    result = requests.post(url_base + '/identity/v3/users', headers=header, data=json.dumps(body), verify=True)
    # result.raise_for_status()

    resultCode = result.status_code
    resultJson = result.json()
    if int(resultCode) == 201:
        user_id = resultJson['user']['id']
    if int(resultCode) == 409:
        user_id = resultJson['error']['title']
    # for x in userList:
    #     user_id = x['id']
    #     break
    #user_id = [ x['id'] for x in resultJson['user'] if not x['id'] == "None"]

    return user_id

def assignRoletoUser(token, project_id, user_id, role_id):
    url = url_base + "/identity/v3/projects/" + project_id + "/users/" + user_id + "/roles/" + role_id

    header = {
        'X-Auth-Token': token
    }
    requests.put(url, headers= header)

def getUserRole(token, project_id, user_id):
    url = url_base + "/identity/v3/projects/" + project_id +  "/users/" + user_id + "/roles"

    header = {
        'X-Auth-Token': token
    }

    result = requests.get(url, headers=header)
    resultJson = result.json()
    role = ""
    roleList = resultJson['roles']

    for x in roleList:
        role = x['name']
        break
    return role


def getProjectId(token):
    header = {
        'X-Auth-Token': token
    }
    result = requests.get(url_base + '/identity/v3/auth/projects', headers = header)
    
    resultJson = result.json()
    project_name = ""
    project_id = ""
    projectList = resultJson['projects']
    for x in projectList:
        project_name = x['name']
        project_id = x['id']
        break        

    return project_id, project_name


