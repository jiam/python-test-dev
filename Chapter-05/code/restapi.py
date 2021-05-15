import json
from functools import wraps
from flask import Flask, make_response, request

app = Flask(__name__)

""" storage all users' data
data structure:
    users_dict = {
        'uid1': {
            'name': 'name1',
            'password': 'pwd1'
        },
        'uid2': {
            'name': 'name2',
            'password': 'pwd2'
        }
    }
"""
users_dict = {}

def validate_request(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token', "")

        if not token:
            result = {
                'success': False,
                'msg': "token is null."
            }
            response = make_response(json.dumps(result), 401)
            response.headers["Content-Type"] = "application/json"
            return response

        if token !='abcd-1234-efgh-9876':
            result = {
                'success': False,
                'msg': "Authorization failed!"
            }
            response = make_response(json.dumps(result), 403)
            response.headers["Content-Type"] = "application/json"
            return response

        return func(*args, **kwargs)

    return wrapper


def auth(user,password):
    if user=='root' and password=='123456':
        return True
    return False


@app.route('/')
def index():
    return "Hello World!"

@app.route('/api/get-token', methods=['POST'])
def get_token():
    data = request.get_json()
    print(data)
    user = data.get('user', '')
    password = data.get('password','')
    
    if auth(user, password):
        result = {
            'success': True,
            'token': 'abcd-1234-efgh-9876'
        }
        response = make_response(json.dumps(result), 403)
    else:
        result = {
            'success': False,
            'token': ''
        }
        response = make_response(json.dumps(result))

    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/api/users')
@validate_request
def get_users():
    print(users_dict)
    users_list = [user for uid, user in users_dict.items()]
    users = {
        'success': True,
        'count': len(users_list),
        'items': users_list
    }
    response = make_response(json.dumps(users))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/api/reset-all')
@validate_request
def clear_users():
    users_dict.clear()
    result = {
        'success': True
    }
    response = make_response(json.dumps(result))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/api/users/<int:uid>', methods=['POST'])
@validate_request
def create_user(uid):
    user = request.get_json()
    if uid not in users_dict:
        result = {
            'success': True,
            'msg': "user created successfully."
        }
        status_code = 201
        users_dict[uid] = user
    else:
        result = {
            'success': False,
            'msg': "user already existed."
        }
        status_code = 500

    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/api/users/<int:uid>')
@validate_request
def get_user(uid):
    user = users_dict.get(uid, {})
    if user:
        result = {
            'success': True,
            'data': user
        }
        status_code = 200
    else:
        result = {
            'success': False,
            'data': user
        }
        status_code = 404

    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/api/users/<int:uid>', methods=['PUT'])
@validate_request
def update_user(uid):
    user = users_dict.get(uid, {})
    if user:
        user = request.get_json()
        success = True
        status_code = 200
        users_dict[uid] = user
    else:
        success = False
        status_code = 404

    result = {
        'success': success,
        'data': user
    }
    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/api/users/<int:uid>', methods=['DELETE'])
@validate_request
def delete_user(uid):
    user = users_dict.pop(uid, {})
    if user:
        success = True
        status_code = 200
    else:
        success = False
        status_code = 404

    result = {
        'success': success,
        'data': user
    }
    response = make_response(json.dumps(result), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(
        host="0.0.0.0"
    )
