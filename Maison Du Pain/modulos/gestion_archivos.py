"""
Módulo para la gestión de archivos JSON
Maneja la carga y guardado de datos
"""
import json
import os

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(BASE_DIR, "datos")

def cargar_datos():
    """Carga los datos desde el archivo JSON"""
    try:
        ruta_archivo = os.path.join(DATOS_DIR, "datos_panaderia.json")
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return crear_estructura_inicial()
    except json.JSONDecodeError:
        return crear_estructura_inicial()

def guardar_datos(datos):
    """Guarda los datos en el archivo JSON"""
    # Aseguramos que existe el directorio
    os.makedirs(DATOS_DIR, exist_ok=True)
    
    ruta_archivo = os.path.join(DATOS_DIR, "datos_panaderia.json")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def crear_estructura_inicial():
    """Crea la estructura inicial de datos"""
    datos = {
        "productos": [
            {
                "codigo_producto": "PAN-001",
                "nombre": "Pan Francés",
                "categoria": "pan",
                "descripcion": "Pan tradicional francés crujiente",
                "proveedor": "Panadería Central",
                "cantidad_en_stock": 50,
                "precio_venta": 1.50,
                "precio_proveedor": 0.75
            },
            {
                "codigo_producto": "PASTEL-001",
                "nombre": "Torta de Chocolate",
                "categoria": "pastel",
                "descripcion": "Deliciosa torta de chocolate con cobertura",
                "proveedor": "Dulces Delicias",
                "cantidad_en_stock": 10,
                "precio_venta": 25.00,
                "precio_proveedor": 15.00
            }
        ],
        "pedidos": []
    }
    guardar_datos(datos)
    return datos

def cargar_pedidos():
    """Carga los pedidos desde el archivo JSON"""
    try:
        ruta_pedidos = os.path.join(DATOS_DIR, "pedidos")
        os.makedirs(ruta_pedidos, exist_ok=True)
        
        ruta_archivo = os.path.join(ruta_pedidos, "pedidos.json")
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        datos = {"pedidos": []}
        guardar_pedidos(datos)
        return datos

def cargar_detalles_pedidos():
    """Carga los detalles de pedidos desde el archivo JSON"""
    try:
        ruta_pedidos = os.path.join(DATOS_DIR, "pedidos")
        os.makedirs(ruta_pedidos, exist_ok=True)
        
        ruta_archivo = os.path.join(ruta_pedidos, "detalles_pedidos.json")
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        datos = {"detalles_pedidos": []}
        guardar_detalles_pedidos(datos)
        return datos

def guardar_pedidos(datos):
    """Guarda los pedidos en el archivo JSON"""
    ruta_pedidos = os.path.join(DATOS_DIR, "pedidos")
    os.makedirs(ruta_pedidos, exist_ok=True)
    
    ruta_archivo = os.path.join(ruta_pedidos, "pedidos.json")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def guardar_detalles_pedidos(datos):
    """Guarda los detalles de pedidos en el archivo JSON"""
    ruta_pedidos = os.path.join(DATOS_DIR, "pedidos")
    os.makedirs(ruta_pedidos, exist_ok=True)
    
    ruta_archivo = os.path.join(ruta_pedidos, "detalles_pedidos.json")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False) 