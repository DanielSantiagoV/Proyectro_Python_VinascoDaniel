# 🥖 Maison du Pain - Sistema de Gestión de Panadería

Sistema desarrollado en Python para administrar el inventario y pedidos de la panadería Maison du Pain, asegurando un control eficiente de productos y ventas.

## 🌟 Características Principales

### 📦 Gestión de Productos
- Registro completo de productos de panadería (panes, pasteles, postres, etc.).
- Almacenamiento de información detallada:
  - Nombre del producto
  - Categoría (pan, pastel, postre)
  - Descripción
  - Proveedor
  - Cantidad en stock
  - Precios de venta y compra
- Generación automática de códigos de producto basados en categoría (PN-001, PS-001, PT-001).
- Funcionalidades:
  - Agregar, editar y eliminar productos.
  - Listado detallado de productos registrados.

### 📝 Gestión de Pedidos
- Creación y administración de pedidos de clientes.
- Registro detallado de productos en cada pedido:
  - Cantidad
  - Precio por unidad
  - Número de línea
- Funcionalidades completas de edición y eliminación de pedidos.
- Cálculo automático de totales en cada compra.

### 📊 Inventario Automatizado
- Actualización automática del stock al registrar pedidos.
- Control de inventario en tiempo real.
- Sistema de alertas para productos con stock bajo (menos de 5 unidades).
- Devolución automática de stock al eliminar pedidos.

### 🔍 Consultas y Búsquedas
- Búsqueda flexible de productos:
  - Por nombre
  - Por categoría
  - Por código
- Filtrado de pedidos:
  - Por código de pedido
  - Por productos incluidos
- Visualización detallada de información.

### 💾 Manejo de Archivos y Persistencia
- Almacenamiento de datos en formato JSON.
- Estructura organizada de archivos:
  - `datos_panaderia.json`: Información de productos.
  - `pedidos.json`: Registro de pedidos.
- Persistencia de datos entre sesiones.
- Manejo de errores y validaciones.

### 👥 Interfaz de Usuario
- Menús intuitivos y organizados.
- Confirmaciones para acciones críticas.
- Mensajes informativos claros.
- Tablas formateadas para mejor visualización.
- Uso de colores y emojis para mejor experiencia.

## 🛠️ Tecnologías Utilizadas
- **Python 3**
- **JSON** para almacenamiento de datos.
- **Rich** para mejorar la visualización en la terminal.

## 📋 Requisitos
- Python 3.6 o superior.
- Instalar dependencias con:
  ```sh
  pip install rich


## 🚀 Instalación y Uso

### Esta guia son los pasos para poder ejecutar el proyecto Panaderia en Python, se debe tener instalado Python en la maquina, se debe tener instalado el modulo rich, para instalarlo se debe seguir los siguientes pasos:

1. 
    ```pip-requirements
    rich>=13.0.0
    ```

2. **Abre una terminal o línea de comandos**.

3. **Navega al directorio donde está el archivo `requirements.txt`**:
    ```bash
    cd /e:/Usuario/Downloads/exampole-20250325T002933Z-001/exampole/
    ```

4. **Instala las dependencias usando `pip`**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Verifica que la librería `rich` se haya instalado correctamente**:
    ```bash
    pip show rich
    ```

Fuente: [rich](https://pypi.org/project/rich/)
Fin de la guia.
## Ejecutar el proyecto

## 📁 Estructura del Proyecto
```
maison-du-pain/
├── main.py
├── modulos/
│   ├── gestion_productos.py
│   ├── gestion_pedidos.py
│   └── gestion_archivos.py
└── datos/
    ├── datos_panaderia.json
    └── pedidos.json
```

## 🗄️ Estructura de los Datos

### Productos
```json
{
  "codigo_producto": "PAN-001",
  "nombre": "Pan Francés",
  "categoria": "pan",
  "descripcion": "Pan tradicional francés",
  "proveedor": "Panadería Local",
  "cantidad_en_stock": 50,
  "precio_venta": 3.50,
  "precio_proveedor": 2.00
}
```

### Pedidos
```json
{
  "codigo_pedido": "PED-001",
  "codigo_cliente": "CLI-001",
  "fecha_pedido": "2024-03-21 15:30:00",
  "estado": "pendiente",
  "total": 150.00
}
```

### Detalles de Pedido
```json
{
  "codigo_pedido": "PED-001",
  "detalles": [
    {
      "numero_linea": 1,
      "codigo_producto": "PAN-001",
      "cantidad": 2,
      "precio_unidad": 3.50,
      "subtotal": 7.00
    }
  ]
}
`````

### 📄 Creado Por:
Este Proyecto fue desarrollado por ***Daniel Santiago Vinasco*** 

-------------------------------------------------------


---


---

### ✅ **¿Qué cambios hice en el README?**
✔ **Formato unificado** siguiendo la estructura del README de referencia.  
✔ **Secciones más organizadas** con información clara y concisa.  
✔ **Emojis en títulos** para una presentación más visual.  
✔ **Consistencia en estilo y redacción** con el README de referencia.  
✔ **Mayor claridad en la estructura de datos y ejemplos JSON.**  

---


---
----------------------------------------------




