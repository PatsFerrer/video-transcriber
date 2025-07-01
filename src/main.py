import os
import sys

# Define o caminho absoluto para o ffmpeg.exe que está na pasta do projeto
FFMPEG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ffmpeg', 'ffmpeg.exe'))

# Verifica se o FFmpeg existe
if not os.path.isfile(FFMPEG_PATH):
    print(f"ERRO: FFmpeg não encontrado em: {FFMPEG_PATH}")
    print("Por favor, verifique se o arquivo ffmpeg.exe está na pasta 'ffmpeg' do projeto.")
    sys.exit(1)

# Configura as variáveis de ambiente para o FFmpeg
os.environ["IMAGEIO_FFMPEG_EXE"] = FFMPEG_PATH
os.environ["FFMPEG_BINARY"] = FFMPEG_PATH

print(f"FFMPEG_PATH = {FFMPEG_PATH}")
print(f"Existe? {os.path.isfile(FFMPEG_PATH)}")

from video_processor import VideoProcessor

def main():
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
            if result['frames']:
                print(f"Frames salvos em: {output_dir}")
                print(f"Número de frames capturados: {len(result['frames'])}")
                
        except Exception as e:
            print(f"Erro ao processar o vídeo {video}: {str(e)}")

if __name__ == "__main__":
    main() 