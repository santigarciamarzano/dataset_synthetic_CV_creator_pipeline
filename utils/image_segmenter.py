# utils/image_segmenter.py
import os
from rembg import remove 
from PIL import Image

def segment_images(input_base_folder, output_base_folder):
    for class_folder in os.listdir(input_base_folder):
        input_folder = os.path.join(input_base_folder, class_folder)
        output_folder = os.path.join(output_base_folder, class_folder)
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for filename in os.listdir(input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')

                inp = Image.open(input_path)
                output = remove(inp)

                if output.mode != 'RGBA':
                    output = output.convert('RGBA')

                bbox = output.getbbox()
                if bbox:
                    output_cropped = output.crop(bbox)
                    output_cropped.save(output_path)
                else:
                    output.save(output_path)

                print(f"Processed {filename} in {class_folder}: bounding box = {bbox}")

# Notebook: llamando a la función segment_images
from utils.image_segmenter import segment_images

input_base_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/images'
output_base_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/segment_images'

segment_images(input_base_folder, output_base_folder)


