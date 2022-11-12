'''
总的思路是：
对128字节的e-edid进行解析并展示。
初步想法是，展示到表格里。
生成8行16列的表格。
对于属于同一个含义的字节进行同一种颜色的着色。
在软件点击上属于同一个组。
点击同一个着色的部分，弹出显示详细解释。（可以弹窗里再绘制一个表格）
自动计算最后一个字节的校验码。

里面的数据块分为几种：
audio data block
video data block
user specific tag data block
speaker allocation data block
vendor specific data block
user extended tag
每个block都可能有多个。

这是一组合法的edid。准确来说是e-edid。
02 03 78 F0 5F 90 01 02 03 04 05 5D 5E 5F 60 61
62 63 64 65 66 75 76 7D 7E C2 C3 C4 C6 C7 06 07
11 12 13 14 48 15 16 1F 20 21 22 3F 40 38 0F 7F
07 17 07 50 3F 7F C0 57 7F 03 5F 7F 03 5F 7F 01
67 7F 03 4F 7F 00 83 01 00 00 77 03 0C 00 10 00
B8 3C 2F C8 6A 01 03 04 81 41 00 16 06 08 00 56
58 00 67 D8 5D C4 01 78 80 63 E5 0F 00 C6 FF 01
E3 05 E3 01 E3 06 07 01 00 00 00 00 00 00 00 F8

先解决表格显示。
再解决着色。
再解决点击。

表格显示很简单。
输入是一个textaera
只接受128字节的输入。
每个部分都是2位的数字，高位补零。
就用put_table来输出。
输出ok了。

下面看着色。
怎么给指定表格着色呢？

这个只能借助js来操作表格元素了。
首先要看pywebio怎么调用js代码。

首先要js可以拿到table元素。
怎么拿到呢？目前看生成的html里，table没有id之类的。
scope不能作为id来使用。根本没有体现在生成的html代码。

找到方式了。
就用jquery来获取表格元素，并进行设置。
设置值：
table.rows[0].cells[0].innerHTML = '表头';

设置颜色：
table.rows[0].cells[0].style.backgroundColor = 'red';

添加hover事件
$(table.rows[0].cells[0]).hover(function() {
                console.log('hello hover');
            });
添加点击事件
$(table.rows[0].cells[0]).click(function() {
                console.log('hello click');
            });
该有的功能都摸索了。
现在应该开始实现功能。
首先是对可以确定的表格进行着色。
首先是前面2个。

'''
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import info as session_info, eval_js

import time

default_edid = """
02 03 78 F0 5F 90 01 02 03 04 05 5D 5E 5F 60 61
62 63 64 65 66 75 76 7D 7E C2 C3 C4 C6 C7 06 07
11 12 13 14 48 15 16 1F 20 21 22 3F 40 38 0F 7F
07 17 07 50 3F 7F C0 57 7F 03 5F 7F 03 5F 7F 01
67 7F 03 4F 7F 00 83 01 00 00 77 03 0C 00 10 00
B8 3C 2F C8 6A 01 03 04 81 41 00 16 06 08 00 56
58 00 67 D8 5D C4 01 78 80 63 E5 0F 00 C6 FF 01
E3 05 E3 01 E3 06 07 01 00 00 00 00 00 00 00 F8
"""

'''
这个转十六进制，2位，高位补零。
参考这个：
https://stackoverflow.com/questions/12638408/decorating-hex-function-to-pad-zeros
'''
def hexstr(num):
    return '0x{0:0{1}X}'.format(num,2)
def main():
    put_markdown("## EDID含义自动解析")
    edid = textarea(label='输入128字节的EDID', value=default_edid, required=True)
    edid = edid.split()
    edid_arr = []
    for val in edid:
        edid_arr.append(int(val, base=16))
    
    put_table([
        [' '] + [hexstr(i) for i in range(0, 16)],
        ['0x00'] + [ hexstr(i) for i in edid_arr[0:16]],
        ['0x01'] + [ hexstr(i) for i in edid_arr[16:32]],
        ['0x02'] + [ hexstr(i) for i in edid_arr[32:48]],
        ['0x03'] + [ hexstr(i) for i in edid_arr[48:64]],
        ['0x04'] + [ hexstr(i) for i in edid_arr[64:80]],
        ['0x05'] + [ hexstr(i) for i in edid_arr[80:96]],
        ['0x06'] + [ hexstr(i) for i in edid_arr[96:112]],
        ['0x07'] + [ hexstr(i) for i in edid_arr[112:128]],
    ])
    # 操作table元素
    # https://blog.csdn.net/liuzhenhe1988/article/details/112346025
    # https://zhuanlan.zhihu.com/p/31798692
    eval_js('''
        $(document).ready(function() {
            console.log("jquery the doc is ready");
            // get the table
            var table = $("table")[0];
            
            //着色就按照赤橙黄绿青蓝紫的循序来给吧。
            //所以edid[0], edid[1]就给red和orange。
            // 我的表格，都要从1开始数。
            //$(table.rows[1].cells[1]).css('color', 'red);
            //$(table.rows[1].cells[1])[0]
            console.log($(table.rows[1].cells[1]) )

        })
        
    ''')
if __name__ == '__main__':
    start_server(main, debug=True, port=8080)