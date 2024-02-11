import pyfiglet
from prettytable import PrettyTable
import getpass

def es_entero(cadena):
    if not cadena:
        return False
    try:
        int(cadena)
        return True
    except ValueError:
        return False 


def mostrar_menu():
    arte_ascii = pyfiglet.figlet_format("+ Hospital San Vicente +")
    print(arte_ascii)
    titulo_menu = "**Ingrese el numero correspondiente a la opcion deseada**"
    opciones = [
    "1. Ingresar nuevo paciente",
    "2. Consultar historia clinica de un paciente",
    "3. Generar reportes e indicadores",
    "4. Salir"
    ]

    # Crear una tabla para el título y opciones
    tabla = PrettyTable()
    tabla.field_names = [titulo_menu]
    for opcion in opciones:
        tabla.add_row([opcion])

    # Imprimir la tabla
    print(tabla)

def iniciar_sesion():
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        contraseña = input("Ingrese su contraseña (solo numeros): ")

        if es_entero(contraseña):
            print("Inicio de sesion exitoso.")
            break
        else:
            print("La contraseña debe contener solo números. Intentelo nuevamente.")

def main():
    print("Bienvenido al sistema de gestion hospitalaria.")
    iniciar_sesion()
    mostrar_menu()

if __name__ == "__main__":
    main()


