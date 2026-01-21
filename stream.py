import subprocess
import os
import sys
import argparse
import cv2
import sys
import sounddevice as sd

# 引数の処理
parser = argparse.ArgumentParser(description='FFmpeg HLSストリーミング')
parser.add_argument('-l', '--listdevices', action='store_true', help='デバイス一覧を表示')
parser.add_argument('-d', '--dnum', type=int, default=0, help='ビデオ入力デバイス番号')
parser.add_argument('-v', '--video', action='store_true', help='streamをビデオ入力に切り替え')
parser.add_argument('-p', '--pnum', type=int, default=None, help='入力パイプの末尾の番号')
args = parser.parse_args()

#デバイス一覧
ffmpeg_devices = [
     'ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i', ''
]

# -d オプションが指定された場合はデバイス一覧を表示して終了
if args.listdevices:
  devices = sd.query_devices()
  print('利用可能な入力デバイス:')
  for idx, dev in enumerate(devices):
    if dev.get('max_input_channels', 0) > 0:
       print(f'{idx}: {dev.get("name")} (in: {dev.get("max_input_channels")})')
  print('利用可能なカメラデバイス: ')
  # カメラデバイスをスキャン（通常0-10程度で十分）
  max_tested = 6
  for idx in range(max_tested):
      cap = cv2.VideoCapture(idx)
      if cap.isOpened():
        # デバイス名の取得を試みる（プラットフォーム依存）
        backend = cap.getBackendName()
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        print(f'{idx}: Camera {idx} ({backend}) - {width}x{height} @ {fps}fps')
        cap.release()
  sys.exit(0)


if args.video:
    media = 'video'
else:
    media = 'audio'

if args.dnum is not None:
   device_num = args.dnum

   
# 入力パイプ（パイプ番号指定時のみ末尾に付加）
if args.pnum is not None:
    path = f'edited_pipe{args.pnum}'
else:
    path = 'edited_pipe'

# 出力ディレクトリ
output_dir = f'/Users/shike/git/audiozoom/live/audio{args.pnum if args.pnum is not None else ""}'
os.makedirs(output_dir, exist_ok=True)


# ffmpegコマンド
ffmpeg_cmd = [
    'ffmpeg',
    '-i', path,
    '-acodec', 'aac',
    '-thread_queue_size', '16384',
    '-f', 'hls',
    '-hls_time', '6',
    '-hls_list_size', '5',
    '-hls_delete_threshold', '2',
    '-hls_flags', 'delete_segments',
    '-hls_segment_filename', f'{output_dir}/audio%04d.ts',
    f'{output_dir}/audio.m3u8'
]

ffmpeg_video = [
  'ffmpeg',
  '-framerate', '30.000000',
  '-f', 'avfoundation',
  '-pix_fmt', 'uyvy422',
  '-thread_queue_size', '8192',
  '-i', f'{args.dnum}', '-vcodec', 'libx264',
   '-preset', 'ultrafast',
  '-tune', 'zerolatency',
  '-vsync', 'cfr', '-r', '30', '-g', '30',
  '-f', 'hls', '-hls_time', '3', '-hls_list_size', '5', '-hls_delete_threshold', '2', '-hls_flags', 'delete_segments',
  '-hls_segment_filename', f'/Users/shike/git/audiozoom/live/video/video%4d.ts',
  '/Users/shike/git/audiozoom/live/video/video.m3u8'
]

# ffmpeg_cmd = [
#     'ffmpeg',
#     '-framerate', '30.000000',
#     '-f', 'avfoundation',
#     '-pix_fmt', 'uyvy422',
#     '-thread_queue_size', '8192',
#     '-i', '0:2',
#     '-vcodec', 'libx264',
#     '-vf', 'crop=1552:873:0:339',
#     '-preset', 'ultrafast',
#     '-tune', 'zerolatency',
#     '-vsync', 'cfr',
#     '-r', '30',
#     '-g', '30',
#     '-acodec', 'aac',
#     '-f', 'hls',
#     '-hls_time', '4',
#     '-hls_list_size', '5',
#     '-hls_delete_threshold', '2',
#     '-hls_flags', 'delete_segments',
#     '-hls_segment_filename', f'{output_dir}/video%04d.ts',
#     f'{output_dir}/output.m3u8'
# ]

# -hls_time was 1 or 4 or 5 or 11
# -hls_list_size was 3 - 5
# -hls_delete_threshold was 2 - 3
# -hls_playlist_type event

print('HLSストリーム開始\n')
print(f'出力先: {output_dir}/{media}.m3u8\n')

try:
    # ffmpegプロセスを実行
    process = subprocess.run(ffmpeg_cmd if not args.video else ffmpeg_video)
    sys.exit(process.returncode)
except KeyboardInterrupt:
    print('\n\nストリーミング停止')
    sys.exit(0)
except Exception as e:
    print(f'\nエラー: {e}')
    sys.exit(1)


