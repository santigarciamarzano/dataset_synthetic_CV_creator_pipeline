import random
from PIL import Image

def scale_image(img, bg_width, scale_min=0.07, scale_max=0.20):
    scale_factor = random.uniform(scale_min, scale_max)
    new_width = int(bg_width * scale_factor)
    new_height = int(new_width * (img.height / img.width))
    return img.resize((new_width, new_height), Image.LANCZOS)

def rotate_image(img, angle_min=0, angle_max=360):
    angle = random.uniform(angle_min, angle_max)
    return img.rotate(angle, expand=True)

def paste_image(bg_img, fg_img, max_x, max_y):
    random_x = random.randint(0, max_x)
    random_y = random.randint(0, max_y)
    bg_img.paste(fg_img, (random_x, random_y), fg_img)
    return random_x, random_y

def calculate_bounding_box(x, y, img_width, img_height, bg_width, bg_height):
    x_center = (x + img_width / 2) / bg_width
    y_center = (y + img_height / 2) / bg_height
    width = img_width / bg_width
    height = img_height / bg_height
    return x_center, y_center, width, height
