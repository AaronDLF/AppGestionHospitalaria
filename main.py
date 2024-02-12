import pyfiglet
from colorama import init, Fore
from prettytable import PrettyTable
import getpass


class Usuario:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Autenticacion:
    def __init__(self):
        self.usuarios_registrados = []
        self.pacientes_registrados = []

    def registrar_usuario(self, username, password):
        nuevo_usuario = Usuario(username, password)
        self.usuarios_registrados.append(nuevo_usuario)


# Instancia de Autenticacion para almacenar pacientes
autenticacion = Autenticacion()


class Paciente:
    def __init__(self, documento, nombre, sexo, fecha_nacimiento, servicio):
        self.documento = documento
        self.nombre = nombre
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.servicio = servicio
        self.historia_clinica = HistoriaClinica()


class HistoriaClinica:
    def __init__(self):
        self.signos_vitales = []
        self.notas_evolucion = []
        self.imagenes_diagnosticas = []
        self.resultados_examenes = []
        self.medicamentos_formulados = []

    def agregar_signos_vitales(
        self, presion_arterial, temperatura, saturacion_o2, frecuencia_respiratoria
    ):
        self.signos_vitales.append(
            {
                "presion_arterial": presion_arterial,
                "temperatura": temperatura,
                "saturacion_o2": saturacion_o2,
                "frecuencia_respiratoria": frecuencia_respiratoria,
            }
        )

    def agregar_nota_evolucion(self, nota):
        self.notas_evolucion.append(nota)

    def agregar_resultado_examen(self, resultado):
        self.resultados_examenes.append(resultado)

    def agregar_medicamento_formulado(self, medicamento):
        self.medicamentos_formulados.append(medicamento)


def es_entero(cadena):
    if not cadena:
        return False
    try:
        int(cadena)
        return True
    except ValueError:
        return False


def ingresar_nuevo_paciente():
    print("Ingrese los datos del nuevo paciente:")

    documento = input("Documento: ")
    nombre = input("Nombre: ")
    sexo = input("Sexo: ")
    fecha_nacimiento = input("Fecha de nacimiento (formato DD/MM/AAAA): ")

    # Preguntar por el servicio y validar la respuesta
    while True:
        servicio = input(
            "Servicio (endocrinologia, cardiologia o nefrologia): "
        ).lower()
        if servicio in ["endocrinologia", "cardiologia", "nefrologia"]:
            break
        else:
            print("Por favor, ingrese un servicio válido.")

    nuevo_paciente = Paciente(documento, nombre, sexo, fecha_nacimiento, servicio)

    # Validar y obtener datos de signos vitales
    while True:
        presion_arterial = input("Presión arterial: ")
        temperatura = input("Temperatura: ")
        saturacion_o2 = input("Saturación O2: ")
        frecuencia_respiratoria = input("Frecuencia respiratoria: ")

        # Validar que los datos ingresados sean números
        if (
            es_entero(presion_arterial)
            and es_entero(temperatura)
            and es_entero(saturacion_o2)
            and es_entero(frecuencia_respiratoria)
        ):
            break
        else:
            print("Por favor, ingrese valores numéricos para los signos vitales.")

    nuevo_paciente.historia_clinica.agregar_signos_vitales(
        presion_arterial, temperatura, saturacion_o2, frecuencia_respiratoria
    )

    # Ingresar notas de evolución con validación
    while True:
        notas_evolucion = input(
            "Notas de evolución (al-alta/ci-cuidados intensivos/cint-cuidados intermedios)//indique alguna de las abreviaturas: "
        ).lower()
        if notas_evolucion in ["al", "ci", "cint"]:
            break
        else:
            print("Por favor, ingrese una opción válida para las notas de evolución.")

    nuevo_paciente.historia_clinica.agregar_nota_evolucion(notas_evolucion)

    # Ingresar los resultados de examen de laboratorio con validación
    while True:
        resultados_lab = input(
            "Resultados de exámenes de laboratorio (si/no) (dependiendo si se detecta o no una enfermedad crónica en el paciente): "
        ).lower()
        if resultados_lab in ["si", "no"]:
            break
        else:
            print(
                "Por favor, ingrese 'si' o 'no' (dependiendo si se detecta o no una enfermedad crónica en el paciente) para los resultados de exámenes de laboratorio."
            )

    nuevo_paciente.historia_clinica.agregar_resultado_examen(resultados_lab)

    # Ingresar los medicamentos formulados
    medicamentos_formulados = input("Medicamentos formulados al paciente: ")
    nuevo_paciente.historia_clinica.agregar_medicamento_formulado(
        medicamentos_formulados
    )

    # Guardar el paciente en la lista de pacientes registrados
    autenticacion.pacientes_registrados.append(nuevo_paciente)

    print("Paciente registrado exitosamente.")


# ////////////////////////////////////////////////////////////////////////
def generar_reportes_indicadores():
    total_camas = 300
    ocupacion_hospitalaria = (
        len(autenticacion.pacientes_registrados) / total_camas * 100
    )

    # Inicializar diccionarios para almacenar estadísticas por servicio
    altas_por_servicio = {}
    pacientes_cronicos_por_servicio = {}
    prescripcion_por_servicio = {}

    for paciente in autenticacion.pacientes_registrados:
        servicio = paciente.servicio

        # Contar altas por servicio
        if "al" in paciente.historia_clinica.notas_evolucion:
            if servicio in altas_por_servicio:
                altas_por_servicio[servicio] += 1
            else:
                altas_por_servicio[servicio] = 1

        # Contar pacientes con enfermedades crónicas por servicio
        if "si" in paciente.historia_clinica.resultados_examenes:
            if servicio in pacientes_cronicos_por_servicio:
                pacientes_cronicos_por_servicio[servicio] += 1
            else:
                pacientes_cronicos_por_servicio[servicio] = 1

        # Almacenar prescripción de medicamentos por servicio
        prescripcion = paciente.historia_clinica.medicamentos_formulados
        if servicio in prescripcion_por_servicio:
            prescripcion_por_servicio[servicio].append(prescripcion)
        else:
            prescripcion_por_servicio[servicio] = [prescripcion]

    # Imprimir resultados
    print(
        Fore.GREEN
        + f"Porcentaje de ocupación hospitalaria: {ocupacion_hospitalaria:.2f}%"
        + Fore.RESET
    )

    print(Fore.GREEN + "Cantidad de altas por servicio:" + Fore.RESET)
    for servicio, altas in altas_por_servicio.items():
        print(f"  {servicio}: {altas}")

    print(
        Fore.GREEN
        + "Cantidad de pacientes con enfermedades crónicas por servicio:"
        + Fore.RESET
    )
    for servicio, pacientes in pacientes_cronicos_por_servicio.items():
        print(f"  {servicio}: {pacientes}")

    print(Fore.GREEN + "Prescripción de medicamentos por servicio:" + Fore.RESET)
    for servicio, prescripcion in prescripcion_por_servicio.items():
        print(f"  {servicio}: {prescripcion}")


# //////////////////////////////////////////////////////////////////////


def mostrar_menu():
    arte_ascii = pyfiglet.figlet_format("+ Hospital San Vicente +")
    print(Fore.RED + arte_ascii + Fore.RESET)
    titulo_menu = "**Ingrese el numero correspondiente a la opcion deseada**"
    opciones = [
        "1. Ingresar nuevo paciente",
        "2. Consultar historia clinica de un paciente",
        "3. Generar reportes e indicadores",
        "4. Salir",
    ]

    # Crear una tabla para el título y opciones
    tabla = PrettyTable()
    tabla.field_names = [titulo_menu]
    for opcion in opciones:
        tabla.add_row([opcion])

    # Imprimir la tabla
    print(tabla)


def consultar_historia_clinica():
    documento_paciente = input("Ingrese el documento del paciente a consultar: ")

    # Buscar el paciente por su documento
    paciente_encontrado = None
    for paciente in autenticacion.pacientes_registrados:
        if paciente.documento == documento_paciente:
            paciente_encontrado = paciente
            break

    if paciente_encontrado:
        # Imprimir la información de la historia clínica del paciente
        print(
            f"\nHistoria clinica del paciente {paciente_encontrado.nombre} (Documento: {paciente_encontrado.documento}):"
        )
        print(f"Servicio: {paciente_encontrado.servicio}")
        print("\nSignos Vitales:")
        for signos in paciente_encontrado.historia_clinica.signos_vitales:
            print(signos)

        print("\nNotas de Evolucion:")
        for nota in paciente_encontrado.historia_clinica.notas_evolucion:
            print(nota)

        print(
            "Recordatorio de siglas: al(alta), ci(cuidados intensivos), cint(cuidados intermedios)"
        )

        print("\nResultados de Exámenes de Laboratorio (¿Existe enfermedad cronica?):")
        for resultado in paciente_encontrado.historia_clinica.resultados_examenes:
            print(resultado)

        print("\nMedicamentos Formulados:")
        for medicamento in paciente_encontrado.historia_clinica.medicamentos_formulados:
            print(medicamento)
    else:
        print("Paciente no encontrado. Verifique el documento ingresado.")


def iniciar_sesion():
    while True:
        print(
            """
        +--------------------------------+
        |    Inicio de sesion de usuario |
        +--------------------------------+
        \n"""
        )
        usuario = input("Usuario => ")
        contraseña = input("Contraseña => ")

        if es_entero(contraseña):
            print("Inicio de sesion exitoso.")
            break
        else:
            print("La contraseña debe contener solo numeros. Intentelo nuevamente.")


def main():
    print("Bienvenido al sistema de gestion hospitalaria del Hospital San Vicente.")
    iniciar_sesion()

    while True:
        mostrar_menu()
        opcion = input("Opcion a ejecutar: ")

        if opcion == "1":
            ingresar_nuevo_paciente()
        elif opcion == "2":
            consultar_historia_clinica()
        elif opcion == "3":
            generar_reportes_indicadores()
        elif opcion == "4":
            print("¡Hasta luego! Gracias por usar el sistema.")
            break
        else:
            print("Opción no valida. Por favor, ingrese un numero del 1 al 4")


if __name__ == "__main__":
    main()
