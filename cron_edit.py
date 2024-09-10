from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from crontab import CronTab
import os

def get_crontab():
    # 直接创建当前用户的CronTab对象
    return CronTab()

def main():
    put_markdown("# Cron 定时任务编辑器")

    while True:
        action = select("选择操作", ["查看现有任务", "添加新任务", "删除任务", "退出"])

        if action == "查看现有任务":
            show_tasks()
        elif action == "添加新任务":
            add_task()
        elif action == "删除任务":
            delete_task()
        else:
            break

    put_text("感谢使用!")

def show_tasks():
    cron = get_crontab()
    tasks = [f"{job.command} ({job.schedule()})" for job in cron]
    
    if tasks:
        put_table([
            ["任务", "计划"],
            *[(task.split('(')[0].strip(), task.split('(')[1].strip(')')) for task in tasks]
        ])
    else:
        put_text("当前没有定时任务")

def add_task():
    command = input("输入要执行的命令:")
    schedule = input("输入cron表达式 (例如: */5 * * * *):")

    cron = get_crontab()
    job = cron.new(command=command)
    job.setall(schedule)
    cron.write()

    put_success("任务添加成功!")

def delete_task():
    cron = get_crontab()
    tasks = [job.command for job in cron]

    if not tasks:
        put_text("没有可删除的任务")
        return

    to_delete = select("选择要删除的任务", tasks)
    cron.remove_all(command=to_delete)
    cron.write()

    put_success("任务删除成功!")

if __name__ == '__main__':
    start_server(main, port=8080)