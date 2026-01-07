import numpy as np
import sounddevice as sd
import time

def play_sine_wave(frequency, duration=0.5, sample_rate=44100, amplitude=0.3):
    """
    指定された周波数の正弦波を再生する
    
    Args:
        frequency (float): 再生する周波数 (Hz)
        duration (float): 再生時間 (秒)
        sample_rate (int): サンプリングレート
        amplitude (float): 音量 (0.0-1.0)
    """
    # 時間軸を作成
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # 正弦波を生成
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # 音声を再生
    sd.play(wave, sample_rate)
    sd.wait()  # 再生完了まで待機

def main(duration=1.0):
    print("周波数を入力してください (終了するには 'q' を入力):")
    
    while True:
        user_input = input("周波数 (Hz): ")
        
        if user_input.lower() == 'q':
            print("プログラムを終了します。")
            break
        
        try:
            frequency = float(user_input)
            
            if frequency <= 0:
                print("正の数値を入力してください。")
                continue
            
            print(f"{frequency} Hzの正弦波を{duration}秒間再生します...")
            play_sine_wave(frequency)
            print("再生完了")
            
        except ValueError:
            print("有効な数値を入力してください。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    # sounddeviceがインストールされていない場合のメッセージ
    try:
        import sounddevice as sd
        main()
    except ImportError:
        print("sounddeviceライブラリが必要です。")
        print("インストールするには: pip install sounddevice")