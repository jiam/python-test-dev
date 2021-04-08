def permit(f):
    def wrapper(info):
        if info.username == 'root' and info.passwd=='123':
            print('你有权限')
            return f(info)
        else:
            print('你没有权限')
            return
            
    return wrapper


@permit
def test(info):
    return  '123'

class Info:
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

info = Info('root', '1234')

print(test(info))