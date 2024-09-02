#frame_extractor.py
import os
import cv2

def extract_frames(video_path, output_folder, base_name, num_frames=None, interval=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if num_frames is not None:
        frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
    elif interval is not None:
        frame_indices = [int(i * fps * interval) for i in range(int(total_frames / (fps * interval)))]
    else:
        raise ValueError("Pasar otro valor de numero de frames o intervalo")

    for idx, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        # Usar el formato <codigo-barra>_<camara-n>_<nro-imagen>.jpg
        frame_path = os.path.join(output_folder, f"{base_name}{idx:04d}.jpg")
        cv2.imwrite(frame_path, frame)

    cap.release()