import os
from utils.frame_extractor import extract_frames

def process_videos_from_folder(video_folder, base_output_folder, num_frames=None, interval=None):
    # Procesar videos dentro de subcarpetas organizadas por productos
    for product_folder in os.listdir(video_folder):
        product_folder_path = os.path.join(video_folder, product_folder)
        
        if os.path.isdir(product_folder_path):  # Verifica si es una subcarpeta
            # Extraer el código de barras del nombre de la carpeta
            codigo_barra = product_folder.split('_')[0]
            
            for camera_folder in os.listdir(product_folder_path):
                camera_folder_path = os.path.join(product_folder_path, camera_folder)
                
                if os.path.isdir(camera_folder_path):  # Verifica si es una subcarpeta de la cámara
                    for video_file in os.listdir(camera_folder_path):
                        if video_file.endswith(('.mp4', '.avi', '.mov')):
                            video_path = os.path.join(camera_folder_path, video_file)
                            camera = camera_folder.lower()  # Nombrar la cámara (camera_1, camera_2, etc.)

                            # Crear la carpeta de salida en 'image_market1501'
                            output_folder = os.path.join(base_output_folder, 'image_market1501', f"{codigo_barra}_{camera}")
                            # Crear el nombre base para las imágenes
                            base_name = f"{codigo_barra}_{camera}_"
                            extract_frames(video_path, output_folder, base_name, num_frames, interval)

    # Procesar videos sueltos en la carpeta raíz
    video_paths = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    for class_idx, video_path in enumerate(video_paths):
        output_folder = os.path.join(base_output_folder, 'images_yolo', f"clase_{class_idx}")
        # También crear un nombre base para las imágenes de videos sueltos
        base_name = f"clase_{class_idx}_"
        extract_frames(video_path, output_folder, base_name, num_frames, interval)
