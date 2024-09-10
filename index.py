
from pywebio.output import put_markdown, put_row, put_html


index_md = r"""
# 我的一些实用小工具
- [wav文件生成](./wav_gen): 生成任意格式的wav文件，用于硬件和开发测试
- [EDID解析](./edid_parse): 输入一段edid，自动解析其含义
- [mac地址申请](./mac_apply): 管理公司内部的mac地址申请。做到不重不漏。
- [mac地址申请记录查看](./mac_view): 查看mac地址申请记录。
- [京东脚本](./jd_script): 进行jd脚本的管理。
- [sqlite操作](./sqlite): 进行sqlite的管理。
- [panel](./panel): 一个panel界面，方便后面根据这个来改。
- [blog](./blog): 一个简单的博客系统，通过跟cursor对话来生成的。这个AI工具真的很强大了。
- [cron_edit](./cron_edit): 一个简单的cron编辑器，可以方便的添加、删除、编辑cron任务。
"""

def main():
    put_markdown(index_md)
