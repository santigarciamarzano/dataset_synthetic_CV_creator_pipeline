import random
import os
from PIL import Image
from utils.image_utils import scale_image, rotate_image, paste_image, calculate_bounding_box

def combine_images(output_folder_segmented, background_folder, output_folder_final, label_folder):
    os.makedirs(output_folder_final, exist_ok=True)
    os.makedirs(label_folder, exist_ok=True)

    class_images = {}
    for class_idx, class_folder in enumerate(os.listdir(output_folder_segmented)):
        class_folder_path = os.path.join(output_folder_segmented, class_folder)
        if os.path.isdir(class_folder_path):
            class_images[class_idx] = [os.path.join(class_folder_path, f) for f in os.listdir(class_folder_path) if f.endswith('.png')]

    background_files = [f for f in os.listdir(background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    num_backgrounds = len(background_files)

    max_images_per_class = max(len(images) for images in class_images.values())

    for i in range(max_images_per_class):
        for background_idx, background_filename in enumerate(background_files):
            background_path = os.path.join(background_folder, background_filename)
            background_img = Image.open(background_path)
            bg_width, bg_height = background_img.size

            final_img = background_img.convert('RGBA')  # Asegurarse de que el fondo está en 'RGBA'
            labels = []

            
            for class_idx, images in class_images.items():
                if i < len(images):  # Verificar si hay suficientes imágenes en esta clase
                    segmented_path = images[i]
                    segmented_img = Image.open(segmented_path)

                    
                    segmented_resized = scale_image(segmented_img, bg_width) # Escalar, rotar y pegar la imagen segmentada
                    segmented_rotated = rotate_image(segmented_resized)
                    max_x = bg_width - segmented_rotated.width
                    max_y = bg_height - segmented_rotated.height
                    random_x, random_y = paste_image(final_img, segmented_rotated, max_x, max_y)

                    x_center, y_center, width, height = calculate_bounding_box(
                        random_x, random_y, segmented_rotated.width, segmented_rotated.height, bg_width, bg_height)

                    labels.append(f"{class_idx} {x_center} {y_center} {width} {height}")

            final_filename = f"final_{os.path.splitext(background_filename)[0]}_{i}.jpg"
            final_path = os.path.join(output_folder_final, final_filename)
            final_img = final_img.convert('RGB')  # Convertir a 'RGB' antes de guardar
            final_img.save(final_path)

            label_filename = f"{os.path.splitext(final_filename)[0]}.txt"
            label_path = os.path.join(label_folder, label_filename)
            with open(label_path, 'w') as f:
                f.write("\n".join(labels))

if __name__ == "__main__":
    output_folder_segmented = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_1/segment_images'
    background_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_1/backgrounds'
    output_folder_final = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_1/imagen_final'
    label_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_1/labels'

    combine_images(output_folder_segmented, background_folder, output_folder_final, label_folder)
