import requests
from api_server import get_sign

def get_token():
    url = 'http://127.0.0.1:5000/api/get-token'
    device_sn = '1234567'
    os_platform = 'win10'
    app_version = '2.8.6'
    headers = {'device_sn':device_sn,
        'os_platform': os_platform,
        'app_version': app_version}
    
    sign = get_sign(device_sn,os_platform,app_version)
    data = {'sign': sign}
    proxies = {'http': '127.0.0.1:8888'}
    r = requests.post(url,json=data,headers=headers)
    return r.json()

def create_user(id, name, password,token):
    device_sn = '1234567'
    url = 'http://127.0.0.1:5000/api/users/%s' % id
    headers = {'device_sn':device_sn,
        'token': token}
    data = {'name': name, 'password': password}
    proxies = {'http': '127.0.0.1:8888'}
    r = requests.post(url,json=data, headers=headers)
    return r.json()

def get_users(token):
    device_sn = '1234567'
    url = 'http://127.0.0.1:5000/api/users'
    headers = {'device_sn':device_sn,
        'token': token}
    r = requests.get(url,headers=headers)
    return r.json()
    


if __name__ == '__main__':
    content = get_token()
    print(content)
    #content2 = create_user(1000, 'test', 'test', content['token'])
    #print(content2)
    #content3 = get_users(content['token'])
    #print(content3)
    
    
