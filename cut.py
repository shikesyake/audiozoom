from scipy.io.wavfile import read
from scipy.signal import spectrogram
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import librosa
import time
import soundfile as sf

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

# 音声ファイルを読み込む（librosaを使用）
data, samplerate = librosa.load('sample/サンプル立原.mp3', sr=None, mono=True)

# 分析パラメータ
window_duration = 0.01  # 分析する時間窓（秒）
step_duration = 0.01    # ステップ間隔（秒）
save_path = 'media/2aligned_from_detection.wav'  # 判定位置以降を書き出す先

window_samples = int(samplerate * window_duration)
step_samples = int(samplerate * step_duration)

print(f"音声ファイル情報:")
print(f"サンプリングレート: {samplerate} Hz")
print(f"総時間: {len(data) / samplerate:.2f} 秒")
print(f"分析窓: {window_duration} 秒")
print(f"ステップ間隔: {step_duration} 秒")
print("-" * 50)

# 各時間窓で分析を実行
current_pos = 0
time_counter = 0
first_detect_pos = None  # 最初に判定した窓の開始サンプル

while current_pos + window_samples <= len(data):
    # 現在の時間窓のデータを取得
    data_segment = data[current_pos:current_pos + window_samples]
    
    # 最大音量の周波数を取得
    max_freq, max_amp = get_max_frequency(data_segment, samplerate)
    
    # 結果を表示
    if 1990 < max_freq < 2010:
                print(f"time: {time_counter:3.1f} - {time_counter + window_duration:3.1f}秒 | "
                    f"maxdB_freq: {max_freq:8.2f} Hz | "
                    f"振幅: {max_amp:8.4f}")
                if first_detect_pos is None:
                        first_detect_pos = current_pos
                        print(f"--> 判定: {time_counter:3.3f} 秒で最初に検出 (サンプル {first_detect_pos})")

    # 次の位置に移動
    current_pos += step_samples
    time_counter += step_duration
    
    # リアルタイム感を出すため少し待機（オプション）
    # time.sleep(0.1)

print("-" * 50)
print("分析完了")

# 判定された最初の地点より前を削除し、残りを別ファイルに保存
if first_detect_pos is not None:
    trimmed = data[first_detect_pos:]
    sf.write(save_path, trimmed, samplerate)
    print(f"切り取りごの音声を {save_path} に保存しました。長さ: {len(trimmed) / samplerate:.2f} 秒")
else:
    print("判定不可。条件やしきい値を調整してください。")