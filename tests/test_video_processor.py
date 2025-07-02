import os
from unittest.mock import MagicMock, patch
import pytest

from transcription.video_processor import VideoProcessor


@pytest.fixture
def temp_dirs(tmp_path):
    """Cria diretórios temporários para teste"""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return str(input_dir), str(output_dir)


@patch("transcription.video_processor.Transcriber")
def test_video_processor_initialization(mock_transcriber_class, temp_dirs):
    """Testa a inicialização do VideoProcessor sem carregar o modelo real"""
    input_dir, output_dir = temp_dirs
    video_path = os.path.join(input_dir, "test_video.mp4")

    # Mocka o objeto Transcriber retornado
    mock_transcriber = MagicMock()
    mock_transcriber_class.return_value = mock_transcriber

    processor = VideoProcessor(video_path, output_dir)

    assert processor.input_path == video_path
    assert processor.output_dir == output_dir
    assert processor.transcriber == mock_transcriber
