import os
from PIL import Image, ImageDraw, ImageFont

def draw_bounding_box(image, bbox, class_id, color=(0, 255, 0), thickness=3):
    draw = ImageDraw.Draw(image)
    for i in range(thickness):
        draw.rectangle(
            [(bbox[0] - i, bbox[1] - i), (bbox[2] + i, bbox[3] + i)],
            outline=color
        )
    # Colocar el ID de la clase encima del bounding box
    font = ImageFont.load_default()
    text_position = (bbox[0], bbox[1] - 10)
    draw.text(text_position, str(class_id), fill=color, font=font)

def calculate_bbox_coordinates(center_x, center_y, norm_width, norm_height, img_width, img_height):
    box_width = norm_width * img_width
    box_height = norm_height * img_height
    x_min = int((center_x * img_width) - (box_width / 2))
    y_min = int((center_y * img_height) - (box_height / 2))
    x_max = int((center_x * img_width) + (box_width / 2))
    y_max = int((center_y * img_height) + (box_height / 2))

    # Verificar y ajustar las coordenadas del bounding box
    if x_min < 0:
        x_min = 0
    if y_min < 0:
        y_min = 0
    if x_max > img_width:
        x_max = img_width
    if y_max > img_height:
        y_max = img_height

    return [x_min, y_min, x_max, y_max]
