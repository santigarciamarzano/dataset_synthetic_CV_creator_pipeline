import os
import torch
from GroundingDINO.groundingdino.util.inference import load_model, predict, annotate
import GroundingDINO.groundingdino.datasets.transforms as T
from PIL import Image


def listar_imagenes(base_folder):
    """
    Recorre una carpeta base y devuelve un diccionario donde la clave es la ruta 
    de cada subcarpeta y el valor es una lista de nombres de imágenes en esa subcarpeta.
    """
    # Diccionario para almacenar las rutas de imágenes por carpeta
    imagenes_dict = {}

    # Recorrer todas las subcarpetas dentro de base_folder
    for root, dirs, files in os.walk(base_folder):
        # Filtrar solo archivos con extensión .jpg
        imagenes = [f for f in files if f.endswith('.jpg')]
        if imagenes:
            # Guardar la lista de imágenes por subcarpeta
            imagenes_dict[root] = imagenes
    
    return imagenes_dict

if __name__ == "__main__":
    # Definir las rutas de las carpetas
    market_folder = 'data/images_market1501'
    yolo_folder = 'data/images_yolo'

    # Listar imágenes en ambas carpetas
    imagenes_market = listar_imagenes(market_folder)
    imagenes_yolo = listar_imagenes(yolo_folder)

    # Mostrar las rutas y los nombres de las imágenes
    print("Imágenes en Market1501:")
    for folder, imagenes in imagenes_market.items():
        print(f"Carpeta: {folder}")
        for imagen in imagenes:
            print(f" - {imagen}")

    print("\nImágenes en YOLO:")
    for folder, imagenes in imagenes_yolo.items():
        print(f"Carpeta: {folder}")
        for imagen in imagenes:
            print(f" - {imagen}")




import os
import requests

def descargar_archivo(url, ruta_destino):
    """
    Descarga un archivo desde una URL y lo guarda en la ruta especificada.
    
    Args:
    - url (str): URL del archivo a descargar.
    - ruta_destino (str): Ruta completa donde se guardará el archivo descargado.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Verifica si la solicitud fue exitosa
    
    # Guarda el archivo en la ruta especificada
    with open(ruta_destino, 'wb') as archivo:
        for chunk in response.iter_content(chunk_size=8192):
            archivo.write(chunk)
    print(f"Archivo descargado y guardado en: {ruta_destino}")

def descargar_pesos_y_config(destino_folder):
    """
    Descarga los pesos y la configuración del modelo Grounding DINO y los guarda en una carpeta especificada.
    
    Args:
    - destino_folder (str): Carpeta donde se guardarán los archivos descargados.
    """
    # URLs de los archivos
    url_pesos = 'https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth'
    url_config = 'https://raw.githubusercontent.com/IDEA-Research/GroundingDINO/main/configs/GroundingDINO_SwinT_OGC.py'
    
    # Nombres de los archivos que se descargarán
    nombre_pesos = 'groundingdino_swint_ogc.pth'
    nombre_config = 'GroundingDINO_SwinT_OGC.py'
    
    # Definir las rutas completas de los archivos
    ruta_pesos = os.path.join(destino_folder, nombre_pesos)
    ruta_config = os.path.join(destino_folder, nombre_config)
    
    # Crear la carpeta de destino si no existe
    if not os.path.exists(destino_folder):
        os.makedirs(destino_folder)
    
    # Descargar los archivos
    descargar_archivo(url_pesos, ruta_pesos)
    descargar_archivo(url_config, ruta_config)

if __name__ == "__main__":
    # Definir la carpeta de destino para guardar los archivos descargados
    destino_folder = '/ruta/a/la/carpeta/de/destino'
    
    # Descargar los pesos y la configuración
    descargar_pesos_y_config(destino_folder)
    
    print("Descarga de pesos y configuración completada.")





# Función para cargar el modelo Grounding DINO
def cargar_modelo_grounding_dino(config_path, weights_path, device='cuda'):
    """
    Carga el modelo Grounding DINO con la configuración y pesos especificados.
    
    Args:
    - config_path (str): Ruta al archivo de configuración del modelo.
    - weights_path (str): Ruta al archivo de pesos preentrenados del modelo.
    - device (str): Dispositivo en el cual cargar el modelo ('cuda' para GPU, 'cpu' para CPU).
    
    Returns:
    - model: El modelo cargado y listo para hacer inferencias.
    """
    model = load_model(config_path, weights_path)
    model.to(device)
    model.eval()  # Establece el modelo en modo evaluación
    return model

# Ejemplo de uso
if __name__ == "__main__":
    # Rutas a los archivos necesarios
    config_path = '/ruta/al/config/GroundingDINO_SwinT_OGC.py'
    weights_path = '/ruta/a/los/pesos/groundingdino_swint_ogc.pth'
    
    # Cargar el modelo
    modelo = cargar_modelo_grounding_dino(config_path, weights_path)
    
    # Ahora el modelo está listo para usarse en el etiquetado de imágenes
    print("Modelo Grounding DINO cargado exitosamente.")
