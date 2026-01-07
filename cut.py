from scipy.io.wavfile import read
from scipy.signal import spectrogram
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import librosa
import time
import soundfile as sf
import os
import sys
import struct
import io
import sounddevice as sd
from queue import Queue, Empty
import argparse

# フーリエ変換をする関数
def calc_fft(data, samplerate):
    spectrum = fftpack.fft(data)                                     # 信号のフーリエ変換
    amp = np.sqrt((spectrum.real ** 2) + (spectrum.imag ** 2))       # 振幅成分
    amp = amp / (len(data) / 2)                                      # 振幅成分の正規化（辻褄合わせ）
    phase = np.arctan2(spectrum.imag, spectrum.real)                 # 位相を計算
    phase = np.degrees(phase)                                        # 位相をラジアンから度に変換
    freq = np.linspace(0, samplerate, len(data))                     # 周波数軸を作成
    return spectrum, amp, phase, freq

# 指定した時間窓での最大音量周波数を取得する関数
def get_max_frequency(data_segment, samplerate):
    if len(data_segment) == 0:
        return 0, 0
    
    spectrum, amp, phase, freq = calc_fft(data_segment, samplerate)
    
    # ナイキスト周波数まで（正の周波数のみ）
    half_len = len(amp) // 2
    amp_positive = amp[:half_len]
    freq_positive = freq[:half_len]
    
    # 最大振幅のインデックスを取得
    max_idx = np.argmax(amp_positive)
    max_freq = freq_positive[max_idx]
    max_amp = amp_positive[max_idx]
    
    return max_freq, max_amp

# コマンドライン引数の処理
parser = argparse.ArgumentParser(description='マイク入力をリアルタイム分析し、検出後にedited_pipeに送信')
parser.add_argument('-l', '--listdevices', action='store_true', help='利用可能なデバイス一覧を表示')
parser.add_argument('-d', '--device', type=int, default=None, help='sounddeviceの入力デバイス番号')
parser.add_argument('-p', '--pnum', type=int, default=None, help='出力パイプの末尾に付加する番号')
parser.add_argument('-r', '--rate', type=int, default=44100, help='サンプリングレート (Hz)')
parser.add_argument('-c', '--channels', type=int, default=1, help='チャンネル数')
args = parser.parse_args()

# デバイス一覧表示
if args.listdevices:
    devices = sd.query_devices()
    print('利用可能な音声入力デバイス:')
    for idx, dev in enumerate(devices):
        if dev.get('max_input_channels', 0) > 0:
            print(f'{idx}: {dev.get("name")} (in: {dev.get("max_input_channels")})')
    sys.exit(0)

save_path = f'media/rec_pipe{args.pnum if args.pnum is not None else ""}.wav'
samplerate = args.rate
channels = args.channels

print(f"音声情報:")
print(f"  チャンネル数: {channels}")
print(f"  サンプリングレート: {samplerate} Hz")

# 分析パラメータ
window_duration = 0.01  # 分析する時間窓（秒）
step_duration = 0.01    # ステップ間隔（秒）
window_samples = int(samplerate * window_duration)
step_samples = int(samplerate * step_duration)

print(f"\n分析パラメータ:")
print(f"分析窓: {window_duration} 秒")
print(f"ステップ間隔: {step_duration} 秒")
print("-" * 50)

# 検出状態
detected = False
buffer = []
time_counter = 0
all_data = []  # 保存用

# edited_pipeを開く準備（パイプ番号指定時のみ末尾に付加）
if args.pnum is not None:
    pipe_path = f'edited_pipe{args.pnum}'
else:
    pipe_path = 'edited_pipe'
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)
    print(f"named pipe作成: {pipe_path}")

output_pipe = None

# 録音用キュー
q = Queue()

def callback(indata, frames, time_info, status):
    if status:
        print(f'InputStream status: {status}', file=sys.stderr)
    q.put(indata.copy())

try:
    print(f'録音開始: rate={samplerate} Hz, channels={channels}, device={args.device}')
    print('録音中 (Ctrl+C で停止)...')
    
    with sd.InputStream(samplerate=samplerate, channels=channels, dtype='int16', 
                        callback=callback, device=args.device, blocksize=step_samples):
        while True:
            try:
                # データを取得
                indata = q.get(timeout=1)
                
                # モノラルに変換
                if channels == 2:
                    audio_chunk = indata.mean(axis=1)
                else:
                    audio_chunk = indata.flatten()
                
                buffer.extend(audio_chunk)
                
                # 分析用のデータが溜まったら分析
                if len(buffer) >= window_samples:
                    # 分析用データを取得
                    analysis_data = np.array(buffer[:window_samples], dtype=np.int16)
                    
                    # 正規化
                    audio_array = analysis_data.astype(np.float32) / np.iinfo(np.int16).max
                    
                    # 最大音量の周波数を取得
                    max_freq, max_amp = get_max_frequency(audio_array, samplerate)
                    
                    # 検出判定
                    if not detected and 1996 < max_freq < 2005:
                        print(f"time: {time_counter:3.1f}秒 | "
                              f"maxdB_freq: {max_freq:8.2f} Hz | "
                              f"振幅: {max_amp:8.4f}")
                        print(f"--> 検出! {time_counter:3.3f} 秒で検出。パイプへの送信を開始します。")
                        detected = True
                        
                        # パイプをオープン
                        output_pipe = open(pipe_path, 'wb')
                        
                        # WAVヘッダーを作成して送信
                        bio = io.BytesIO()
                        buffer_array = np.array(buffer, dtype=np.int16)
                        sf.write(bio, buffer_array.astype(np.float32) / np.iinfo(np.int16).max, 
                                samplerate, format='WAV', subtype='PCM_16')
                        bio.seek(0)
                        wav_header = bio.read(44)
                        
                        # データサイズを最大値に設定
                        temp_header = bytearray(wav_header)
                        struct.pack_into('<I', temp_header, 40, 0xFFFFFFFF - 44)
                        output_pipe.write(temp_header)
                        output_pipe.flush()
                        
                        # バッファ内のデータを送信
                        output_pipe.write(buffer_array.tobytes())
                        output_pipe.flush()
                        all_data.extend(buffer)
                        
                    elif detected:
                        # 検出後は受信データをそのままパイプに送信
                        send_samples = buffer[:step_samples]
                        send_array = np.array(send_samples, dtype=np.int16)
                        output_pipe.write(send_array.tobytes())
                        output_pipe.flush()
                        all_data.extend(send_samples)
                    
                    # バッファをスライド
                    buffer = buffer[step_samples:]
                    time_counter += step_duration
                    
            except Empty:
                continue
                
except KeyboardInterrupt:
    print('\nユーザー割り込み: 録音を停止します')
except Exception as e:
    print(f"エラー: {e}")
    import traceback
    traceback.print_exc()
finally:
    if output_pipe:
        output_pipe.close()
        print(f"named_pipeへの送信完了")
    
    # 保存用データの処理
    if detected and all_data:
        all_audio = np.array(all_data, dtype=np.int16)
        all_audio = all_audio.astype(np.float32) / np.iinfo(np.int16).max
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        sf.write(save_path, all_audio, samplerate)
        print(f"切り取り後の音声を {save_path} に保存しました。長さ: {len(all_audio) / samplerate:.2f} 秒")
    elif not detected:
        print("検出されませんでした。条件やしきい値を調整してください。")

print("-" * 50)
print("処理完了")