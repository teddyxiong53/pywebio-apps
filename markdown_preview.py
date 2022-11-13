from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import download, set_env

def main():
    set_env(output_animation=False)
    put_markdown("""
    # write your markdown here

    """)
    put_textarea('md_text', rows=18, code={
        'mode': 'markdown'
    })
    put_markdown('## preview')
    while True:
        change_detail = pin_wait_change('md_text')
        with use_scope('md', clear=True):
            put_markdown(change_detail['value'], sanitize=False)
if __name__ == '__main__':
    start_server(main, debug=True, port=8080)