import os
import platform

def setup_ffmpeg():
    sistema = platform.system().lower()  # 'windows', 'linux', 'darwin'

    if sistema == 'windows':
        subpasta = 'windows'
        ffmpeg_bin = 'ffmpeg.exe'
    elif sistema == 'linux':
        subpasta = 'linux'
        ffmpeg_bin = 'ffmpeg'
    elif sistema == 'darwin':
        subpasta = 'macos'
        ffmpeg_bin = 'ffmpeg'
    else:
        print(f"Sistema operacional não suportado: {sistema}")
        return

    projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    ffmpeg_path = os.path.join(projeto_dir, 'ffmpeg', subpasta, ffmpeg_bin)

    if not os.path.isfile(ffmpeg_path):
        print(f"ERRO: FFmpeg não encontrado em: {ffmpeg_path}")
        return

    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]

    print(f"FFmpeg configurado para: {ffmpeg_path}")
