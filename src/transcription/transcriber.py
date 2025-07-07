import os
import whisper
import json

class Transcriber:
    def __init__(self, model_size: str = "small"):
        """
        Inicializa o modelo Whisper para transcrição.
        Args:
            model_size: Tamanho do modelo (tiny, base, small, medium, large)
        """
        print("Carregando modelo de transcrição...")
        self.model = whisper.load_model(model_size)

    def clean_transcription(self, segments) -> str:
        """
        Limpa a transcrição removendo timestamps e informações extras.
        Retorna apenas o texto transcrito.
        """
        return " ".join(segment["text"].strip() for segment in segments)

    def transcribe(self, audio_path: str) -> str:
        """
        Transcreve um arquivo de áudio para texto.
        Args:
            audio_path: Caminho do arquivo de áudio
        Returns:
            str: Texto transcrito
        """
        print("Transcrevendo áudio (pode levar alguns minutos)...")
        result = self.model.transcribe(audio_path)
        
        # Retorna apenas o texto limpo
        return self.clean_transcription(result["segments"])

    def save_transcription(self, transcription: str, output_dir: str) -> str:
        """
        Salva a transcrição em um arquivo JSON.
        Args:
            transcription: Texto transcrito
            output_dir: Diretório de saída
        Returns:
            str: Caminho do arquivo salvo
        """
        output_path = os.path.join(output_dir, "transcription.json")
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"transcription": transcription}, f, ensure_ascii=False, indent=2)
            
        return output_path
