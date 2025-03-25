import json
import os

def cargar_datos():
    """Carga los datos desde el archivo JSON"""
    try:
        with open("datos/datos_panaderia.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return crear_estructura_inicial()
    except json.JSONDecodeError:
        return crear_estructura_inicial()

def guardar_datos(datos):
    """Guarda los datos en el archivo JSON"""
    with open("datos/datos_panaderia.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def crear_estructura_inicial():
    """Crea la estructura inicial de datos"""
    datos = {
        "productos": [],
        "pedidos": []
    }
    guardar_datos(datos)
    return datos 