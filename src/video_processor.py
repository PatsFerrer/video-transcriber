import os
from moviepy.editor import VideoFileClip

import whisper
from datetime import datetime

class VideoProcessor:
    def __init__(self, input_path: str, output_dir: str):
        """
        Inicializa o processador de vídeo.

        Args:
            input_path: Caminho do arquivo de vídeo
            output_dir: Diretório para salvar os resultados
        """
        self.input_path = input_path
        self.output_dir = output_dir
        print("Carregando modelo de transcrição...")
        self.model = whisper.load_model(
            "small"
        )  # Usando o modelo small que é bom e rápido

    def extract_audio(self) -> str:
        """
        Extrai o áudio do vídeo e salva como arquivo temporário.

        Returns:
            str: Caminho do arquivo de áudio extraído
        """
        video = VideoFileClip(self.input_path)
        if video.audio is None:
            raise Exception("O vídeo não contém áudio!")

        audio_path = os.path.join(self.output_dir, "temp_audio.mp3")
        video.audio.write_audiofile(audio_path)
        video.close()
        return audio_path

    def transcribe_audio(self, audio_path: str) -> dict:
        """
        Transcreve o áudio para texto usando Whisper.

        Args:
            audio_path: Caminho do arquivo de áudio

        Returns:
            dict: Resultado da transcrição com timestamps
        """

        print("Transcrevendo áudio (pode levar alguns minutos)...")
        result = self.model.transcribe(
            audio_path, language="pt", task="transcribe", verbose=True
        )
        return result

    def save_transcription(self, transcription: dict) -> str:
        """
        Salva a transcrição em um arquivo.

        Args:
            transcription: Dicionário com a transcrição

        Returns:
            str: Caminho do arquivo de transcrição
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"transcricao_{timestamp}.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            # Salva o texto completo primeiro
            f.write("=== TRANSCRIÇÃO COMPLETA ===\n\n")
            f.write(transcription["text"])
            f.write("\n\n=== TRANSCRIÇÃO COM TIMESTAMPS ===\n\n")

            # Depois salva com timestamps
            for segment in transcription["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                f.write(f"[{start:.1f}s -> {end:.1f}s] {text}\n")

        return output_path

    def capture_frames(self, interval: int = 60) -> list:
        """
        Captura frames do vídeo em intervalos específicos.

        Args:
            interval: Intervalo em segundos entre os frames

        Returns:
            list: Lista com os caminhos dos frames salvos
        """
        video = VideoFileClip(self.input_path)
        frame_paths = []

        for t in range(0, int(video.duration), interval):
            frame = video.get_frame(t)
            frame_path = os.path.join(self.output_dir, f"frame_{t}s.jpg")
            video.save_frame(frame_path, t)
            frame_paths.append(frame_path)

        video.close()
        return frame_paths

    def process_video(self, capture_frames: bool = False) -> dict:
        """
        Processa o vídeo completo: extrai áudio, transcreve e opcionalmente captura frames.

        Args:
            capture_frames: Se True, também captura frames do vídeo

        Returns:
            dict: Resultado do processamento
        """
        audio_path = self.extract_audio()
        transcription = self.transcribe_audio(audio_path)
        transcription_path = self.save_transcription(transcription)

        result = {"transcription_path": transcription_path, "frames": None}

        if capture_frames:
            result["frames"] = self.capture_frames()

        # Limpa o arquivo de áudio temporário
        os.remove(audio_path)

        return result
