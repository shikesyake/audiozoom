import subprocess
import os
import sys
import argparse

# 引数の処理
parser = argparse.ArgumentParser(description='FFmpeg HLSストリーミング')
parser.add_argument('-d', '--devices', action='store_true', help='デバイス一覧を表示')
args = parser.parse_args()

#デバイス一覧
ffmpeg_devices = [
     'ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''
]

# -d オプションが指定された場合はデバイス一覧を表示して終了
if args.devices:
	print('利用可能なデバイス一覧:\n')
	devices = subprocess.run(ffmpeg_devices)
	print(devices.stderr)
	sys.exit(0)


# 出力ディレクトリ
output_dir = '/Users/shike/git/audiozoom/live'
os.makedirs(output_dir, exist_ok=True)



# ffmpegコマンド
ffmpeg_cmd = [
    'ffmpeg',
    '-framerate', '30.000000',
    '-f', 'avfoundation',
    '-pix_fmt', 'uyvy422',
    '-thread_queue_size', '8192',
    '-i', '0:2',
    '-vcodec', 'libx264',
    '-vf', 'crop=1552:873:0:339',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-vsync', 'cfr',
    '-r', '30',
    '-g', '30',
    '-acodec', 'aac',
    '-f', 'hls',
    '-hls_time', '4',
    '-hls_list_size', '5',
    '-hls_delete_threshold', '2',
    '-hls_flags', 'delete_segments',
    '-hls_segment_filename', f'{output_dir}/video%04d.ts',
    f'{output_dir}/output.m3u8'
]

# -hls_time was 1 or 4 or 5 or 11
# -hls_list_size was 3 - 5
# -hls_delete_threshold was 2 - 3 
# -hls_playlist_type event 

print('HLSストリーム開始\n')
print(f'出力先: {output_dir}/output.m3u8\n')

try:
    # ffmpegプロセスを実行
    process = subprocess.run(ffmpeg_cmd)
    sys.exit(process.returncode)
except KeyboardInterrupt:
    print('\n\nストリーミング停止')
    sys.exit(0)
except Exception as e:
    print(f'\nエラー: {e}')
    sys.exit(1)


