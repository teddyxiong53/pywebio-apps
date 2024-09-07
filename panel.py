from pywebio import start_server
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env

def main():
    set_env(output_animation=False)
    
    put_html("""
    <style>
        .custom-title { font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #333; }
        .custom-subtitle { font-size: 18px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #444; }
        .custom-table { width: 100%; border-collapse: collapse; }
        .custom-table td, .custom-table th { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .custom-table th { background-color: #f2f2f2; }
        .status-item { text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }
        .status-value { font-size: 24px; font-weight: bold; color: #007bff; }
        .status-label { font-size: 14px; color: #6c757d; }
        .app-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .app-item { display: flex; align-items: center; background-color: #f8f9fa; padding: 10px; border-radius: 5px; }
        .app-icon { width: 40px; height: 40px; margin-right: 10px; }
        .app-name { flex-grow: 1; }
        .install-btn { background-color: #28a745; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; }
    </style>
    """)

    put_row([
        put_column([
            put_html('<h1 style="text-align: center; color: #007bff;">1Panel</h1>'),
            put_html('<h2 style="margin-top: 20px;">菜单</h2>'),
            put_text("概览").style('cursor: pointer; padding: 5px; background-color: #e9ecef;'),
            put_text("应用商店").style('cursor: pointer; padding: 5px;'),
            put_text("网站").style('cursor: pointer; padding: 5px;'),
            put_text("数据库").style('cursor: pointer; padding: 5px;'),
            put_text("文件").style('cursor: pointer; padding: 5px;'),
            put_text("面板设置").style('cursor: pointer; padding: 5px;'),
            put_text("退出登录").style('cursor: pointer; padding: 5px; color: red;'),
        ], size='20%'),
        put_column([
            put_row([
                put_html('<h2 style="margin: 0;">概览</h2>'),
                None,
                put_text("重启面板 | 重启服务器").style('color: #007bff; cursor: pointer;')
            ]),
            put_html('<h3 class="custom-subtitle">统计</h3>'),
            put_table([
                ['网站', '数据库', '计划任务', '已安装应用'],
                ['8', '10', '6', '6']
            ]).style('width: 100%; border-collapse: collapse;'),
            
            put_html('<h3 class="custom-subtitle">状态</h3>'),
            put_row([
                put_column([put_html('<div class="status-value">2.77%</div>'), put_html('<div class="status-label">CPU</div>')]).style('text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'),
                put_column([put_html('<div class="status-value">23.02%</div>'), put_html('<div class="status-label">内存</div>')]).style('text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'),
                put_column([put_html('<div class="status-value">3.67%</div>'), put_html('<div class="status-label">负载</div>')]).style('text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'),
                put_column([put_html('<div class="status-value">8.87%</div>'), put_html('<div class="status-label">/</div>')]).style('text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'),
            ]),
            
            put_html('<h3 class="custom-subtitle">监控</h3>'),
            put_image('https://via.placeholder.com/800x200.png?text=监控图表'),
            
            put_html('<h3 class="custom-subtitle">系统信息</h3>'),
            put_table([
                ['主机名称', 'uZf8banvZ7n94hbxe7mcZ'],
                ['发行版本', 'ubuntu-22.04'],
                ['内核版本', '5.15.0-92-generic'],
                ['系统架构', 'x86_64'],
                ['启动时间', '2024-02-20 10:59:20'],
                ['运行时间', '7天 5小时 43分 37秒']
            ]).style('width: 100%; border-collapse: collapse;'),
            
            put_html('<h3 class="custom-subtitle">推荐应用</h3>'),
            put_html('''
            <div class="app-grid">
                <div class="app-item">
                    <img src="https://via.placeholder.com/40x40.png?text=OR" class="app-icon">
                    <span class="app-name">OpenResty</span>
                    <button class="install-btn">安装</button>
                </div>
                <div class="app-item">
                    <img src="https://via.placeholder.com/40x40.png?text=MySQL" class="app-icon">
                    <span class="app-name">MySQL</span>
                    <button class="install-btn">安装</button>
                </div>
                <div class="app-item">
                    <img src="https://via.placeholder.com/40x40.png?text=Halo" class="app-icon">
                    <span class="app-name">Halo</span>
                    <button class="install-btn">安装</button>
                </div>
            </div>
            '''),
            
            put_html('<hr>'),
            put_row([
                put_text("Copyright © 2014-2024 FIT2CLOUD 飞致云").style('color: #6c757d; font-size: 12px;'),
                None,
                put_text("论坛 | 文档 | 项目地址 | 当前运行版本: v1.10.0-lts (检查更新)").style('color: #6c757d; font-size: 12px;')
            ])
        ], size='80%')
    ])

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)