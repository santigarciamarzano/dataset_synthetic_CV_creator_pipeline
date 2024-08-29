import os
from PIL import Image
import random

def add_background_to_images(segmented_images_folder, cropped_images_folder):
    os.makedirs(cropped_images_folder, exist_ok=True)

    background_colors = [
        (245, 245, 245),  # Gris claro
        (220, 220, 220),  # Gris más oscuro
        (238, 232, 170),  # Beige
        (240, 230, 140),  # Amarillo claro
        (255, 228, 181),  # Beige claro
        (250, 240, 230),  # Almendra blanqueada
        (255, 222, 173),  # Blanco Navajo
        (255, 228, 225),  # Rosa suave
        (245, 222, 179),  # Trigo
        (240, 248, 255),  # Azul claro
        (255, 250, 250),  # Nieve
        (169, 169, 169),  # Gris oscuro
        (128, 128, 128),  # Gris
        (105, 105, 105),  # Gris tenue
        (80, 80, 80),     # Carbón
        (54, 69, 79),     # Gris pizarra oscuro
        (47, 79, 79),     # Gris pizarra profundo
        (39, 39, 39),     # Carbón negro
    ]

    class_folders = [os.path.join(segmented_images_folder, folder) for folder in os.listdir(segmented_images_folder) if os.path.isdir(os.path.join(segmented_images_folder, folder))]

    for class_folder in class_folders:
        class_name = os.path.basename(class_folder)
        output_class_folder = os.path.join(cropped_images_folder, class_name)
        
        os.makedirs(output_class_folder, exist_ok=True)
        
        images = [os.path.join(class_folder, img) for img in os.listdir(class_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
        
        for image_path in images:
            img = Image.open(image_path)
            
            bg_color = random.choice(background_colors)
            bg = Image.new('RGB', img.size, bg_color)
            
            bg.paste(img, (0, 0), img)
            
            output_image_path = os.path.join(output_class_folder, f"cropped_{os.path.basename(image_path)}")
            bg.save(output_image_path)
            
            print(f"Imagen guardada: {output_image_path} con fondo {bg_color}")

if __name__ == "__main__":
    segmented_images_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/data/segmented_images'
    cropped_images_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/data/cropped_images'
    add_background_to_images(segmented_images_folder, cropped_images_folder)
