import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
        "pastel": 0,
        "postre": 0
    }
    
    for producto in datos["productos"]:
        categoria = producto["categoria"].lower()
        if categoria in ultimos_numeros:
            numero = int(producto["codigo_producto"].split("-")[1])
            if numero > ultimos_numeros[categoria]:
                ultimos_numeros[categoria] = numero
    
    # Pedimos la categoría
    console.print("\n[bold cyan]Categorías disponibles:[/bold cyan]")
    console.print("1. Pan")
    console.print("2. Pastel")
    console.print("3. Postre")
    
    while True:
        opcion = input("\nSeleccione la categoría (1-3): ")
        if opcion == "1":
            categoria = "pan"
            break
        elif opcion == "2":
            categoria = "pastel"
            break
        elif opcion == "3":
            categoria = "postre"
            break
        else:
            console.print("\n[bold red]❌ Opción no válida[/bold red]")
    
    # Generamos el nuevo código
    nuevo_numero = ultimos_numeros[categoria] + 1
    return f"{categoria.upper()}-{nuevo_numero:03d}"

def validar_producto(datos, codigo):
    """Verifica si un producto existe en los datos"""
    return codigo in datos['productos']

def validar_categoria(categoria):
    """Valida que la categoría ingresada sea válida"""
    categorias_validas = ['pan', 'pastel', 'postre']
    return categoria.lower() in categorias_validas

def agregar_producto(datos):
    """Agrega un nuevo producto al sistema"""
    console.print("\n[bold green]=== AGREGAR PRODUCTO ===[/bold green]")
    
    # Generamos el código del producto
    codigo = generar_codigo_producto(datos)
    
    # Pedimos los datos del producto
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    proveedor = input("Proveedor: ")
    stock = int(input("Cantidad en stock: "))
    precio_venta = float(input("Precio de venta: "))
    precio_proveedor = float(input("Precio del proveedor: "))
    
    # Creamos el producto
    producto = {
        "codigo_producto": codigo,
        "nombre": nombre,
        "categoria": codigo.split("-")[0].lower(),
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
    tabla.add_column("Código", style="cyan")
    tabla.add_column("Nombre", style="green")
    tabla.add_column("Categoría", style="yellow")
    tabla.add_column("Stock", justify="right")
    tabla.add_column("Precio Venta", justify="right")
    tabla.add_column("Precio Proveedor", justify="right")
    
    encontrados = False
    for producto in datos["productos"]:
        if (busqueda in producto["codigo_producto"].lower() or 
            busqueda in producto["nombre"].lower()):
            tabla.add_row(
                producto["codigo_producto"],
                producto["nombre"],
                producto["categoria"],
                str(producto["cantidad_en_stock"]),
                f"${producto['precio_venta']:.2f}",
                f"${producto['precio_proveedor']:.2f}"
            )
            encontrados = True
    
    if encontrados:
        console.print(tabla)
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
    
    # Mostramos la lista de productos
    listar_productos(datos)
    
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

def gestionar_productos(datos):
    """Gestiona el menú de productos"""
    while True:
        opcion = mostrar_menu_productos()
        
        if opcion == "1":
            agregar_producto(datos)
        elif opcion == "2":
            listar_productos(datos)
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