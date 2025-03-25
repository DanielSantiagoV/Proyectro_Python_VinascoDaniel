"""
Sistema de Gestión de Panadería "Maison du Pain"
Archivo principal para la ejecución del programa
"""
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

from modulos.gestion_archivos import cargar_datos, guardar_datos
from modulos.gestion_productos import gestionar_productos
from modulos.gestion_pedidos import gestionar_pedidos

# Instancia de consola para la visualización
console = Console()

def mostrar_banner():
    """Muestra un banner ASCII con el nombre de la panadería"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  ███╗   ███╗ █████╗ ██╗███████╗ ██████╗ ███╗   ██╗          ║
    ║  ████╗ ████║██╔══██╗██║██╔════╝██╔═══██╗████╗  ██║          ║
    ║  ██╔████╔██║███████║██║███████╗██║   ██║██╔██╗ ██║          ║
    ║  ██║╚██╔╝██║██╔══██║██║╚════██║██║   ██║██║╚██╗██║          ║
    ║  ██║ ╚═╝ ██║██║  ██║██║███████║╚██████╔╝██║ ╚████║          ║
    ║  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝          ║
    ║                                                              ║
    ║    ██████╗ ██╗   ██╗    ██████╗  █████╗ ██╗███╗   ██╗       ║
    ║    ██╔══██╗██║   ██║    ██╔══██╗██╔══██╗██║████╗  ██║       ║
    ║    ██║  ██║██║   ██║    ██████╔╝███████║██║██╔██╗ ██║       ║
    ║    ██║  ██║██║   ██║    ██╔═══╝ ██╔══██║██║██║╚██╗██║       ║
    ║    ██████╔╝╚██████╔╝    ██║     ██║  ██║██║██║ ╚████║       ║
    ║    ╚═════╝  ╚═════╝     ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝       ║
    ║                                                              ║
    ║           Sistema de Gestión de Panadería                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    # Creamos un texto con el banner y lo mostramos en rojo
    text = Text(banner, style="bold red", justify="center")
    console.print(Panel(text, 
                       title="🥐 Bienvenido 🥖", 
                       subtitle="🍰 Sistema de Gestión 🍞",
                       width=90))

def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    console.print("\n[bold cyan]=== MENÚ PRINCIPAL ===[/bold cyan]")
    console.print("1️⃣ Gestión de Productos")
    console.print("2️⃣ Gestión de Pedidos")
    console.print("3️⃣ 👋 Salir")
    return input("\n⚡ Seleccione una opción: ")

def main():
    """Función principal del programa"""
    # Mostrar el banner de bienvenida
    mostrar_banner()
    
    # Cargar datos desde el archivo JSON
    datos = cargar_datos()
    
    # Menú principal
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == "1":
            gestionar_productos(datos)
            # Guardamos los cambios después de gestionar productos
            guardar_datos(datos)
        elif opcion == "2":
            gestionar_pedidos(datos)
            # Guardamos los cambios después de gestionar pedidos
            guardar_datos(datos)
        elif opcion == "3":
            break
        else:
            console.print("\n[bold yellow]⚠ Opción no válida[/bold yellow]")
    
    # Mensaje de despedida
    console.print("\n[bold green]¡Gracias por usar el sistema de Maison du Pain![/bold green]")

if __name__ == "__main__":
    main() 