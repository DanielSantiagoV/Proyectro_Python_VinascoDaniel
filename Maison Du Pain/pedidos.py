from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import json
import os

console = Console()

def cargar_pedidos():
    """Carga los pedidos desde el archivo JSON"""
    try:
        with open("datos/pedidos/pedidos.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"pedidos": []}

def cargar_detalles_pedidos():
    """Carga los detalles de pedidos desde el archivo JSON"""
    try:
        with open("datos/pedidos/detalles_pedidos.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {"detalles_pedidos": []}

def guardar_pedidos(datos):
    """Guarda los pedidos en el archivo JSON"""
    with open("datos/pedidos/pedidos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def guardar_detalles_pedidos(datos):
    """Guarda los detalles de pedidos en el archivo JSON"""
    with open("datos/pedidos/detalles_pedidos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def mostrar_menu_pedidos():
    """Muestra el menú de gestión de pedidos"""
    console.print("\n[bold cyan]=== GESTIÓN DE PEDIDOS ===[/bold cyan]")
    console.print("1️⃣ Crear Pedido")
    console.print("2️⃣ Listar Pedidos")
    console.print("3️⃣ Buscar Pedido")
    console.print("4️⃣ Editar Pedido")
    console.print("5️⃣ Eliminar Pedido")
    console.print("6️⃣ 🔙 Volver al Menú Principal")
    return input("\n⚡ Seleccione una opción: ")

def generar_codigo_pedido(datos):
    """Genera un código único para el pedido"""
    # Buscamos el último número usado
    ultimo_numero = 0
    for pedido in datos["pedidos"]:
        numero = int(pedido["codigo_pedido"].split("-")[1])
        if numero > ultimo_numero:
            ultimo_numero = numero
    
    # Generamos el nuevo código
    nuevo_numero = ultimo_numero + 1
    return f"PED-{nuevo_numero:03d}"

def crear_pedido(datos_productos):
    """Crea un nuevo pedido"""
    console.print("\n[bold green]=== CREAR PEDIDO ===[/bold green]")
    
    # Cargamos los datos actuales
    datos_pedidos = cargar_pedidos()
    datos_detalles = cargar_detalles_pedidos()
    
    # Pedimos los datos del cliente
    codigo_cliente = input("Código del cliente: ")
    
    # Creamos el pedido
    pedido = {
        "codigo_pedido": generar_codigo_pedido(datos_pedidos),
        "codigo_cliente": codigo_cliente,
        "fecha_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estado": "pendiente",
        "total": 0.0
    }
    
    # Creamos los detalles del pedido
    detalles_pedido = {
        "codigo_pedido": pedido["codigo_pedido"],
        "detalles": []
    }
    
    # Agregamos productos al pedido
    while True:
        codigo_producto = input("\nCódigo del producto (o 'fin' para terminar): ")
        if codigo_producto.lower() == 'fin':
            break
        
        # Buscamos el producto
        producto_encontrado = None
        for producto in datos_productos["productos"]:
            if producto["codigo_producto"] == codigo_producto:
                producto_encontrado = producto
                break
        
        if not producto_encontrado:
            console.print("\n[bold red]❌ Producto no encontrado[/bold red]")
            continue
        
        # Pedimos la cantidad
        cantidad = int(input("Cantidad: "))
        if cantidad > producto_encontrado["cantidad_en_stock"]:
            console.print("\n[bold red]❌ No hay suficiente stock[/bold red]")
            continue
        
        # Calculamos el subtotal
        subtotal = cantidad * producto_encontrado["precio_venta"]
        
        # Creamos el detalle
        detalle = {
            "numero_linea": len(detalles_pedido["detalles"]) + 1,
            "codigo_producto": producto_encontrado["codigo_producto"],
            "cantidad": cantidad,
            "precio_unidad": producto_encontrado["precio_venta"],
            "subtotal": subtotal
        }
        
        # Actualizamos el stock
        producto_encontrado["cantidad_en_stock"] -= cantidad
        
        # Agregamos el detalle al pedido
        detalles_pedido["detalles"].append(detalle)
        pedido["total"] += subtotal
    
    # Agregamos el pedido y sus detalles a las listas
    datos_pedidos["pedidos"].append(pedido)
    datos_detalles["detalles_pedidos"].append(detalles_pedido)
    
    # Guardamos los cambios
    guardar_pedidos(datos_pedidos)
    guardar_detalles_pedidos(datos_detalles)
    
    console.print("\n[bold green]✅ Pedido creado exitosamente![/bold green]")

def listar_pedidos():
    """Muestra todos los pedidos en una tabla"""
    datos_pedidos = cargar_pedidos()
    datos_detalles = cargar_detalles_pedidos()
    
    if not datos_pedidos["pedidos"]:
        console.print("\n[bold yellow]⚠ No hay pedidos registrados[/bold yellow]")
        return
    
    # Creamos la tabla
    tabla = Table(title="Lista de Pedidos")
    tabla.add_column("Código", style="cyan")
    tabla.add_column("Cliente", style="green")
    tabla.add_column("Fecha", style="yellow")
    tabla.add_column("Estado", style="magenta")
    tabla.add_column("Total", justify="right")
    
    # Agregamos los pedidos a la tabla
    for pedido in datos_pedidos["pedidos"]:
        tabla.add_row(
            pedido["codigo_pedido"],
            pedido["codigo_cliente"],
            pedido["fecha_pedido"],
            pedido["estado"],
            f"${pedido['total']:.2f}"
        )
    
    console.print(tabla)
    
    # Preguntamos si quiere ver los detalles
    if input("\n¿Desea ver los detalles de algún pedido? (s/n): ").lower() == 's':
        codigo = input("Ingrese el código del pedido: ")
        mostrar_detalles_pedido(codigo, datos_detalles)

def mostrar_detalles_pedido(codigo_pedido, datos_detalles):
    """Muestra los detalles de un pedido específico"""
    for detalle_pedido in datos_detalles["detalles_pedidos"]:
        if detalle_pedido["codigo_pedido"] == codigo_pedido:
            # Creamos la tabla de detalles
            tabla = Table(title=f"Detalles del Pedido {codigo_pedido}")
            tabla.add_column("Línea", justify="right")
            tabla.add_column("Producto", style="cyan")
            tabla.add_column("Cantidad", justify="right")
            tabla.add_column("Precio Unit.", justify="right")
            tabla.add_column("Subtotal", justify="right")
            
            # Agregamos los detalles a la tabla
            for detalle in detalle_pedido["detalles"]:
                tabla.add_row(
                    str(detalle["numero_linea"]),
                    detalle["codigo_producto"],
                    str(detalle["cantidad"]),
                    f"${detalle['precio_unidad']:.2f}",
                    f"${detalle['subtotal']:.2f}"
                )
            
            console.print(tabla)
            return
    
    console.print("\n[bold red]❌ Pedido no encontrado[/bold red]")

def buscar_pedido():
    """Busca un pedido por código o código de cliente"""
    datos_pedidos = cargar_pedidos()
    datos_detalles = cargar_detalles_pedidos()
    
    if not datos_pedidos["pedidos"]:
        console.print("\n[bold yellow]⚠ No hay pedidos registrados[/bold yellow]")
        return
    
    busqueda = input("\nIngrese código del pedido o código del cliente: ").lower()
    
    # Creamos la tabla para mostrar resultados
    tabla = Table(title="Resultados de la Búsqueda")
    tabla.add_column("Código", style="cyan")
    tabla.add_column("Cliente", style="green")
    tabla.add_column("Fecha", style="yellow")
    tabla.add_column("Estado", style="magenta")
    tabla.add_column("Total", justify="right")
    
    encontrados = False
    for pedido in datos_pedidos["pedidos"]:
        if (busqueda in pedido["codigo_pedido"].lower() or 
            busqueda in pedido["codigo_cliente"].lower()):
            tabla.add_row(
                pedido["codigo_pedido"],
                pedido["codigo_cliente"],
                pedido["fecha_pedido"],
                pedido["estado"],
                f"${pedido['total']:.2f}"
            )
            encontrados = True
    
    if encontrados:
        console.print(tabla)
        if input("\n¿Desea ver los detalles de algún pedido? (s/n): ").lower() == 's':
            codigo = input("Ingrese el código del pedido: ")
            mostrar_detalles_pedido(codigo, datos_detalles)
    else:
        console.print("\n[bold yellow]⚠ No se encontraron pedidos[/bold yellow]")

def editar_pedido():
    """Edita un pedido existente"""
    datos_pedidos = cargar_pedidos()
    datos_detalles = cargar_detalles_pedidos()
    
    if not datos_pedidos["pedidos"]:
        console.print("\n[bold yellow]⚠ No hay pedidos registrados[/bold yellow]")
        return
    
    codigo = input("\nIngrese el código del pedido a editar: ")
    
    # Buscamos el pedido
    for i, pedido in enumerate(datos_pedidos["pedidos"]):
        if pedido["codigo_pedido"] == codigo:
            # Pedimos el nuevo estado
            console.print("\n[bold cyan]Estados disponibles:[/bold cyan]")
            console.print("1. Pendiente")
            console.print("2. En proceso")
            console.print("3. Entregado")
            
            opcion = input("\nSeleccione el nuevo estado (1-3): ")
            if opcion == "1":
                pedido["estado"] = "pendiente"
            elif opcion == "2":
                pedido["estado"] = "en_proceso"
            elif opcion == "3":
                pedido["estado"] = "entregado"
            else:
                console.print("\n[bold red]❌ Opción no válida[/bold red]")
                return
            
            # Guardamos los cambios
            guardar_pedidos(datos_pedidos)
            console.print("\n[bold green]✅ Pedido editado exitosamente![/bold green]")
            return
    
    console.print("\n[bold red]❌ Pedido no encontrado[/bold red]")

def eliminar_pedido():
    """Elimina un pedido del sistema"""
    datos_pedidos = cargar_pedidos()
    datos_detalles = cargar_detalles_pedidos()
    
    if not datos_pedidos["pedidos"]:
        console.print("\n[bold yellow]⚠ No hay pedidos registrados[/bold yellow]")
        return
    
    codigo = input("\nIngrese el código del pedido a eliminar: ")
    
    # Buscamos y eliminamos el pedido
    for i, pedido in enumerate(datos_pedidos["pedidos"]):
        if pedido["codigo_pedido"] == codigo:
            confirmacion = input("¿Está seguro de eliminar este pedido? (s/n): ").lower()
            if confirmacion == 's':
                # Eliminamos el pedido
                datos_pedidos["pedidos"].pop(i)
                # Eliminamos los detalles
                for j, detalle in enumerate(datos_detalles["detalles_pedidos"]):
                    if detalle["codigo_pedido"] == codigo:
                        datos_detalles["detalles_pedidos"].pop(j)
                        break
                
                # Guardamos los cambios
                guardar_pedidos(datos_pedidos)
                guardar_detalles_pedidos(datos_detalles)
                console.print("\n[bold green]✅ Pedido eliminado exitosamente![/bold green]")
            return
    
    console.print("\n[bold red]❌ Pedido no encontrado[/bold red]")

def gestionar_pedidos(datos_productos):
    """Gestiona el menú de pedidos"""
    while True:
        opcion = mostrar_menu_pedidos()
        
        if opcion == "1":
            crear_pedido(datos_productos)
        elif opcion == "2":
            listar_pedidos()
        elif opcion == "3":
            buscar_pedido()
        elif opcion == "4":
            editar_pedido()
        elif opcion == "5":
            eliminar_pedido()
        elif opcion == "6":
            break
        else:
            console.print("\n[bold yellow]⚠ Opción no válida[/bold yellow]") 