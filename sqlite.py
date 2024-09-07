from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env, run_js
import sqlite3
import tempfile
import os

def main():
    set_env(title="SQLite 数据库操作应用")
    
    put_markdown("# SQLite 数据库操作应用")
    
    # 替换文件路径输入为文件上传
    db_file = file_upload("请上传 SQLite 数据库文件：", accept=".db,.sqlite,.sqlite3")
    
    if not db_file:
        put_error("未上传文件")
        return
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_file:
        temp_file.write(db_file['content'])
        db_path = temp_file.name
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        put_success("成功连接到数据库！")
    except sqlite3.Error as e:
        put_error(f"连接数据库时出错：{e}")
        os.unlink(db_path)  # 删除临时文件
        return
    
    while True:
        choice = select("请选择操作：", [
            "查看所有表",
            "创建新表",
            "查询表数据",
            "插入数据",
            "更新数据",
            "删除数据",
            "删除表",
            "退出"
        ])
        
        if choice == "查看所有表":
            view_tables(cursor)
        elif choice == "创建新表":
            create_table(cursor, conn)
        elif choice == "查询表数据":
            query_table(cursor)
        elif choice == "插入数据":
            insert_data(cursor, conn)
        elif choice == "更新数据":
            update_data(cursor, conn)
        elif choice == "删除数据":
            delete_data(cursor, conn)
        elif choice == "删除表":
            drop_table(cursor, conn)
        else:
            break
    
    conn.close()
    os.unlink(db_path)  # 删除临时文件
    put_info("已断开数据库连接。")

def view_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        put_table([["表名"]] + tables)
    else:
        put_warning("数据库中没有表。")

def create_table(cursor, conn):
    table_name = input("请输入新表的名称：")
    columns = []
    while True:
        col = input("请输入列名和类型（格式：列名 类型），留空结束：")
        if not col:
            break
        columns.append(col)
    
    if columns:
        query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        try:
            cursor.execute(query)
            conn.commit()
            put_success(f"成功创建表 {table_name}")
        except sqlite3.Error as e:
            put_error(f"创建表时出错：{e}")
    else:
        put_warning("没有输入列，取消创建表。")

def query_table(cursor):
    table_name = input("请输入要查询的表名：")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        if rows:
            columns = [description[0] for description in cursor.description]
            put_table([columns] + rows)
        else:
            put_info(f"表 {table_name} 中没有数据。")
    except sqlite3.Error as e:
        put_error(f"查询表时出错：{e}")

def insert_data(cursor, conn):
    table_name = input("请输入要插入数据的表名：")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    values = []
    for col in columns:
        value = input(f"请输入 {col} 的值：")
        values.append(value)
    
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"
    try:
        cursor.execute(query, values)
        conn.commit()
        put_success("数据插入成功！")
    except sqlite3.Error as e:
        put_error(f"插入数据时出错：{e}")

def update_data(cursor, conn):
    table_name = input("请输入要更新数据的表名：")
    condition = input("请输入更新条件（例如：id=1）：")
    update_col = input("请输入要更新的列名：")
    new_value = input("请输入新的值：")
    
    query = f"UPDATE {table_name} SET {update_col} = ? WHERE {condition}"
    try:
        cursor.execute(query, (new_value,))
        conn.commit()
        put_success(f"成功更新 {cursor.rowcount} 行数据。")
    except sqlite3.Error as e:
        put_error(f"更新数据时出错：{e}")

def delete_data(cursor, conn):
    table_name = input("请输入要删除数据的表名：")
    condition = input("请输入删除条件（例如：id=1）：")
    
    query = f"DELETE FROM {table_name} WHERE {condition}"
    try:
        cursor.execute(query)
        conn.commit()
        put_success(f"成功删除 {cursor.rowcount} 行数据。")
    except sqlite3.Error as e:
        put_error(f"删除数据时出错：{e}")

def drop_table(cursor, conn):
    table_name = input("请输入要删除的表名：")
    confirm = input(f"您确定要删除表 {table_name} 吗？这将永久删除表及其所有数据。(输入 'yes' 确认)")
    
    if confirm.lower() == 'yes':
        try:
            cursor.execute(f"DROP TABLE {table_name}")
            conn.commit()
            put_success(f"成功删除表 {table_name}")
        except sqlite3.Error as e:
            put_error(f"删除表时出错：{e}")
    else:
        put_info("取消删除表操作。")

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
