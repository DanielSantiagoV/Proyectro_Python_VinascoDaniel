# 🥖 Maison du Pain - Sistema de Gestión de Panadería

Sistema de gestión desarrollado en Python para administrar el inventario y pedidos de la panadería Maison du Pain.

## 🌟 Características Principales

### 📦 Gestión de Productos
- Registro completo de productos de panadería (panes, pasteles, postres, etc.)
- Almacenamiento de información detallada:
  - Nombre del producto
  - Categoría (pan, pastel, postre)
  - Descripción
  - Proveedor
  - Cantidad en stock
  - Precios de venta y compra
- Códigos de producto automáticos basados en categoría (PN-001, PS-001, PT-001)

### 📝 Gestión de Pedidos
- Creación y administración de pedidos de clientes
- Registro detallado de productos en cada pedido:
  - Cantidad
  - Precio por unidad
  - Número de línea
- Funcionalidades completas de edición y eliminación
- Cálculo automático de totales

### 📊 Inventario Automatizado
- Actualización automática del stock al registrar pedidos
- Control de inventario en tiempo real
- Sistema de alertas para productos con stock bajo (menos de 5 unidades)
- Devolución automática de stock al eliminar pedidos

### 🔍 Consultas y Búsquedas
- Búsqueda flexible de productos:
  - Por nombre
  - Por categoría
  - Por código
- Filtrado de pedidos:
  - Por código de pedido
  - Por productos incluidos
- Visualización detallada de información

### 💾 Manejo de Archivos y Persistencia
- Almacenamiento de datos en formato JSON
- Estructura organizada de archivos:
  - `datos_panaderia.json`: Información de productos
  - `pedidos.json`: Registro de pedidos
- Persistencia de datos entre sesiones
- Manejo de errores y validaciones

### 👥 Interfaz de Usuario
- Menús intuitivos y organizados
- Confirmaciones para acciones críticas
- Mensajes informativos claros
- Tablas formateadas para mejor visualización
- Uso de colores y emojis para mejor experiencia

## 🛠️ Tecnologías Utilizadas
- Python 3
- Biblioteca Rich para interfaz de usuario
- JSON para almacenamiento de datos

## 📋 Requisitos
- Python 3.6 o superior
- Biblioteca Rich (`pip install rich`)

## 🚀 Instalación y Uso
1. Clona el repositorio
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta el programa: `python main.py`

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
```


## 📄 Creado Por:
Este proyecto está creado por Daniel Santiago.

