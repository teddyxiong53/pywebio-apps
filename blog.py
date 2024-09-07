from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env, run_js, eval_js, local as session_local
import sqlite3
import hashlib
import time

# 初始化数据库
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# 用户注册
def register():
    info = input_group("用户注册", [
        input("用户名", name="username", required=True),
        input("密码", name="password", type="password", required=True)
    ])
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    try:
        hashed_password = hashlib.sha256(info['password'].encode()).hexdigest()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (info['username'], hashed_password))
        conn.commit()
        put_success("注册成功!")
    except sqlite3.IntegrityError:
        put_error("用户名已存在!")
    finally:
        conn.close()

# 用户登录
def login():
    info = input_group("用户登录", [
        input("用户名", name="username", required=True),
        input("密码", name="password", type="password", required=True)
    ])
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(info['password'].encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (info['username'], hashed_password))
    user = c.fetchone()
    conn.close()
    if user:
        run_js("localStorage.setItem('username', '%s')" % info['username'])
        put_success("登录成功!")
        return True
    else:
        put_error("用户名或密码错误!")
        return False

# 发表文章
def post_article():
    info = input_group("发表文章", [
        input("标题", name="title", required=True),
        textarea("内容", name="content", required=True)
    ])
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    username = eval_js("localStorage.getItem('username')")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c.execute("INSERT INTO posts (title, content, author, timestamp) VALUES (?, ?, ?, ?)", 
              (info['title'], info['content'], username, timestamp))
    conn.commit()
    conn.close()
    put_success("文章发表成功!")

# 查看文章列表
def view_articles():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY timestamp DESC")
    posts = c.fetchall()
    conn.close()
    
    for post in posts:
        put_text(f"标题: {post[1]}")
        put_text(f"作者: {post[3]}")
        put_text(f"时间: {post[4]}")
        put_text(f"内容: {post[2][:100]}...")  # 只显示前100个字符
        put_button("阅读全文", onclick=lambda p=post: view_full_article(p))
        put_text("---")

# 查看完整文章
def view_full_article(post):
    clear()
    put_text(f"标题: {post[1]}")
    put_text(f"作者: {post[3]}")
    put_text(f"时间: {post[4]}")
    put_text(f"内容: {post[2]}")
    put_button("返回", onclick=lambda: run_js("window.location.reload()"))

# 主页
def navbar():
    def nav_click(btn):
        if btn == '首页':
            main()
        elif btn == '发表文章':
            post_page()
        elif btn == '查看文章':
            view_page()
        elif btn == '注册':
            register_page()
        elif btn == '登录':
            login_page()
        elif btn == '登出':
            logout_page()

    put_column([
        put_buttons(['首页', '发表文章', '查看文章', '注册', '登录', '登出'], onclick=nav_click),
        put_text('---')  # 分隔线
    ])
    
    username = eval_js("localStorage.getItem('username')")
    if username:
        put_text(f"欢迎, {username}!")
    else:
        put_text("请登录")

def entry():
    clear()
    navbar()
    put_text("欢迎来到简单博客系统")

def register_page():
    clear()
    navbar()
    register()

def login_page():
    clear()
    navbar()
    if login():
        main()

def post_page():
    clear()
    navbar()
    username = eval_js("localStorage.getItem('username')")
    if not username:
        put_error("请先登录!")
        return
    post_article()

def view_page():
    clear()
    navbar()
    view_articles()

def logout_page():
    run_js("localStorage.removeItem('username')")
    put_success("已登出!")
    main()

def main():
    set_env(title="简单博客系统")
    init_db()
    entry()

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)