
from pywebio.output import put_markdown, put_row, put_html


index_md = r"""
# 我的一些实用小工具
- [wav文件生成](./wav_gen): 生成任意格式的wav文件，用于硬件和开发测试
- [EDID解析](./edid_parse): 输入一段edid，自动解析其含义
- [typocheck整理](./typo_helper): 整理公司typocheck检测出的拼写错误。
"""

def main():
    put_markdown(index_md)
