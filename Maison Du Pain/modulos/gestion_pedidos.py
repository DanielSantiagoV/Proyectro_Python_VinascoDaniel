"""
Módulo para la gestión de pedidos
Maneja operaciones CRUD para pedidos de la panadería
"""
from rich.console import Console
from rich.table import Table
from datetime import datetime
from modulos.gestion_archivos import cargar_pedidos, cargar_detalles_pedidos, guardar_pedidos, guardar_detalles_pedidos, cargar_datos, guardar_datos

# Instancia de consola para la visualización
console = Console()

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
        # Mostramos la lista de productos disponibles
        console.print("\n[bold cyan]=== PRODUCTOS DISPONIBLES ===[/bold cyan]")
        tabla = Table(title="📦 Catálogo de Productos")
        tabla.add_column("Código", style="cyan", justify="center")
        tabla.add_column("Nombre", style="green", justify="center")
        tabla.add_column("Stock", justify="center")
        tabla.add_column("Precio ($)", justify="center")
        
        for producto in datos_productos["productos"]:
            tabla.add_row(
                producto["codigo_producto"],
                producto["nombre"],
                str(producto["cantidad_en_stock"]),
                f"{producto['precio_venta']:.2f}"
            )
        console.print(tabla)
        
        codigo_producto = input("\nCódigo del producto (o 'fin' para terminar): ")
        if codigo_producto.lower() == 'fin':
            break
        
        # Buscamos el producto
        producto_encontrado = None
        for producto in datos_productos["productos"]:
            if producto["codigo_producto"].lower() == codigo_producto.lower():
                producto_encontrado = producto
                break
        
        if not producto_encontrado:
            console.print("\n[bold red]❌ Producto no encontrado. Por favor, use uno de los códigos mostrados en la tabla.[/bold red]")
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
    guardar_datos(datos_productos)  # Guardamos también los cambios en el stock
    
    console.print("\n[bold green]✅ Pedido creado exitosamente![/bold green]")

def listar_pedidos():
    """Muestra todos los pedidos en una tabla"""
    datos_pedidos = cargar_pedidos()
    datos_detalles = cargar_detalles_pedidos()
    
    if not datos_pedidos["pedidos"]:
        console.print("\n[bold yellow]⚠ No hay pedidos registrados[/bold yellow]")
        return
    
    # Creamos la tabla
    tabla = Table(title="📋 Lista de Pedidos")
    tabla.add_column("Código", style="cyan", justify="center")
    tabla.add_column("Cliente", style="green", justify="center")
    tabla.add_column("Fecha", style="yellow", justify="center")
    tabla.add_column("Estado", style="magenta", justify="center")
    tabla.add_column("Total", justify="center")
    
    # Agregamos los pedidos a la tabla
    for pedido in datos_pedidos["pedidos"]:
        tabla.add_row(
            pedido["codigo_pedido"],
            pedido["codigo_cliente"],
            pedido["fecha_pedido"],
            pedido["estado"],
            f"${pedido['total']:.2f}"
        )
    
    console.print("\n📋 --- PEDIDOS DE LA PANADERÍA ---")
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
            tabla.add_column("Línea", justify="center")
            tabla.add_column("Producto", style="cyan", justify="center")
            tabla.add_column("Cantidad", justify="center")
            tabla.add_column("Precio Unit.", justify="center")
            tabla.add_column("Subtotal", justify="center")
            
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
    tabla.add_column("Código", style="cyan", justify="center")
    tabla.add_column("Cliente", style="green", justify="center")
    tabla.add_column("Fecha", style="yellow", justify="center")
    tabla.add_column("Estado", style="magenta", justify="center")
    tabla.add_column("Total", justify="center")
    
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
    datos_productos = cargar_datos()
    
    if not datos_pedidos["pedidos"]:
        console.print("\n[bold yellow]⚠ No hay pedidos registrados[/bold yellow]")
        return
    
    codigo = input("\nIngrese el código del pedido a editar: ")
    
    # Buscamos el pedido
    pedido_index = None
    pedido_encontrado = None
    for i, pedido in enumerate(datos_pedidos["pedidos"]):
        if pedido["codigo_pedido"] == codigo:
            pedido_index = i
            pedido_encontrado = pedido
            break
    
    if pedido_encontrado is None:
        console.print("\n[bold red]❌ Pedido no encontrado[/bold red]")
        return
        
    # Buscamos los detalles del pedido
    detalle_pedido_index = None
    detalle_pedido = None
    for i, detalle in enumerate(datos_detalles["detalles_pedidos"]):
        if detalle["codigo_pedido"] == codigo:
            detalle_pedido_index = i
            detalle_pedido = detalle
            break
    
    if detalle_pedido is None:
        console.print("\n[bold red]❌ Detalles del pedido no encontrados[/bold red]")
        return
    
    # Mostramos los detalles actuales del pedido
    mostrar_detalles_pedido(codigo, datos_detalles)
    
    # Menú de edición
    console.print("\n[bold cyan]=== OPCIONES DE EDICIÓN ===[/bold cyan]")
    console.print("1️⃣ Cambiar estado del pedido")
    console.print("2️⃣ Agregar productos al pedido")
    console.print("3️⃣ Cambiar cantidad de un producto")
    console.print("4️⃣ Eliminar un producto del pedido")
    
    opcion_edicion = input("\n⚡ Seleccione una opción: ")
    
    # 1. Cambiar estado
    if opcion_edicion == "1":
        console.print("\n[bold cyan]Estados disponibles:[/bold cyan]")
        console.print("1. Pendiente")
        console.print("2. En proceso")
        console.print("3. Entregado")
        
        opcion = input("\nSeleccione el nuevo estado (1-3): ")
        if opcion == "1":
            pedido_encontrado["estado"] = "pendiente"
        elif opcion == "2":
            pedido_encontrado["estado"] = "en_proceso"
        elif opcion == "3":
            pedido_encontrado["estado"] = "entregado"
        else:
            console.print("\n[bold red]❌ Opción no válida[/bold red]")
            return
        
        # Guardamos los cambios
        guardar_pedidos(datos_pedidos)
        console.print("\n[bold green]✅ Estado del pedido actualizado exitosamente![/bold green]")
    
    # 2. Agregar productos
    elif opcion_edicion == "2":
        # Mostramos productos disponibles
        from modulos.gestion_productos import mostrar_lista_productos
        mostrar_lista_productos(datos_productos)
        
        # Agregamos productos al pedido
        while True:
            codigo_producto = input("\nCódigo del producto a agregar (o 'fin' para terminar): ")
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
            if cantidad <= 0:
                console.print("\n[bold red]❌ La cantidad debe ser mayor a cero[/bold red]")
                continue
                
            if cantidad > producto_encontrado["cantidad_en_stock"]:
                console.print("\n[bold red]❌ No hay suficiente stock. Disponible: " + 
                             str(producto_encontrado["cantidad_en_stock"]) + "[/bold red]")
                continue
            
            # Calculamos el subtotal
            subtotal = cantidad * producto_encontrado["precio_venta"]
            
            # Creamos el detalle
            detalle = {
                "numero_linea": len(detalle_pedido["detalles"]) + 1,
                "codigo_producto": producto_encontrado["codigo_producto"],
                "cantidad": cantidad,
                "precio_unidad": producto_encontrado["precio_venta"],
                "subtotal": subtotal
            }
            
            # Actualizamos el stock
            producto_encontrado["cantidad_en_stock"] -= cantidad
            
            # Agregamos el detalle al pedido
            detalle_pedido["detalles"].append(detalle)
            pedido_encontrado["total"] += subtotal
        
        # Guardamos los cambios
        guardar_datos(datos_productos)
        guardar_pedidos(datos_pedidos)
        guardar_detalles_pedidos(datos_detalles)
        console.print("\n[bold green]✅ Productos agregados al pedido exitosamente![/bold green]")
    
    # 3. Cambiar cantidad
    elif opcion_edicion == "3":
        if not detalle_pedido["detalles"]:
            console.print("\n[bold yellow]⚠ Este pedido no tiene productos[/bold yellow]")
            return
        
        numero_linea = int(input("\nIngrese el número de línea del producto a modificar: "))
        
        # Buscamos el detalle
        detalle_encontrado = None
        detalle_index = None
        for i, detalle in enumerate(detalle_pedido["detalles"]):
            if detalle["numero_linea"] == numero_linea:
                detalle_encontrado = detalle
                detalle_index = i
                break
        
        if detalle_encontrado is None:
            console.print("\n[bold red]❌ Línea de producto no encontrada[/bold red]")
            return
        
        # Buscamos el producto para verificar stock
        producto_encontrado = None
        for producto in datos_productos["productos"]:
            if producto["codigo_producto"] == detalle_encontrado["codigo_producto"]:
                producto_encontrado = producto
                break
        
        if producto_encontrado is None:
            console.print("\n[bold red]❌ Producto no encontrado en inventario[/bold red]")
            return
        
        # Mostramos la cantidad actual
        console.print(f"\nProducto: {detalle_encontrado['codigo_producto']}")
        console.print(f"Cantidad actual: {detalle_encontrado['cantidad']}")
        console.print(f"Stock disponible: {producto_encontrado['cantidad_en_stock'] + detalle_encontrado['cantidad']}")
        
        # Pedimos la nueva cantidad
        nueva_cantidad = int(input("\nNueva cantidad: "))
        if nueva_cantidad <= 0:
            console.print("\n[bold red]❌ La cantidad debe ser mayor a cero[/bold red]")
            return
        
        # Verificamos stock disponible (stock actual + cantidad anterior)
        stock_disponible = producto_encontrado["cantidad_en_stock"] + detalle_encontrado["cantidad"]
        if nueva_cantidad > stock_disponible:
            console.print(f"\n[bold red]❌ No hay suficiente stock. Disponible: {stock_disponible}[/bold red]")
            return
        
        # Actualizamos el stock
        diferencia = nueva_cantidad - detalle_encontrado["cantidad"]
        producto_encontrado["cantidad_en_stock"] -= diferencia
        
        # Actualizamos el total del pedido
        pedido_encontrado["total"] -= detalle_encontrado["subtotal"]
        
        # Actualizamos el detalle
        detalle_encontrado["cantidad"] = nueva_cantidad
        detalle_encontrado["subtotal"] = nueva_cantidad * detalle_encontrado["precio_unidad"]
        
        # Actualizamos el total del pedido
        pedido_encontrado["total"] += detalle_encontrado["subtotal"]
        
        # Guardamos los cambios
        guardar_datos(datos_productos)
        guardar_pedidos(datos_pedidos)
        guardar_detalles_pedidos(datos_detalles)
        console.print("\n[bold green]✅ Cantidad actualizada exitosamente![/bold green]")
    
    # 4. Eliminar producto
    elif opcion_edicion == "4":
        if not detalle_pedido["detalles"]:
            console.print("\n[bold yellow]⚠ Este pedido no tiene productos[/bold yellow]")
            return
        
        numero_linea = int(input("\nIngrese el número de línea del producto a eliminar: "))
        
        # Buscamos el detalle
        detalle_encontrado = None
        detalle_index = None
        for i, detalle in enumerate(detalle_pedido["detalles"]):
            if detalle["numero_linea"] == numero_linea:
                detalle_encontrado = detalle
                detalle_index = i
                break
        
        if detalle_encontrado is None:
            console.print("\n[bold red]❌ Línea de producto no encontrada[/bold red]")
            return
        
        # Buscamos el producto para devolver stock
        for producto in datos_productos["productos"]:
            if producto["codigo_producto"] == detalle_encontrado["codigo_producto"]:
                # Devolvemos el stock
                producto["cantidad_en_stock"] += detalle_encontrado["cantidad"]
                break
        
        # Actualizamos el total del pedido
        pedido_encontrado["total"] -= detalle_encontrado["subtotal"]
        
        # Eliminamos el detalle
        detalle_pedido["detalles"].pop(detalle_index)
        
        # Renumeramos las líneas
        for i, detalle in enumerate(detalle_pedido["detalles"]):
            detalle["numero_linea"] = i + 1
        
        # Guardamos los cambios
        guardar_datos(datos_productos)
        guardar_pedidos(datos_pedidos)
        guardar_detalles_pedidos(datos_detalles)
        console.print("\n[bold green]✅ Producto eliminado del pedido exitosamente![/bold green]")
    
    else:
        console.print("\n[bold yellow]⚠ Opción no válida[/bold yellow]")
        return
        
    # Mostramos los detalles actualizados
    console.print("\n[bold cyan]=== DETALLES ACTUALIZADOS DEL PEDIDO ===[/bold cyan]")
    mostrar_detalles_pedido(codigo, datos_detalles)

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