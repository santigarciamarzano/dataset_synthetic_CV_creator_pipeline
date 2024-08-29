#create_market1501_dataset.py
import os
import shutil
import random

def create_market1501_dataset(cropped_images_folder, dataset_folder, train_ratio):
    os.makedirs(os.path.join(dataset_folder, 'train'), exist_ok=True)
    os.makedirs(os.path.join(dataset_folder, 'gallery'), exist_ok=True)
    os.makedirs(os.path.join(dataset_folder, 'query'), exist_ok=True)

    

    for class_folder in os.listdir(cropped_images_folder):
        class_path = os.path.join(cropped_images_folder, class_folder)
        
        if os.path.isdir(class_path):
            images = [img for img in os.listdir(class_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
            num_images = len(images)
            
            random.shuffle(images)
            
            num_train = int(num_images * train_ratio)
            
            train_images = images[:num_train]
            gallery_images = images[num_train:]
            
            for i, img in enumerate(train_images):
                src = os.path.join(class_path, img)
                dst = os.path.join(dataset_folder, 'train', f'{class_folder}_{i}{os.path.splitext(img)[1]}')
                shutil.copy(src, dst)
            
            for i, img in enumerate(gallery_images):
                src = os.path.join(class_path, img)
                dst = os.path.join(dataset_folder, 'gallery', f'{class_folder}_{i}{os.path.splitext(img)[1]}')
                shutil.copy(src, dst)
            
            if gallery_images:
                query_img = gallery_images[0]
                src = os.path.join(class_path, query_img)
                dst = os.path.join(dataset_folder, 'query', f'{class_folder}_{0}{os.path.splitext(query_img)[1]}')
                shutil.copy(src, dst)
            
            print(f"Clases procesadas: {class_folder}")
    
    print("Dataset Market-1501 creado con éxito.")

if __name__ == "__main__":
    cropped_images_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/data/cropped_images'
    dataset_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/data/dataset_market1501'
    train_ratio = 0.7
    create_market1501_dataset(cropped_images_folder, dataset_folder, train_ratio)

