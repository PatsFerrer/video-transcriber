from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path: str, output_dir: str) -> str:
    """
    Extrai o áudio do vídeo e salva como arquivo temporário.
    """
    video = VideoFileClip(video_path)
    if video.audio is None:
        raise Exception("O vídeo não contém áudio!")

    audio_path = os.path.join(output_dir, "temp_audio.mp3")
    video.audio.write_audiofile(audio_path)
    video.close()
    return audio_path
