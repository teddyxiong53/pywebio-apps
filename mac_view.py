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

def main():
    put_markdown("## mac地址申请记录")
    # 就用表格来呈现。
    # 读取数据库里的apply_table。
    Apply = Query()
    apply_record = apply_table.all()
    record_table = [
        ['申请人', '申请时间', '申请用途', '申请数量'],
    ]
    for rc in apply_record:
        record_table.append([rc['username'], rc['time'], rc['usage'], rc['num']])
    put_table(
        record_table
    )
if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
