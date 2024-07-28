#!/bin/python3
#Creator: PatxaSec
import argparse
import random
import requests
from bs4 import BeautifulSoup, Tag
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

banner = '''
    ██████╗  ██████╗  ██████╗██╗  ██╗███████╗██████╗ ██╗      █████╗ ██████╗ ███████╗     ██████╗██╗     ██╗
    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝    ██╔════╝██║     ██║
    ██║  ██║██║   ██║██║     █████╔╝ █████╗  ██████╔╝██║     ███████║██████╔╝███████╗    ██║     ██║     ██║
    ██║  ██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗██║     ██╔══██║██╔══██╗╚════██║    ██║     ██║     ██║
    ██████╔╝╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║███████╗██║  ██║██████╔╝███████║    ╚██████╗███████╗██║
    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝     ╚═════╝╚══════╝╚═╝
    Made with LOVE by @PatxaSec                      Para ver WriteUps visita: http://beta.dockerlabs.es/#/
'''

MAQUINAS_HECHAS_FILENAME = "maquinas_hechas.txt"

# Leer máquinas hechas desde el archivo
def leer_maquinas_hechas():
    if not os.path.exists(MAQUINAS_HECHAS_FILENAME):
        return set()
    with open(MAQUINAS_HECHAS_FILENAME, "r") as file:
        return set(line.strip().lower() for line in file)

# Escribir una máquina hecha en el archivo
def escribir_maquina_hecha(maquina):
    with open(MAQUINAS_HECHAS_FILENAME, "a") as file:
        file.write(maquina.lower() + "\n")

# Argumentos del script
parser = argparse.ArgumentParser(description='Busca tu máquina de Dockerlabs.')
parser.add_argument('-d', '--dificultad', help="Filtrar por dificultad. ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']")
parser.add_argument('-r', '--random', action='store_true', help='Máquina aleatoria.')
parser.add_argument('-n', '--nombre', help='Buscar una máquina concreta.')
parser.add_argument('-nb', '--no-banner', action='store_true', help='Eliminar el banner del output.')
parser.add_argument('-D', '--Done', help='Marcar una máquina como hecha.')
args = parser.parse_args()

url = 'http://beta.dockerlabs.es/#/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    docker_rows = soup.find_all("div", 'item')
    dificultad = [unidecode.unidecode(d).lower() for d in ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']]
    
    if not args.no_banner:
        print(f'{AZUL}{banner}{NORMAL}')
    else:
        print()

    machines = []
    for row in docker_rows:
        name = row.find("span").find("strong")
        difficulty = row.find("span", class_="badge")
        size = row.find("span", class_="size").find("strong")
        download = row.find("button", class_="download").attrs.get("onclick")

        name_text = name.get_text(strip=True) if name and isinstance(name, Tag) else 'N/A'
        difficulty_text = unidecode.unidecode(difficulty.get_text(strip=True)) if difficulty and isinstance(difficulty, Tag) else 'N/A'
        size_text = size.get_text(strip=True) if size and isinstance(size, Tag) else 'N/A'
        download_text = re.search(r"'([^']+)'", download).group(1) if download else 'N/A'

        machines.append((name_text.lower(), difficulty_text.lower(), download_text, size_text))

    maquinas_hechas = leer_maquinas_hechas()
    maquinas_por_hacer = [machine for machine in machines if machine[0] not in maquinas_hechas]

    if args.Done:
        maquina = args.Done.lower()
        if maquina in maquinas_hechas:
            print(f"{AMARILLO}[!] La máquina '{maquina}' ya está marcada como hecha.{NORMAL}")
        elif any(maquina == m[0] for m in machines):
            escribir_maquina_hecha(maquina)
            print(f"{VERDE}[+] Máquina '{maquina}' marcada como hecha.{NORMAL}")
        else:
            print(f"{AMARILLO}[!] La máquina '{maquina}' no existe.{NORMAL}")
        print(f"{VERDE}Agradecimientos a @elpingüinodemario por crear {url} y darnos otra forma de jugar.{NORMAL}")
        exit()

    if args.dificultad:
        filtered_machines = [machine for machine in machines if machine[1] == args.dificultad.lower()] 
        random_filtered_machines = [machines for machines in maquinas_por_hacer if machines[1] == args.dificultad.lower()] 
        if filtered_machines:
            if args.random:
                random_machine = random.choice(random_filtered_machines)
                print(f"{VERDE}[+] La máquina de nivel {random_machine[1].capitalize()} que te ha tocado es:{NORMAL}")
                print(f"{AZUL}Nombre:{NORMAL} {random_machine[0].capitalize()}")
                print(f"{PURPLE}Tamaño de descarga:{NORMAL} {random_machine[3]}")
                print(f"{PURPLE}Link de descarga:{NORMAL} {random_machine[2]}")
                print()
            else:
                print(f"{VERDE}[+] Las máquinas de nivel {args.dificultad.capitalize()} son:{NORMAL}")
                print()
                for machine in filtered_machines:
                    if machine[0] in maquinas_hechas:
                        print(f"{AZUL}Nombre:{NORMAL} {machine[0].capitalize()}{AMARILLO} [!] Hecha!{NORMAL}")
                    else:
                        print(f"{AZUL}Nombre:{NORMAL} {machine[0].capitalize()}")
                    print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
                    print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
                    print()
        else:
            print(f"{AMARILLO}[!] No hay máquinas de dificultad {args.dificultad}.{NORMAL}")
    elif args.nombre:
        found_machine = next((machine for machine in machines if machine[0] == args.nombre.lower()), None)
        if found_machine:
            print(f"{VERDE}[+]======================> {found_machine[1].capitalize()}{NORMAL}")
            print()
            print(f"{AZUL}Nombre:{NORMAL} {found_machine[0].capitalize()}")
            print(f"{PURPLE}Tamaño de descarga:{NORMAL} {found_machine[3]}")
            print(f"{PURPLE}Link de descarga:{NORMAL} {found_machine[2]}")
            if found_machine[0] in maquinas_hechas:
                print(f"{AMARILLO}[!] Esta máquina ya está marcada como hecha.{NORMAL}")
            print()
        else:
            if args.nombre.lower() in maquinas_hechas:
                print(f"{AMARILLO}[!] La máquina '{args.nombre}' está marcada como hecha, pero no se encuentra en la lista actual de máquinas.{NORMAL}")
            else:
                print(f"{AMARILLO}[!] No hay ninguna máquina con el nombre de {args.nombre}.{NORMAL}")
        
    else:
        if args.random:
            if machines:
                random_machine = random.choice(maquinas_por_hacer)
                print(f"{VERDE}[+]======================> {random_machine[1].capitalize()}{NORMAL}")
                print()
                print(f"{AZUL}Nombre:{NORMAL} {random_machine[0].capitalize()}")
                print(f"{PURPLE}Tamaño de descarga:{NORMAL} {random_machine[3]}")
                print(f"{PURPLE}Link de descarga:{NORMAL} {random_machine[2]}")
                print()
            else:
                print(f"{AMARILLO}[!] No hay máquinas disponibles para mostrar.{NORMAL}")
        else:
            for dif in dificultad:
                filtered_machines = [machine for machine in machines if machine[1] == dif]
                if filtered_machines:
                    print(f"{VERDE}[+]======================> {dif.capitalize()}{NORMAL}")
                    print()
                    for machine in filtered_machines:
                        if machine[0] in maquinas_hechas:
                            print(f"{AZUL}Nombre:{NORMAL} {machine[0].capitalize()} {AMARILLO} [!] Hecha!{NORMAL}")
                        else:
                            print(f"{AZUL}Nombre:{NORMAL} {machine[0].capitalize()}")
                        print(f"{PURPLE}Tamaño de descarga:{NORMAL} {machine[3]}")
                        print(f"{PURPLE}Link de descarga:{NORMAL} {machine[2]}")
                        print() 
                else:
                    print(f"{AMARILLO}[!] No hay máquinas de dificultad {dif.capitalize()}.{NORMAL}")
                print()  
    
else:
    print(f"{ROJO}[x] Error al acceder a la página: {response.status_code}{NORMAL}")

print(f"{VERDE}Agradecimientos a @elpingüinodemario por crear {url} y darnos otra forma de jugar.{NORMAL}")
