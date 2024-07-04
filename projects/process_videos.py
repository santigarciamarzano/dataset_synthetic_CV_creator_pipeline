# projects/process_videos.py
import os
from utils.frame_extractor import extract_frames

def process_videos_from_folder(video_folder, base_output_folder, num_frames=None, interval=None):
    video_paths = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    for class_idx, video_path in enumerate(video_paths):
        output_folder = os.path.join(base_output_folder, f"clase_{class_idx}")
        extract_frames(video_path, output_folder, num_frames, interval)

if __name__ == "__main__":
    video_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/videos'
    base_output_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/images'
    num_frames = 10  
    interval = None  

    process_videos_from_folder(video_folder, base_output_folder, num_frames, interval)
