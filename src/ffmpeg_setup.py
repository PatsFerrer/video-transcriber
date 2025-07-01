import os
import sys

def setup_ffmpeg():
    FFMPEG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ffmpeg', 'ffmpeg.exe'))

    if not os.path.isfile(FFMPEG_PATH):
        print(f"ERRO: FFmpeg não encontrado em: {FFMPEG_PATH}")
        sys.exit(1)

    # Configura as variáveis para moviepy, whisper e outras libs
    os.environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_PATH
    os.environ["FFMPEG_BINARY"] = FFMPEG_PATH

    # Adiciona ao PATH para subprocessos (como whisper)
    ffmpeg_dir = os.path.dirname(FFMPEG_PATH)
    os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
