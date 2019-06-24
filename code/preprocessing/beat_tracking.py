from __future__ import print_function
import librosa

if __name__ == "__main__":
    # 2. 波形情報を `y` へ、
    #    サンプリングレートを `sr` へ格納します。
    y, sr = librosa.load("hoge.wav")

    # 3. デフォルトの「ビートトラッカー」を実行します。
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

    # 4. ビートイベントの発生したフレーム索引をタイムスタンプ（先頭からの秒数）へ変換します。
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print('Saving output to beat_times.csv')
    librosa.output.times_csv('beat_times.csv', beat_times)
