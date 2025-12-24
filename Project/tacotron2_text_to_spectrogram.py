# tacotron2_text_to_spectrogram.py
# Mô tả: Dùng Tacotron2 (qua Coqui TTS) để chuyển văn bản -> WAV, sau đó tạo spectrogram và có thể lưu dữ liệu spectrogram (npz)
# Ghi chú cài đặt (PowerShell, Windows):
# 1) Tạo env (tuỳ chọn): python -m venv .venv; .\.venv\Scripts\Activate.ps1
# 2) Cài Coqui TTS và phụ thuộc: pip install TTS
#    - Coqui TTS sẽ tự cài các model khi gọi lần đầu (cần internet)
#    - Nếu gặp lỗi torch, cài torch phù hợp: https://pytorch.org
# 3) Cài thêm cho spectrogram: pip install librosa matplotlib numpy soundfile
# 4) Ví dụ chạy:
#    python tacotron2_text_to_spectrogram.py --text "Xin chào" --model "tts_models/en/ljspeech/tacotron2-DDC" --out spec.png --save-spec spec_data.npz

import argparse
import os
import tempfile
import shutil


def synthesize_with_tts_model(text, out_wav, model_name, speaker=None, language=None):
    """Cố gắng dùng Coqui TTS. Nếu không có, fallback về pyttsx3 hoặc gTTS.
    """
    try:
        from TTS.api import TTS
    except Exception as e:
        print("Coqui TTS không có hoặc không thể import. Sẽ thử fallback TTS (pyttsx3 -> gTTS).", e)
        fallback_tts(text, out_wav)
        return

    # Tạo instance TTS. Lần đầu sẽ tự tải model về máy nếu chưa có.
    print(f"Khởi tạo TTS model: {model_name} ...")
    tts = TTS(model_name)
    # tts.tts_to_file hỗ trợ nhiều tham số, ta chỉ gọi đơn giản
    try:
        tts.tts_to_file(text=text, file_path=out_wav, speaker=speaker, language=language)
    except TypeError:
        # Một số phiên bản API không chấp nhận speaker/language nếu None
        tts.tts_to_file(text=text, file_path=out_wav)


def fallback_tts(text, out_wav):
    """Thử sinh WAV bằng pyttsx3 (offline). Nếu không có, thử gTTS + pydub (online).
    Nếu cả hai đều không có, ném lỗi hướng dẫn cài đặt.
    """
    # 1) Thử pyttsx3 (offline, Windows SAPI)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, out_wav)
        engine.runAndWait()
        print(f"Đã tạo WAV bằng pyttsx3: {out_wav}")
        return
    except Exception as e:
        print("pyttsx3 không khả dụng hoặc lỗi chạy:", e)

    # 2) Thử gTTS + pydub (cần ffmpeg trên PATH)
    try:
        from gtts import gTTS
        from pydub import AudioSegment
    except Exception as e:
        print("gTTS hoặc pydub không khả dụng:", e)
        raise RuntimeError("Không có Coqui TTS, pyttsx3 hoặc gTTS/pydub. Cài: pip install TTS pyttsx3 gTTS pydub") from e

    # gTTS tạo mp3 rồi convert sang wav
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
        tmp_mp3 = tmp.name
    try:
        tts = gTTS(text, lang='vi')
        tts.save(tmp_mp3)
        audio = AudioSegment.from_file(tmp_mp3, format='mp3')
        audio.export(out_wav, format='wav')
        print(f"Đã tạo WAV bằng gTTS: {out_wav}")
    finally:
        try:
            os.remove(tmp_mp3)
        except Exception:
            pass


def make_spectrogram(wav_path, out_image, show_plot=True, dpi=150, save_npz=None):
    try:
        import librosa
        import librosa.display
        import numpy as np
        import matplotlib.pyplot as plt
    except Exception as e:
        raise RuntimeError("Thiếu librosa/matplotlib/numpy. Cài: pip install librosa matplotlib numpy") from e

    y, sr = librosa.load(wav_path, sr=None)
    if y.size == 0:
        raise RuntimeError("Audio rỗng hoặc không đọc được.")

    n_fft = 2048
    hop_length = 512
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_mag = np.abs(S)
    S_db = librosa.amplitude_to_db(S_mag, ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='hz', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram (dB)')
    plt.tight_layout()
    plt.savefig(out_image, dpi=dpi)

    if save_npz:
        try:
            np.savez(save_npz, S_mag=S_mag, sr=sr, n_fft=n_fft, hop_length=hop_length)
            print(f"Saved spectrogram data to {save_npz} (magnitude + metadata).")
        except Exception as e:
            print("Không lưu được spectrogram data:", e)

    if show_plot:
        plt.show()
    plt.close()


def spectrogram_to_audio(npz_path, out_wav, n_iter=60):
    try:
        import numpy as np
        import librosa
        import soundfile as sf
    except Exception as e:
        raise RuntimeError("Thiếu numpy/librosa/soundfile. Cài: pip install numpy librosa soundfile") from e

    data = np.load(npz_path)
    S_mag = data['S_mag']
    sr = int(data['sr'])
    n_fft = int(data['n_fft'])
    hop_length = int(data['hop_length'])

    y = librosa.griffinlim(S_mag, n_iter=n_iter, hop_length=hop_length, win_length=n_fft)
    sf.write(out_wav, y, sr)
    print(f"Reconstructed audio saved to {out_wav}")


def play_wav(wav_path):
    try:
        import simpleaudio as sa
    except Exception as e:
        print("simpleaudio chưa cài, bỏ qua phát âm thanh. Cài: pip install simpleaudio")
        return
    try:
        wave_obj = sa.WaveObject.from_wave_file(wav_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print("Không phát được audio:", e)


def main():
    parser = argparse.ArgumentParser(description='Text -> Tacotron2 TTS -> Spectrogram')
    parser.add_argument('--text', '-t', type=str, help='Văn bản cần chuyển thành âm thanh (nên đặt trong dấu ngoặc kép).')
    parser.add_argument('--model', '-m', default='tts_models/en/ljspeech/tacotron2-DDC', help='Tên model Tacotron2 của Coqui TTS (ví dụ).')
    parser.add_argument('--speaker', help='Speaker id nếu model multi-speaker (tuỳ model).')
    parser.add_argument('--language', help='Ngôn ngữ nếu cần (tuỳ model).')
    parser.add_argument('--out', '-o', default='spectrogram.png', help='Tên file ảnh spectrogram (PNG).')
    parser.add_argument('--play', action='store_true', help='Phát âm thanh sau khi tạo (tùy vào simpleaudio).')
    parser.add_argument('--save-spec', '-s', help='Lưu dữ liệu spectrogram (npz) để phục hồi âm thanh sau này.')
    args = parser.parse_args()

    if not args.text:
        args.text = input('Nhập văn bản muốn chuyển thành spectrogram: ').strip()

    temp_dir = tempfile.mkdtemp(prefix='tacotron2_')
    try:
        wav_path = os.path.join(temp_dir, 'out.wav')
        print('Synthesize with Tacotron2 model...')
        synthesize_with_tts_model(args.text, wav_path, model_name=args.model, speaker=args.speaker, language=args.language)

        if not os.path.isfile(wav_path):
            raise RuntimeError('Không tạo được file WAV.')

        print('Tạo spectrogram...')
        make_spectrogram(wav_path, args.out, show_plot=True, save_npz=args.save_spec)
        print(f'Đã lưu spectrogram: {args.out}')

        if args.play:
            print('Phát âm thanh...')
            play_wav(wav_path)
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass

if __name__ == '__main__':
    main()
