#!/bin/python3
# Creator: PatxaSec
import argparse
import random
import requests
from bs4 import BeautifulSoup
import re
from colorama import init, Fore, Style
import unidecode
import os

init()

VERDE = Fore.GREEN
AZUL = Fore.BLUE
PURPLE = Fore.MAGENTA
AMARILLO = Fore.YELLOW
ROJO = Fore.RED
NORMAL = Style.RESET_ALL
MAQUINAS_HECHAS_FILENAME = "maquinas_hechas.txt"
URL = 'https://dockerlabs.es'

BANNERS = [
    '''
    ██████╗  ██████╗  ██████╗██╗  ██╗███████╗██████╗ ██╗      █████╗ ██████╗ ███████╗     ██████╗██╗     ██╗
    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝    ██╔════╝██║     ██║
    ██║  ██║██║   ██║██║     █████╔╝ █████╗  ██████╔╝██║     ███████║██████╔╝███████╗    ██║     ██║     ██║
    ██║  ██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗██║     ██╔══██║██╔══██╗╚════██║    ██║     ██║     ██║
    ██████╔╝╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║███████╗██║  ██║██████╔╝███████║    ╚██████╗███████╗██║
    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝     ╚═════╝╚══════╝╚═╝v2.0
    Made with LOVE by @PatxaSec
    ''',
    f'    Para ver WriteUps visita: {URL} \n',
    f'    Para aprender, entra en https://elrincondelhacker.es/ \n'
]

DIFICULTADES = ['muy facil', 'facil', 'medio', 'dificil']

def quitar_colores():
    global VERDE, AZUL, PURPLE, AMARILLO, ROJO, NORMAL
    VERDE = AZUL = PURPLE = AMARILLO = ROJO = NORMAL = ''

def leer_maquinas_hechas(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as file:
        return set(line.strip().lower() for line in file)

def escribir_maquina_hecha(filename, maquina):
    with open(filename, "a") as file:
        file.write(maquina.lower() + "\n")

def obtener_datos():
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"{ROJO}[x] Error al acceder a la página: {response.status_code}{NORMAL}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find_all("div", class_=lambda x: x and "item" in x.split())

def procesar_maquinas(docker_rows):
    def obtener_elemento_onclick(text, index):
        if text is None:
            return 'N/A'
        try:
            elementos = text.split('(')[1].split(')')[0].split(',')
            return elementos[index].strip().strip("'").strip('"')
        except (IndexError, AttributeError):
            return 'N/A'
    machines = []
    for row in docker_rows:
        name = row.find("span").find("strong")
        difficulty = row.find("span", class_="badge")
        size = row.find("span", class_="size").find("strong")
        download = row.find("button", class_="download")
        download_onclick = download.attrs.get("onclick") if download else None
        onclick_text = row.attrs.get('onclick')
        creador_text = 'N/A'
        if onclick_text:
            creador_text = unidecode.unidecode(obtener_elemento_onclick(onclick_text, 3))
        if creador_text == 'N/A' and name:
            onclick_text = name.attrs.get('onclick')
            creador_text = unidecode.unidecode(obtener_elemento_onclick(onclick_text, 3))
        name_text = name.get_text(strip=True) if name else 'N/A'
        difficulty_text = unidecode.unidecode(difficulty.get_text(strip=True)) if difficulty else 'N/A'
        size_text = size.get_text(strip=True) if size else 'N/A'
        download_text = re.search(r"'([^']+)'", download_onclick).group(1) if download_onclick else 'N/A'
        machines.append((name_text.lower(), difficulty_text.lower(), download_text, size_text, creador_text.lower()))
    return machines

def imprimir_banner():
    for banner in BANNERS:
        print(f'{AZUL}{banner}{NORMAL}')

def listar_maquinas(maquinas, dificultad=None):
    for dif in (dificultad if dificultad else DIFICULTADES):
        filtered_machines = [machine for machine in maquinas if machine[1] == dif]
        if filtered_machines:
            print()
            print(f"{VERDE}{dif.title()}{NORMAL}")
            print()
            contador = 0
            for machine in filtered_machines:
                if machine[0] in maquinas_hechas:
                    print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()} {AMARILLO} Pwn3d!{NORMAL}")
                else:
                    print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()}")
                print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
                print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
                print(f"{AZUL}Creador:{NORMAL} {machine[4].title()}")
                print()
                contador += 1
            print()
            print(f'Nº de máquinas de dificultad {dif.title()}: {contador}')
            print()
        else:
            print(f"{AMARILLO}No hay máquinas de dificultad {dif.title()}.{NORMAL}")
        print()

def listar_maquinas_por_creador(maquinas):
    maquinas_por_creador = {}
    for machine in maquinas:
        if machine[4] not in maquinas_por_creador:
            maquinas_por_creador[machine[4]] = []
        maquinas_por_creador[machine[4]].append(machine)

    for creador, machines in maquinas_por_creador.items():
        print()
        print(f"{VERDE}Creador: {creador.title()}{NORMAL}\n")
        contador = 0
        for machine in machines:
            print(f"{PURPLE}Dificultad:{NORMAL} {machine[1]}")
            if machine[0] in maquinas_hechas:
                print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()} {AMARILLO} Pwn3d!{NORMAL}")
            else:
                print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()}")
            print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
            print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
            print()
            contador += 1
        print('=========================================================')
        print(f'Nº de máquinas creadas por {creador.title()}: {contador}')
        print()

def listar_maquinas_hechas(maquinas, maquinas_hechas):
    maquinas_por_dificultad = {dif: [] for dif in DIFICULTADES}
    contador_por_dificultad = {dif: 0 for dif in DIFICULTADES}
    for machine in maquinas:
        if machine[0] in maquinas_hechas:
            maquinas_por_dificultad[machine[1]].append(machine)
            contador_por_dificultad[machine[1]] += 1
    for dif, machines in maquinas_por_dificultad.items():
        if machines:
            print()
            print(f"{VERDE}{dif.title()}{NORMAL}\n")
            for machine in machines:
                print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()}")
                print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
                print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
                print(f"{AZUL}Creador:{NORMAL} {machine[4].title()}")
                print()
            print(f'Nº de máquinas hechas de dificultad {dif.title()}: {contador_por_dificultad[dif]}')
            print()

def listar_maquinas_pendientes(maquinas, maquinas_hechas):
    maquinas_por_dificultad = {dif: [] for dif in DIFICULTADES}
    contador_por_dificultad = {dif: 0 for dif in DIFICULTADES}
    for machine in maquinas:
        if machine[0] not in maquinas_hechas:
            maquinas_por_dificultad[machine[1]].append(machine)
            contador_por_dificultad[machine[1]] += 1
    for dif, machines in maquinas_por_dificultad.items():
        if machines:
            print()
            print(f"{VERDE}{dif.title()}{NORMAL}\n")
            for machine in machines:
                print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()}")
                print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
                print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
                print(f"{AZUL}Creador:{NORMAL} {machine[4].title()}")
                print()
            print(f'Nº de máquinas pendientes de dificultad {dif.title()}: {contador_por_dificultad[dif]}')
            print()

def mostrar_estadisticas(maquinas, maquinas_hechas):
    total_maquinas = len(maquinas)
    total_hechas = len(maquinas_hechas)
    total_pendientes = total_maquinas - total_hechas

    maquinas_por_dificultad = {dif: 0 for dif in DIFICULTADES}
    hechas_por_dificultad = {dif: 0 for dif in DIFICULTADES}
    maquinas_por_creador = {}
    maquinas_hechas_por_creador = {}

    for maquina in maquinas:
        nombre, dificultad, download_text, size_text, creador = maquina
        maquinas_por_dificultad[dificultad] += 1

        if creador not in maquinas_por_creador:
            maquinas_por_creador[creador] = 0
            maquinas_hechas_por_creador[creador] = 0
        maquinas_por_creador[creador] += 1

        if nombre in maquinas_hechas:
            hechas_por_dificultad[dificultad] += 1
            maquinas_hechas_por_creador[creador] += 1

    print(f"\n{VERDE}Estadísticas generales:{NORMAL}\n")
    print(f"{AZUL}Total de máquinas disponibles:{NORMAL} {total_maquinas}")
    print(f"{AZUL}Total de máquinas hechas:{NORMAL} {total_hechas}")
    print(f"{AZUL}Total de máquinas pendientes:{NORMAL} {total_pendientes}\n")

    print(f"\n{VERDE}Por creador:{NORMAL}\n")
    barra_ancho = 40  
    ancho_nombre = 20  

    def truncar_nombre(nombre, ancho_maximo):
        if len(nombre) > ancho_maximo:
            return nombre[:ancho_maximo - 3] + '...'
        return nombre

    for creador, total in maquinas_por_creador.items():
        realizadas = maquinas_hechas_por_creador[creador]
        porcentaje = (realizadas / total) * 100
        barra_completada = int((realizadas / total) * barra_ancho)
        barra_pendiente = barra_ancho - barra_completada

        bar_completed = f"{VERDE}{'█' * barra_completada}{NORMAL}"
        bar_pending = f"{PURPLE}{'░' * barra_pendiente}{NORMAL}"

        nombre_truncado = truncar_nombre(creador.title(), ancho_nombre)
        print(f"{nombre_truncado:<{ancho_nombre}} {bar_completed}{bar_pending} {realizadas}/{total} ({porcentaje:.2f}%)")

    print(f"\n{VERDE}Por dificultad:{NORMAL}\n")
    ancho_dificultad = 15  

    for dif in DIFICULTADES:
        total = maquinas_por_dificultad[dif]
        hechas = hechas_por_dificultad[dif]

        barra_completada = int((hechas / total) * barra_ancho) if total > 0 else 0
        barra_pendiente = barra_ancho - barra_completada

        bar_completed = f"{VERDE}{'█' * barra_completada}{NORMAL}"
        bar_pending = f"{PURPLE}{'░' * barra_pendiente}{NORMAL}"

        dificultad_truncada = truncar_nombre(dif.title(), ancho_dificultad)
        print(f"{dificultad_truncada:<{ancho_dificultad}} {bar_completed}{bar_pending} {hechas}/{total} ({(hechas / total) * 100:.2f}% Hechas)")

    dificultad_fav = max(hechas_por_dificultad, key=hechas_por_dificultad.get)
    print(f"\n{VERDE}Dificultad más realizada:{NORMAL} {dificultad_fav.title()}\n")


def buscar_maquina_por_nombre(maquinas, nombre):
    found_machine = next((machine for machine in maquinas if machine[0] == nombre.lower()), None)
    if found_machine:
        print(f"{VERDE}{found_machine[1].title()}{NORMAL}")
        print()
        if found_machine[0] in maquinas_hechas:
            print(f"{AZUL}Nombre:{NORMAL} {found_machine[0].title()}{AMARILLO} Pwn3d!{NORMAL}")
        else:
            print(f"{AZUL}Nombre:{NORMAL} {found_machine[0].title()}")
        print(f"{PURPLE}Tamaño de descarga:{NORMAL} {found_machine[3]}")
        print(f"{AZUL}Creador:{NORMAL} {found_machine[4].title()}")
        print(f"{PURPLE}Link de descarga:{NORMAL} {found_machine[2]}")
        print()
    else:
        if nombre.lower() in maquinas_hechas:
            print(f"{AMARILLO}La máquina '{nombre}' está marcada como hecha, pero no se encuentra en la lista actual de máquinas.{NORMAL}")
        else:
            print(f"{AMARILLO}No hay ninguna máquina con el nombre de {nombre}.{NORMAL}")

def buscar_maquinas_por_creador(maquinas, creador):
    filtered_machines = [machine for machine in maquinas if machine[4] == creador.lower()]
    if filtered_machines:
        print(f"{VERDE} Máquinas creadas por {creador.title()}{NORMAL}\n")
        contador = 0
        for machine in filtered_machines:
            print(f"{PURPLE}Dificultad:{NORMAL} {machine[1].title()}")
            if machine[0] in maquinas_hechas:
                print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()} {AMARILLO} Pwn3d!{NORMAL}")
            else:
                print(f"{AZUL}Nombre:{NORMAL} {machine[0].title()}")
            print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
            print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
            print(f"{AZUL}Creador:{NORMAL} {machine[4].title()}")
            print()
            contador += 1
        print(f'Nº de máquinas creadas por {creador.title()}: {contador}')
        print()
    else:
        print(f"{AMARILLO}No hay máquinas creadas por {creador}.{NORMAL}")

def seleccionar_maquina_aleatoria(maquinas):
    maquinas_disponibles = [machine for machine in maquinas if machine[0] not in maquinas_hechas]
    if not maquinas_disponibles:
        print(f"{AMARILLO}No hay máquinas disponibles para seleccionar aleatoriamente.{NORMAL}")
    else:
        print(f"{VERDE} Máquina seleccionada aleatoriamente:{NORMAL}")
        print(f"{AZUL}Nombre:{NORMAL} {maquinas_disponibles[0].title()}")
        print(f"{PURPLE}Dificultad:{NORMAL} {maquinas_disponibles[1].title()}")
        print(f"{PURPLE}Tamaño de descarga:{NORMAL} {maquinas_disponibles[3]}")
        print(f"{PURPLE}Link de descarga:{NORMAL} {maquinas_disponibles[2]}")
        print(f"{AZUL}Creador:{NORMAL} {maquinas_disponibles[4].title()}")

def manejar_argumentos(args, maquinas):
    if args.dificultad:
        filtered_machines = [machine for machine in maquinas if machine[1] == args.dificultad.lower()]
        if args.nombre_creador:
            filtered_machines = [machine for machine in maquinas if machine[1] == args.dificultad.lower() and machine[4] == args.nombre_creador.lower()]
            if args.random:
                available_machines = [machine for machine in filtered_machines if machine[0] not in maquinas_hechas]
                if available_machines:
                    random_machine = random.choice(available_machines)
                    print(f"{VERDE}La máquina de dificultad {random_machine[1].title()} creada por {args.nombre_creador.title()} que te ha tocado es:{NORMAL}")
                    imprimir_info_maquina(random_machine, args.nombre_creador)
                else:
                    print(f"{AMARILLO}No hay máquinas del creador {args.nombre_creador} disponibles.{NORMAL}")
            elif filtered_machines:
                print(f"{VERDE} Máquinas de dificultad {args.dificultad.title()} creadas por {args.nombre_creador.title()}{NORMAL}\n")
                for machine in filtered_machines:
                    imprimir_info_maquina(machine, args.nombre_creador)
            else:
                print(f"{AMARILLO}No hay máquinas de dificultad {args.dificultad.title()} creadas por {args.nombre_creador.title()}.{NORMAL}")
        elif args.random:
            available_machines = [machine for machine in filtered_machines if machine[0] not in maquinas_hechas]
            if available_machines:
                random_machine = random.choice(available_machines)
                print(f"{VERDE}La máquina de dificultad {random_machine[1].title()} que te ha tocado es:{NORMAL}")
                imprimir_info_maquina(random_machine, args.dificultad)
            else:
                print(f"{AMARILLO}No hay máquinas de dificultad {args.dificultad} disponibles.{NORMAL}")
        else:
            listar_maquinas(maquinas, [args.dificultad.lower()])
    elif args.Done:
        marcar_maquina_hecha(args.Done.lower())
    elif args.pwn3d:
        listar_maquinas_hechas(maquinas, maquinas_hechas)
    elif args.no_pwn3d:
        listar_maquinas_pendientes(maquinas, maquinas_hechas)
    elif args.estadisticas:
        mostrar_estadisticas(maquinas, maquinas_hechas)
    elif args.nombre:
        buscar_maquina_por_nombre(maquinas, args.nombre.lower())
    elif args.nombre_creador:
        filtered_machines = [machine for machine in maquinas if machine[4] == args.nombre_creador.lower()]
        if args.random:
            available_machines = [machine for machine in filtered_machines if machine[0] not in maquinas_hechas]
            if available_machines:
                random_machine = random.choice(available_machines)
                print(f"{VERDE}La máquina de dificultad {random_machine[1].title()} que te ha tocado creada por {args.nombre_creador.title()} es:{NORMAL}")
                imprimir_info_maquina(random_machine, args.nombre_creador)
            else:
                print(f"{AMARILLO}No hay máquinas del creador {args.nombre_creador} disponibles.{NORMAL}")
        else:
            buscar_maquinas_por_creador(maquinas, args.nombre_creador.lower())
    elif args.random:
        available_machines = [machine for machine in maquinas if machine[0] not in maquinas_hechas]
        if available_machines:
            random_machine = random.choice(available_machines)
            seleccionar_maquina_aleatoria(random_machine)
        else:
            print(f"{AMARILLO}No hay máquinas disponibles.{NORMAL}")
    elif args.creador:
        listar_maquinas_por_creador(maquinas)
    else:
        listar_maquinas(maquinas)

def imprimir_info_maquina(maquina, info):
    if info in DIFICULTADES:
        print(f"{AZUL}Nombre:{NORMAL} {maquina[0].title()}")
        print(f"{PURPLE}Tamaño de descarga:{NORMAL} {maquina[3]}")
        print(f"{PURPLE}Link de descarga:{NORMAL} {maquina[2]}")
        print(f"{AZUL}Creador:{NORMAL} {maquina[4].title()}")
        print(f"{PURPLE}Dificultad:{NORMAL} {maquina[1].title()}")
        print()
    elif info.lower() in maquina[4].lower():
        print(f"{PURPLE}Dificultad:{NORMAL} {maquina[1].title()}")
        print(f"{AZUL}Nombre:{NORMAL} {maquina[0].title()}")
        print(f"{PURPLE}Tamaño de descarga:{NORMAL} {maquina[3]}")
        print(f"{PURPLE}Link de descarga:{NORMAL} {maquina[2]}")
        print(f"{AZUL}Creador:{NORMAL} {maquina[4].title()}")
        print()
    else:
        print(f"{VERDE} La máquina de {info.title()} que te ha tocado es:{NORMAL}")
        print(f"{AZUL}Nombre:{NORMAL} {maquina[0].title()}")
        print(f"{PURPLE}Tamaño de descarga:{NORMAL} {maquina[3]}")
        print(f"{PURPLE}Link de descarga:{NORMAL} {maquina[2]}")
        print(f"{PURPLE}Dificultad:{NORMAL} {maquina[1].title()}")
        print(f"{AZUL}Creador:{NORMAL} {maquina[4].title()}")
        print()

def marcar_maquina_hecha(maquina):
    if maquina in maquinas_hechas:
        print(f"{AMARILLO}La máquina '{maquina}' ya está marcada como hecha.{NORMAL}")
    elif any(maquina == m[0] for m in maquinas):
        escribir_maquina_hecha(MAQUINAS_HECHAS_FILENAME, maquina)
        print(f"{VERDE} Máquina '{maquina}' marcada como hecha.{NORMAL}")
    else:
        print(f"{AMARILLO}La máquina '{maquina}' no existe.{NORMAL}")
    exit()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Busca tu máquina de Dockerlabs.')
    parser.add_argument('-d', '--dificultad', help="Filtrar por dificultad. ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']")
    parser.add_argument('-r', '--random', action='store_true', help='Máquina aleatoria.')
    parser.add_argument('-n', '--nombre', help='Buscar una máquina concreta.')
    parser.add_argument('-p', '--pwn3d', action='store_true', help='Listar todas las maquinas marcadas como hechas')
    parser.add_argument('-np', '--no-pwn3d', action='store_true', help='Listar todas las maquinas pendientes')
    parser.add_argument("-s", "--estadisticas" , action="store_true", help="Muestra estadísticas de las máquinas.")
    parser.add_argument('-nb', '--no-banner', action='store_true', help='Eliminar el banner del output.')
    parser.add_argument('-D', '--Done', help='Marcar una máquina como hecha.')
    parser.add_argument('-c', '--creador', action='store_true', help='Listar máquinas por creador.')
    parser.add_argument('-nc', '--nombre_creador', help='Buscar máquinas por nombre de creador.')
    parser.add_argument('--no-colors', action='store_true', help='Eliminar colores del output.')
    args = parser.parse_args()
    maquinas_hechas = leer_maquinas_hechas(MAQUINAS_HECHAS_FILENAME)
    docker_rows = obtener_datos()
    if docker_rows:
        maquinas = procesar_maquinas(docker_rows)
        maquinas_por_hacer = [machine for machine in maquinas if machine[0] not in maquinas_hechas]
        if args.no_colors:
            quitar_colores()
        if not args.no_banner:
            imprimir_banner()
        manejar_argumentos(args, maquinas)
    print(f"Agradecimientos a {AZUL}@elpingüinodemario{NORMAL} por crear {PURPLE}{URL}{NORMAL} y darnos otra forma de jugar.")
