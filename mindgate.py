import requests

api_base_url = "http://localhost:8080"


def requestSender(mapping_url, params, method):
    headers = {'Content-Type': 'application/json'}
    url = api_base_url + mapping_url

    response = None

    if method == "GET":
        response = requests.get(url=url, headers=headers, params=params)
    elif method == "POST":
        response = requests.post(url=url, headers=headers, params=params)
    elif method == "PATCH":
        response = requests.patch(url=url, headers=headers, params=params)
    elif method == "DELETE":
        response = requests.delete(url=url, headers=headers, params=params)

    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        return f'SERVER ERROR: {response.status_code}'


def sendMessageAsUser(user_id, message):
    mapping_url = "/sendMessage"
    params = {"id": user_id, "message": message, "role": "user"}
    return requestSender(mapping_url, params, "POST")


def sendMessageAsSystem(user_id, message):
    mapping_url = "/sendMessage"
    params = {"id": user_id, "message": message, "role": "system"}
    return requestSender(mapping_url, params, "POST")


def clearMessages(user_id):
    mapping_url = "/clearMessages"
    params = {"id": user_id}
    return requestSender(mapping_url, params, "PATCH")


def getModel(user_id):
    mapping_url = "/getModel"
    params = {"id": user_id}
    return requestSender(mapping_url, params, "GET")


def setModel(user_id, model):
    mapping_url = "/setModel"
    params = {"id": user_id, "model": model}
    return requestSender(mapping_url, params, "PATCH")


def getBalance(user_id):
    mapping_url = "/getBalance"
    params = {"id": user_id}
    return requestSender(mapping_url, params, "GET")


def addBalance(user_id, amount):
    mapping_url = "/addBalance"
    params = {"id": user_id, "amount": amount}
    return requestSender(mapping_url, params, "PATCH")
