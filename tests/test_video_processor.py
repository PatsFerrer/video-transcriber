import os
import pytest
from src.video_processor import VideoProcessor

@pytest.fixture
def temp_dirs(tmp_path):
    """Cria diretórios temporários para teste"""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return str(input_dir), str(output_dir)

def test_video_processor_initialization(temp_dirs):
    """Testa a inicialização do VideoProcessor"""
    input_dir, output_dir = temp_dirs
    video_path = os.path.join(input_dir, "test_video.mp4")
    
    processor = VideoProcessor(video_path, output_dir)
    
    assert processor.input_path == video_path
    assert processor.output_dir == output_dir
    assert processor.model is not None 