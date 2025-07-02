import os
import sys
# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ffmpeg_setup import setup_ffmpeg
from transcription.summarizer import summarize_text
from video_processor import VideoProcessor

def main():
    setup_ffmpeg()

    # Diretórios do projeto
    input_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "input")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    
    # Lista todos os vídeos na pasta input
    videos = [f for f in os.listdir(input_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    if not videos:
        print("Nenhum vídeo encontrado na pasta 'input'!")
        print("Por favor, adicione arquivos de vídeo (.mp4, .avi, .mov) na pasta 'input'")
        return
    
    for video in videos:
        print(f"\nProcessando vídeo: {video}")
        video_path = os.path.join(input_dir, video)
        
        # Cria uma instância do processador de vídeo
        processor = VideoProcessor(video_path, output_dir)
        
        try:
            # Processa o vídeo com captura de frames
            result = processor.process_video(capture_frames=True)
            
            print(f"\nProcessamento concluído!")
            print(f"Transcrição salva em: {result['transcription_path']}")

            with open(result['transcription_path'], 'r', encoding='utf-8') as file:
                transcription_text = file.read()

            print('\nResumo gerado com Groq:\n') 
            summarize_text(transcription_text)
                
            if result['frames']:
                print(f"\n\nFrames salvos em: {output_dir}")
                print(f"Número de frames capturados: {len(result['frames'])}")
                
        except Exception as e:
            print(f"Erro ao processar o vídeo {video}: {str(e)}")

if __name__ == "__main__":
    main()
