from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import info as session_info, run_js
import time
from tinydb import TinyDB, Query
import re
import datetime

db = TinyDB('./db.json')
user_table = db.table('user')
apply_table = db.table('apply')

def check_signup(data):
    # if valid username
    # 小写英文和数字，还有下划线，只允许这3种字符。
    # 长度在3到20个字符。
    # 只能以字母开头。
    # ^[a-z0-9_]{3,20}$
    res = re.search('^[a-z0-9_]{3,20}$', data['username'])
    if not res:
        return ('username', '用户名不合法')
    # if valid password
    if len(data['password'].strip()) < 6:
        return ('password', '密码长度不合法')

'''
检查登陆的用户名和密码
'''
def check_signin(data):
    # 读取数据库的user表
    User = Query()
    # print(data['username'])
    # print(user_table.all())
    user = user_table.search(User.username == data["username"])[0]
    # print(user)
    if not user:
        return ('username', '该用户名没有注册')
    # check password
    print("-------------")
    print(user['password'])
    print("-------------")
    print(data['password'])
    if user['password'] != data['password']:
        return ('password', '密码输入错误')
def main():
    put_markdown("## mac地址申请系统")
    
    choice = actions('登陆/注册', 
            ['登陆', '注册']
        )
    if choice == '注册': 
        signup_info = input_group('注册', [
            input('用户名', name='username', required=True, help_text='用户名只能包含小写字母，字母，下划线这3种符号，长度3到20个字符'),
            input('密码', name='password',  required=True, type=PASSWORD, help_text='密码长度至少6位')
        ], validate=check_signup)
        # check 
        # write info to db
        # use tinydb to store info
        
        user_table.insert({
            'username': signup_info['username'],
            'password': signup_info['password']
        })
        put_success('注册成功，现在可以登陆了', closable=True)
        # 然后跳转到登录界面。
        # 只能强制刷新一下。
        run_js('''
            window.location.reload();
        ''')
    else:
        signin_info = input_group('登陆', [
            input('用户名', name='username', required=True),
            input('密码', name='password',type=PASSWORD, required=True)
        ], validate=check_signin)
        # 到这里，说明登陆成功了。
        # 显示申请的表单。
        apply_info = input_group('申请MAC地址', [
            input('申请人', name='username', readonly=True, value=f'{signin_info["username"]}'),
            textarea('申请用途', name='usage', rows=3, required=True),
            input('申请数量', name='num', required=True, value=100, type=NUMBER),
        ])
        # 开始写入到数据库。
        apply_table.insert({
            'username': apply_info['username'],
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
            'usage': apply_info['usage'],
            'num': apply_info['num'],
        })
        # 提示申请成功。
        # 可以查看所有的申请数据。
        put_success('申请mac地址成功，可以点击下面按钮查看所有申请数据', closable=True)
        put_markdown('''
        - [查看MAC地址申请记录](./mac_view):查看mac地址申请的记录。
        ''')
if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
