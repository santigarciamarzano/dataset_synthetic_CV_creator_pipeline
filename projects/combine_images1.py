import random
import os
from PIL import Image

def combine_images(output_folder_segmented, background_folder, output_folder_final, label_folder):
    os.makedirs(output_folder_final, exist_ok=True)
    os.makedirs(label_folder, exist_ok=True)

    # Crear una lista de imágenes segmentadas por clase
    class_images = {}
    for class_idx, class_folder in enumerate(os.listdir(output_folder_segmented)):
        class_folder_path = os.path.join(output_folder_segmented, class_folder)
        if os.path.isdir(class_folder_path):
            class_images[class_idx] = [os.path.join(class_folder_path, f) for f in os.listdir(class_folder_path) if f.endswith('.png')]

    # Procesar cada imagen de fondo
    background_files = [f for f in os.listdir(background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    num_backgrounds = len(background_files)

    # Obtener el número máximo de imágenes por clase
    max_images_per_class = max(len(images) for images in class_images.values())

    # Iterar sobre las imágenes segmentadas por clase
    for i in range(max_images_per_class):
        for background_idx, background_filename in enumerate(background_files):
            background_path = os.path.join(background_folder, background_filename)
            background_img = Image.open(background_path)
            bg_width, bg_height = background_img.size

            final_img = background_img.convert('RGBA')  # Asegurarse de que el fondo está en 'RGBA'
            labels = []

            # Añadir una imagen de cada clase
            for class_idx, images in class_images.items():
                if i < len(images):  # Verificar si hay suficientes imágenes en esta clase
                    segmented_path = images[i]
                    segmented_img = Image.open(segmented_path)

                    # Escalar la imagen segmentada aleatoriamente entre 7% y 20% del tamaño del fondo
                    scale_factor = random.uniform(0.07, 0.20)
                    new_width = int(bg_width * scale_factor)
                    new_height = int(new_width * (segmented_img.height / segmented_img.width))
                    segmented_resized = segmented_img.resize((new_width, new_height), Image.LANCZOS)

                    # Rotar la imagen segmentada aleatoriamente entre 0 y 360 grados
                    angle = random.uniform(0, 360)
                    segmented_rotated = segmented_resized.rotate(angle, expand=True)

                    # Convertir a 'RGBA' si no lo está ya
                    if segmented_rotated.mode != 'RGBA':
                        segmented_rotated = segmented_rotated.convert('RGBA')

                    # Posicionar la imagen segmentada en un lugar aleatorio del fondo
                    max_x = bg_width - segmented_rotated.width
                    max_y = bg_height - segmented_rotated.height
                    random_x = random.randint(0, max_x)
                    random_y = random.randint(0, max_y)

                    # Pegar la imagen segmentada en la imagen de fondo
                    final_img.paste(segmented_rotated, (random_x, random_y), segmented_rotated)

                    # Calcular las coordenadas del bounding box y normalizarlas
                    img_width, img_height = final_img.size
                    x_center = (random_x + segmented_rotated.width / 2) / img_width
                    y_center = (random_y + segmented_rotated.height / 2) / img_height
                    width = segmented_rotated.width / img_width
                    height = segmented_rotated.height / img_height

                    # Añadir las coordenadas a la lista de etiquetas
                    labels.append(f"{class_idx} {x_center} {y_center} {width} {height}")

            # Guardar la imagen final
            final_filename = f"final_{os.path.splitext(background_filename)[0]}_{i}.jpg"
            final_path = os.path.join(output_folder_final, final_filename)
            final_img = final_img.convert('RGB')  # Convertir a 'RGB' antes de guardar
            final_img.save(final_path)

            # Guardar las etiquetas en un archivo .txt con el mismo nombre que la imagen final
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
