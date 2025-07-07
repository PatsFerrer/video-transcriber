import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import INPUT_DIR, OUTPUT_DIR, WHISPER_MODEL_SIZE
from ffmpeg_setup import setup_ffmpeg
from transcription.video_processor import VideoProcessor
from evaluation.interview_evaluator import InterviewEvaluator


def main():
    setup_ffmpeg()

    # Lista todos os vídeos na pasta input
    videos = [f for f in os.listdir(INPUT_DIR) if f.endswith((".mp4", ".avi", ".mov"))]

    if not videos:
        print("Nenhum vídeo encontrado na pasta 'input'!")
        print(
            "Por favor, adicione arquivos de vídeo (.mp4, .avi, .mov) na pasta 'input'"
        )
        print(
            "O nome do arquivo deve seguir o padrão: candidato_nome_cargo_q{numero}.mp4"
        )
        print("Exemplo: candidato_joao_frontend_q1.mp4")
        return

    # Inicializa o avaliador
    evaluator = InterviewEvaluator()

    for video in videos:
        print(f"\nProcessando vídeo: {video}")
        video_path = os.path.join(INPUT_DIR, video)

        # Cria uma instância do processador de vídeo
        processor = VideoProcessor(
            video_path, OUTPUT_DIR, model_size=WHISPER_MODEL_SIZE
        )

        try:
            # Processa o vídeo e obtém a transcrição
            result = processor.process_video(capture=True)
            print(f"\nTranscrição concluída!")

            # Avalia a entrevista usando a transcrição diretamente
            print("\nAvaliando respostas...")
            evaluation_path = evaluator.evaluate_interview(
                video_filename=video,
                transcription=result["transcription"],
                output_dir=OUTPUT_DIR,
            )

            if evaluation_path:
                print(f"\nAvaliação concluída e salva em: {evaluation_path}")
            else:
                print("\nErro ao avaliar a entrevista.")

            if result["frames"]:
                print(f"\nFrames salvos em: {OUTPUT_DIR}")
                print(f"Número de frames capturados: {len(result['frames'])}")

        except Exception as e:
            print(f"Erro ao processar o vídeo {video}: {str(e)}")


if __name__ == "__main__":
    main()
