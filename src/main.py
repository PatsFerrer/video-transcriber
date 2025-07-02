import os
import sys
# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import INPUT_DIR, OUTPUT_DIR, WHISPER_MODEL_SIZE
from ffmpeg_setup import setup_ffmpeg
from transcription.summarizer import summarize_text
from transcription.video_processor import VideoProcessor

def main():
    setup_ffmpeg()
    
    # Lista todos os vídeos na pasta input
    videos = [f for f in os.listdir(INPUT_DIR) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    if not videos:
        print("Nenhum vídeo encontrado na pasta 'input'!")
        print("Por favor, adicione arquivos de vídeo (.mp4, .avi, .mov) na pasta 'input'")
        return
    
    for video in videos:
        print(f"\nProcessando vídeo: {video}")
        video_path = os.path.join(INPUT_DIR, video)
        
        # Cria uma instância do processador de vídeo
        processor = VideoProcessor(video_path, OUTPUT_DIR, model_size=WHISPER_MODEL_SIZE)
        
        try:
            # Processa o vídeo com captura de frames
            result = processor.process_video(capture=True)
            
            print(f"\nProcessamento concluído!")
            print(f"Transcrição salva em: {result['transcription_path']}")

            with open(result['transcription_path'], 'r', encoding='utf-8') as file:
                transcription_text = file.read()

            print('\nResumo gerado com Groq:\n')
            summarize_text(transcription_text, verbose=True)
                
            if result['frames']:
                print(f"\n\nFrames salvos em: {OUTPUT_DIR}")
                print(f"Número de frames capturados: {len(result['frames'])}")
                
        except Exception as e:
            print(f"Erro ao processar o vídeo {video}: {str(e)}")

if __name__ == "__main__":
    main()
