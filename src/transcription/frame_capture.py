import os
from moviepy.editor import VideoFileClip

def capture_frames(video_path: str, output_dir: str, interval: int = 60) -> list:
    video = VideoFileClip(video_path)
    frame_paths = []

    for t in range(0, int(video.duration), interval):
        frame_path = os.path.join(output_dir, f"frame_{t}s.jpg")
        video.save_frame(frame_path, t)
        frame_paths.append(frame_path)

    video.close()
    return frame_paths
