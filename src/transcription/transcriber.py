import whisper
import os
from datetime import datetime

class Transcriber:
    def __init__(self, model_size: str = "small"):
        print("Carregando modelo de transcrição...")
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcreve o áudio para texto usando Whisper.
        """
        print("Transcrevendo áudio (pode levar alguns minutos)...")
        result = self.model.transcribe(
            audio_path, language="pt", task="transcribe", verbose=True
        )
        return result

    def save_transcription(self, transcription: dict, output_dir: str) -> str:
        """
        Salva a transcrição em um arquivo.
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"transcricao_{timestamp}.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=== TRANSCRIÇÃO COMPLETA ===\n\n")
            f.write(transcription["text"])
            f.write("\n\n=== TRANSCRIÇÃO COM TIMESTAMPS ===\n\n")

            for segment in transcription["segments"]:
                start = segment["start"]
                end = segment["end"]
                text = segment["text"]
                f.write(f"[{start:.1f}s -> {end:.1f}s] {text}\n")

        return output_path
