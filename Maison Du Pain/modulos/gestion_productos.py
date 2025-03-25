"""
Módulo para la gestión de productos
Maneja operaciones CRUD para productos de panadería
"""
from rich.console import Console
from rich.table import Table
from datetime import datetime

# Instancia de consola para la visualización
console = Console()

def updateQuantityInventory(stock, quantity):
    """Actualiza la cantidad en inventario de manera segura"""
    if quantity > 0:
        stock = stock + quantity
        return stock
    else:
        return stock

def mostrar_menu_productos():
    """Muestra el menú de gestión de productos"""
    console.print("\n[bold cyan]=== GESTIÓN DE PRODUCTOS ===[/bold cyan]")
    console.print("1️⃣ Agregar Producto")
    console.print("2️⃣ Listar Productos")
    console.print("3️⃣ Buscar Producto")
    console.print("4️⃣ Editar Producto")
    console.print("5️⃣ Eliminar Producto")
    console.print("6️⃣ 🔙 Volver al Menú Principal")
    return input("\n⚡ Seleccione una opción: ")

def generar_codigo_producto(datos):
    """Genera un código único para el producto"""
    # Buscamos el último número usado por categoría
    ultimos_numeros = {
        "pan": 0,
        "pt": 0,  # PT para pasteles
        "ps": 0   # PS para postres
    }
    
    # Mapeo de categorías completas a códigos
    mapeo_categorias = {
        "pan": "PAN",
        "pastel": "PT",
        "postre": "PS"
    }
    
    for producto in datos["productos"]:
        categoria = producto["categoria"].lower()
        codigo_categoria = mapeo_categorias.get(categoria)
        if codigo_categoria:
            # Extraemos el número del código existente
            partes = producto["codigo_producto"].split("-")
            if len(partes) == 2:
                try:
                    numero = int(partes[1])
                    categoria_corta = partes[0].lower()
                    if categoria_corta == "pt" or categoria_corta == "pastel":
                        ultimos_numeros["pt"] = max(ultimos_numeros["pt"], numero)
                    elif categoria_corta == "ps" or categoria_corta == "postre":
                        ultimos_numeros["ps"] = max(ultimos_numeros["ps"], numero)
                    elif categoria_corta == "pan":
                        ultimos_numeros["pan"] = max(ultimos_numeros["pan"], numero)
                except ValueError:
                    pass
    
    # Pedimos la categoría
    console.print("\n[bold cyan]Categorías disponibles:[/bold cyan]")
    console.print("1. Pan")
    console.print("2. Pastel")
    console.print("3. Postre")
    
    while True:
        opcion = input("\nSeleccione la categoría (1-3): ")
        if opcion == "1":
            categoria = "pan"
            codigo_categoria = "PAN"
            break
        elif opcion == "2":
            categoria = "pastel"
            codigo_categoria = "PT"
            break
        elif opcion == "3":
            categoria = "postre"
            codigo_categoria = "PS"
            break
        else:
            console.print("\n[bold red]❌ Opción no válida[/bold red]")
    
    # Generamos el nuevo código
    categoria_corta = codigo_categoria.lower()
    nuevo_numero = ultimos_numeros[categoria_corta] + 1
    return f"{codigo_categoria}-{nuevo_numero:03d}"

def agregar_producto(datos):
    """Agrega un nuevo producto al sistema"""
    console.print("\n[bold green]=== AGREGAR PRODUCTO ===[/bold green]")
    
    # Generamos el código del producto
    codigo = generar_codigo_producto(datos)
    
    # Mapeo de códigos a categorías
    mapeo_categorias_inverso = {
        "PAN": "pan",
        "PT": "pastel",
        "PS": "postre"
    }
    
    # Pedimos los datos del producto
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    proveedor = input("Proveedor: ")
    stock = int(input("Cantidad en stock: "))
    precio_venta = float(input("Precio de venta: "))
    precio_proveedor = float(input("Precio del proveedor: "))
    
    # Obtenemos la categoría del código
    categoria_codigo = codigo.split("-")[0]
    categoria = mapeo_categorias_inverso.get(categoria_codigo, "otro")
    
    # Creamos el producto
    producto = {
        "codigo_producto": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "descripcion": descripcion,
        "proveedor": proveedor,
        "cantidad_en_stock": stock,
        "precio_venta": precio_venta,
        "precio_proveedor": precio_proveedor
    }
    
    # Agregamos el producto a la lista
    datos["productos"].append(producto)
    console.print("\n[bold green]✅ Producto agregado exitosamente![/bold green]")

def listar_productos(datos):
    """Muestra todos los productos en una tabla"""
    if not datos["productos"]:
        console.print("\n[bold yellow]⚠ No hay productos registrados[/bold yellow]")
        return
    
    # Creamos la tabla
    tabla = Table(title="📦 Lista de Productos")
    tabla.add_column("Código", style="cyan", justify="center")
    tabla.add_column("Nombre", style="green", justify="center")
    tabla.add_column("Categoría", style="yellow", justify="center")
    tabla.add_column("Stock", justify="center")
    tabla.add_column("Precio Venta ($)", justify="center")
    tabla.add_column("Descripción", style="white", justify="center")
    
    # Agregamos los productos a la tabla
    for producto in datos["productos"]:
        tabla.add_row(
            producto["codigo_producto"],
            producto["nombre"],
            producto["categoria"],
            str(producto["cantidad_en_stock"]),
            f"{producto['precio_venta']:.2f}",
            producto["descripcion"]
        )
    
    console.print("\n📦 --- PRODUCTOS DE LA PANADERÍA ---")
    console.print(tabla)
    console.print("\n💠 --- OPCIONES ---")
    console.print("🔹 [1] Volver al Menú Principal")
    console.print("🔹 [2] Agregar Producto Nuevo")
    return input("\n⚡ Seleccione una opción [1/2]: ")

def buscar_producto(datos):
    """Busca un producto por código o nombre"""
    if not datos["productos"]:
        console.print("\n[bold yellow]⚠ No hay productos registrados[/bold yellow]")
        return
    
    busqueda = input("\nIngrese código o nombre del producto: ").lower()
    
    # Creamos la tabla para mostrar resultados
    tabla = Table(title="Resultados de la Búsqueda")
    tabla.add_column("Código", style="cyan", justify="center")
    tabla.add_column("Nombre", style="green", justify="center")
    tabla.add_column("Categoría", style="yellow", justify="center")
    tabla.add_column("Stock", justify="center")
    tabla.add_column("Precio Venta ($)", justify="center")
    tabla.add_column("Descripción", style="white", justify="center")
    
    encontrados = False
    for producto in datos["productos"]:
        if (busqueda in producto["codigo_producto"].lower() or 
            busqueda in producto["nombre"].lower()):
            tabla.add_row(
                producto["codigo_producto"],
                producto["nombre"],
                producto["categoria"],
                str(producto["cantidad_en_stock"]),
                f"{producto['precio_venta']:.2f}",
                producto["descripcion"]
            )
            encontrados = True
    
    if encontrados:
        console.print(tabla)
        
        # Verificar productos con bajo stock
        for producto in datos["productos"]:
            if ((busqueda in producto["codigo_producto"].lower() or 
                busqueda in producto["nombre"].lower()) and 
                producto["cantidad_en_stock"] < 5):
                console.print(f"\n[bold red]⚠ ALERTA: El producto {producto['nombre']} tiene stock bajo ({producto['cantidad_en_stock']} unidades)[/bold red]")
    else:
        console.print("\n[bold yellow]⚠ No se encontraron productos[/bold yellow]")

def editar_producto(datos):
    """Edita un producto existente"""
    if not datos["productos"]:
        console.print("\n[bold yellow]⚠ No hay productos registrados[/bold yellow]")
        return
    
    codigo = input("\nIngrese el código del producto a editar: ")
    
    # Buscamos el producto
    for producto in datos["productos"]:
        if producto["codigo_producto"] == codigo:
            # Pedimos los nuevos datos
            producto["nombre"] = input("Nuevo nombre: ")
            producto["descripcion"] = input("Nueva descripción: ")
            producto["proveedor"] = input("Nuevo proveedor: ")
            
            # Actualizamos el stock usando la nueva función
            cantidad = int(input("Cantidad a agregar/quitar (positivo para agregar, negativo para quitar): "))
            producto["cantidad_en_stock"] = updateQuantityInventory(producto["cantidad_en_stock"], cantidad)
            
            producto["precio_venta"] = float(input("Nuevo precio de venta: "))
            producto["precio_proveedor"] = float(input("Nuevo precio del proveedor: "))
            
            console.print("\n[bold green]✅ Producto editado exitosamente![/bold green]")
            return
    
    console.print("\n[bold red]❌ Producto no encontrado[/bold red]")

def eliminar_producto(datos):
    """Elimina un producto del sistema"""
    if not datos["productos"]:
        console.print("\n[bold yellow]⚠ No hay productos registrados[/bold yellow]")
        return
    
    # Mostramos la lista de productos con una función separada
    mostrar_lista_productos(datos)
    
    codigo = input("\nIngrese el código del producto a eliminar: ")
    
    # Buscamos y eliminamos el producto
    for i, producto in enumerate(datos["productos"]):
        if producto["codigo_producto"] == codigo:
            # Mostramos los detalles del producto a eliminar
            console.print("\n[bold red]⚠ Producto a eliminar:[/bold red]")
            tabla = Table(title="Detalles del Producto")
            tabla.add_column("Código", style="cyan")
            tabla.add_column("Nombre", style="green")
            tabla.add_column("Categoría", style="yellow")
            tabla.add_column("Stock", justify="right")
            tabla.add_column("Precio Venta", justify="right")
            tabla.add_column("Precio Proveedor", justify="right")
            
            tabla.add_row(
                producto["codigo_producto"],
                producto["nombre"],
                producto["categoria"],
                str(producto["cantidad_en_stock"]),
                f"${producto['precio_venta']:.2f}",
                f"${producto['precio_proveedor']:.2f}"
            )
            console.print(tabla)
            
            confirmacion = input("\n¿Está seguro de eliminar este producto? (s/n): ").lower()
            if confirmacion == 's':
                datos["productos"].pop(i)
                console.print("\n[bold green]✅ Producto eliminado exitosamente![/bold green]")
            return
    
    console.print("\n[bold red]❌ Producto no encontrado[/bold red]")

def mostrar_lista_productos(datos):
    """Muestra la lista de productos sin pedir opciones"""
    if not datos["productos"]:
        console.print("\n[bold yellow]⚠ No hay productos registrados[/bold yellow]")
        return
    
    # Creamos la tabla
    tabla = Table(title="📦 Lista de Productos")
    tabla.add_column("Código", style="cyan", justify="center")
    tabla.add_column("Nombre", style="green", justify="center")
    tabla.add_column("Categoría", style="yellow", justify="center")
    tabla.add_column("Stock", justify="center")
    tabla.add_column("Precio Venta ($)", justify="center")
    tabla.add_column("Descripción", style="white", justify="center")
    
    # Agregamos los productos a la tabla
    for producto in datos["productos"]:
        tabla.add_row(
            producto["codigo_producto"],
            producto["nombre"],
            producto["categoria"],
            str(producto["cantidad_en_stock"]),
            f"{producto['precio_venta']:.2f}",
            producto["descripcion"]
        )
    
    console.print("\n📦 --- PRODUCTOS DE LA PANADERÍA ---")
    console.print(tabla)

def gestionar_productos(datos):
    """Gestiona el menú de productos"""
    while True:
        opcion = mostrar_menu_productos()
        
        if opcion == "1":
            agregar_producto(datos)
        elif opcion == "2":
            opcion_lista = listar_productos(datos)
            if opcion_lista == "2":
                agregar_producto(datos)
        elif opcion == "3":
            buscar_producto(datos)
        elif opcion == "4":
            editar_producto(datos)
        elif opcion == "5":
            eliminar_producto(datos)
        elif opcion == "6":
            break
        else:
            console.print("\n[bold yellow]⚠ Opción no válida[/bold yellow]") 