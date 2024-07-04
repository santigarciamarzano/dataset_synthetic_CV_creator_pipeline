import os
from PIL import Image
from utils.bbox_utils import draw_bounding_box, calculate_bbox_coordinates

def verify_bounding_boxes(output_folder_final, labels_folder, evaluation_folder, num_images_to_evaluate=50):
    os.makedirs(evaluation_folder, exist_ok=True)

    final_images = [f for f in os.listdir(output_folder_final) if f.endswith('.jpg')]
    final_images = final_images[:num_images_to_evaluate]

    for final_image in final_images:
        final_image_path = os.path.join(output_folder_final, final_image)
        label_path = os.path.join(labels_folder, os.path.splitext(final_image)[0] + '.txt')

        img = Image.open(final_image_path)
        img_draw = img.copy()

        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                class_id = int(parts[0])
                center_x = float(parts[1])
                center_y = float(parts[2])
                norm_width = float(parts[3])
                norm_height = float(parts[4])

                img_width, img_height = img.size
                bbox = calculate_bbox_coordinates(center_x, center_y, norm_width, norm_height, img_width, img_height)
                draw_bounding_box(img_draw, bbox, class_id, color=(0, 255, 0), thickness=3)

        evaluation_image_path = os.path.join(evaluation_folder, final_image)
        img_draw.save(evaluation_image_path)

if __name__ == "__main__":
    output_folder_final = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/imagen_final'
    labels_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/labels'
    evaluation_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator_2/data/evaluated'
    num_images_to_evaluate = 50

    verify_bounding_boxes(output_folder_final, labels_folder, evaluation_folder, num_images_to_evaluate)
