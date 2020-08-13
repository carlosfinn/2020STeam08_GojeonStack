from flask import Flask, request, make_response
from flask_cors import CORS
import json, os, api
import random, string, time

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

app = Flask(__name__)

cors = CORS(
    app, resources={
        r"/*": {"origin": "*"},
        r"/api/*": {"origin": "*"},
        r"/api/vm/*": {"origin": "*"},
        r"/api/stack/*": {"origin": "*"},
        r"/api/image/*": {"origin": "*"}
    }
)

@app.route('/api/flavors', methods=['GET'])
def getFlavor():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get('X-Auth-Token', None)

    result = api.getFlavors(X_AUTH_TOKEN)
    print(json.dumps(result))

    return json.dumps(result)

@app.route('/api/stack/create', methods=['POST'])
def createStack():
    requestHeader = request.headers
    requestBody = json.loads(request.get_data())
    print(requestBody)

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    image = requestBody.get("image", None)
    vcpus = requestBody.get("vcpus", 1)
    ram = requestBody.get("ram", 2048)
    disk = requestBody.get("disk", 24)
    stack_name = requestBody.get("stack_name", get_random_string(16))

    result = api.createInstance(X_AUTH_TOKEN, tenant_id, stack_name, image, vcpus, ram, disk)
    print(X_AUTH_TOKEN, tenant_id, stack_name, image, vcpus, ram, disk)
    return json.dumps(result)

@app.route('/api/stack/details', methods=['GET'])
def getStackDetails():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)

    result = api.getStackStatus(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    print(result)

    return json.dumps(result)

@app.route('/api/stack/list', methods=['GET'])
def listStack():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    result = api.getStackList(X_AUTH_TOKEN, tenant_id)

    return json.dumps(result)

@app.route('/api/stack/delete', methods=['DELETE'])
def deleteStack():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    tenant_id = requestHeader.get("tenant_id", None)

    requestBody = json.loads(request.get_data())

    stack_name = requestBody.get("stack_name", None)
    stack_id = requestBody.get("stack_id", None)

    result = api.deleteStack(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)

    return json.dumps(result)

@app.route('/api/image/list', methods=['GET'])
def listImage():
    requestHeader = request.headers
    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)

    result = api.getImageList(X_AUTH_TOKEN)

    return json.dumps(result)

@app.route('/api/image/create', methods=['PUT'])
def createImage():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    disk_format = requestHeader.get("disk_format", "qcow2")
    min_disk = requestHeader.get("min_disk", 0)
    min_ram = requestHeader.get("min_ram", 0)
    name = requestHeader.get("name", get_random_string(16))

    print(request.get_data())
    result = api.uploadImage(X_AUTH_TOKEN, request.get_data(), name, disk_format, int(min_disk), int(min_ram))

    return json.dumps(result)

@app.route('/api/stack/console', methods=['POST'])
def getResources():
    requestHeader = request.headers

    X_AUTH_TOKEN = requestHeader.get("X-Auth-Token", None)
    stack_name = requestHeader.get("stack_name", None)
    stack_id = requestHeader.get("stack_id", None)
    tenant_id = requestHeader.get("tenant_id", None)

    resources = api.getStackResources(X_AUTH_TOKEN, tenant_id, stack_name, stack_id)
    instance = api.getInstanceInfo(resources)
    console_info = api.getInstanceConsole(X_AUTH_TOKEN, instance.get("physical_resource_id", ""))

    return json.dumps(console_info)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)

