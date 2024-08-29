import os
import shutil
import random
import yaml

def create_yolo_dataset(output_folder_final, label_folder, dataset_folder, train_ratio=0.8):
    # crear carpetas para el dataset
    train_images_folder = os.path.join(dataset_folder, 'train', 'images')
    train_labels_folder = os.path.join(dataset_folder, 'train', 'labels')
    val_images_folder = os.path.join(dataset_folder, 'val', 'images')
    val_labels_folder = os.path.join(dataset_folder, 'val', 'labels')
    
    os.makedirs(train_images_folder, exist_ok=True)
    os.makedirs(train_labels_folder, exist_ok=True)
    os.makedirs(val_images_folder, exist_ok=True)
    os.makedirs(val_labels_folder, exist_ok=True)
    
    # listar todas las imágenes y etiquetas
    all_images = [f for f in os.listdir(output_folder_final) if f.endswith('.jpg')]
    all_labels = [f for f in os.listdir(label_folder) if f.endswith('.txt')]
    
    # asegurarse de que cada imagen tenga su etiqueta correspondiente
    matched_files = [(img, os.path.splitext(img)[0] + '.txt') for img in all_images if os.path.splitext(img)[0] + '.txt' in all_labels]
    
    # mezclar y dividir en train y val
    random.shuffle(matched_files)
    num_train = int(len(matched_files) * train_ratio)
    
    train_files = matched_files[:num_train]
    val_files = matched_files[num_train:]
    
    # mover archivos a las carpetas correspondientes
    for img_file, label_file in train_files:
        shutil.copy(os.path.join(output_folder_final, img_file), train_images_folder)
        shutil.copy(os.path.join(label_folder, label_file), train_labels_folder)
    
    for img_file, label_file in val_files:
        shutil.copy(os.path.join(output_folder_final, img_file), val_images_folder)
        shutil.copy(os.path.join(label_folder, label_file), val_labels_folder)
    
    # crear archivo .yaml
    classes = sorted({int(line.split()[0]) for label_file in all_labels for line in open(os.path.join(label_folder, label_file))})
    
    yaml_content = {
        'train': './train',
        'val': './val',
        'nc': len(classes),
        'names': [f'clase_{cls}' for cls in classes]
    }
    
    with open(os.path.join(dataset_folder, 'dataset.yaml'), 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False)

if __name__ == "__main__":
    output_folder_final = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/imagen_final'
    label_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/labels'
    dataset_folder = '/media/minigo/Disco/modelado3d/santiago/codigos/image_generator/dataset'
    
    create_yolo_dataset(output_folder_final, label_folder, dataset_folder, train_ratio=0.8)
