import os
from unittest import mock
from src.ffmpeg_setup import setup_ffmpeg

def test_setup_ffmpeg_windows(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setattr("os.path.isfile", lambda path: True)

    setup_ffmpeg()

    expected_path = os.path.normpath("ffmpeg/windows/ffmpeg.exe")
    assert expected_path in os.environ["IMAGEIO_FFMPEG_EXE"]

def test_setup_ffmpeg_linux(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("os.path.isfile", lambda path: True)

    setup_ffmpeg()

    expected_path = os.path.normpath(os.path.join("ffmpeg", "linux", "ffmpeg"))
    assert expected_path in os.environ["IMAGEIO_FFMPEG_EXE"]

def test_setup_ffmpeg_macos(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr("os.path.isfile", lambda path: True)

    setup_ffmpeg()

    expected_path = os.path.normpath(os.path.join("ffmpeg", "macos", "ffmpeg"))
    assert expected_path in os.environ["IMAGEIO_FFMPEG_EXE"]
