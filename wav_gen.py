from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import info as session_info
import time

samplerates= [
    8000,
    22100,
    44100,
    48000,
    96000,
    19200,
]
def check_time_len(time_len):
    if time_len > 60 or time_len < 1:
        return '时长只能是1到60秒之间'
def generate_wav(channel_num, format, samplerate, wave_shape, time_len):
    print(f"begin genrate {session_info.user_agent}")
    put_text(f"begin genrate {session_info.user_agent}")
    time.sleep(10)
    print(f"end genrate {session_info.user_agent}")
    put_text(f"end genrate {session_info.user_agent}")
def main():
    put_markdown("## wav生成工具")
    audio_info = input_group('wav param', [
        select('声道数', name='channel_num', options=[i for i in range(1,33)], value=2),
        select('格式', name='format', options=['S8', 'S16_LE', 'S32_LE'], value='S32_LE'),
        select('采样率', name='samplerate', options=samplerates, value=48000),
        select('波形', name='wave_shape', options=['全部正弦波', '全部静音', '奇数正弦波，偶数静音', '偶数正弦波，奇数静音'], value='全部正弦波'),
        input('时长', name='time_len',type=NUMBER, value=10, help_text='范围1到60秒', validate=check_time_len )
    ])
    # put_text(f'{audio_info["channel_num"]}')
    # get info to generate wave
    generate_wav(audio_info["channel_num"], audio_info["format"], audio_info["samplerate"],
        audio_info["wave_shape"], audio_info["time_len"])
if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
