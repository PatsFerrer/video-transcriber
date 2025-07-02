import os
from transcription.audio_extractor import extract_audio
from transcription.frame_capture import capture_frames
from transcription.transcriber import Transcriber

class VideoProcessor:
    def __init__(self, input_path: str, output_dir: str, model_size: str = "small"):
        """
        Inicializa o processador de vídeo.

        Args:
            input_path: Caminho do arquivo de vídeo
            output_dir: Diretório para salvar os resultados
            model_size: Tamanho do modelo de transcrição
        """
        self.input_path = input_path
        self.output_dir = output_dir
        self.transcriber = Transcriber(model_size)

    def process_video(self, capture: bool = False) -> dict:
        """
        Processa o vídeo completo: extrai áudio, transcreve e opcionalmente captura frames.

        Args:
            capture_frames: Se True, também captura frames do vídeo

        Returns:
            dict: Resultado do processamento
        """
        audio_path = extract_audio(self.input_path, self.output_dir)
        transcription = self.transcriber.transcribe(audio_path)
        transcription_path = self.transcriber.save_transcription(
            transcription, self.output_dir
        )

        result = {"transcription_path": transcription_path, "frames": None}

        if capture:
            result["frames"] = capture_frames(self.input_path, self.output_dir)

        os.remove(audio_path)
        return result
