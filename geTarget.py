import argparse
import random
import requests
from bs4 import BeautifulSoup, Tag
import re
from colorama import init, Fore, Style
import unidecode

init()


VERDE = Fore.GREEN
AZUL = Fore.BLUE
PURPLE = Fore.MAGENTA
AMARILLO = Fore.YELLOW
ROJO = Fore.RED
NORMAL = Style.RESET_ALL

parser = argparse.ArgumentParser(description='Busca tu máquina de Dockerlabs.')
parser.add_argument('-d', '--dificultad', help="Filtrar por dificultad. ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']")
parser.add_argument('-r', '--random', action='store_true', help='Máquina aleatoria.')
parser.add_argument('-n', '--nombre', help='Buscar una máquina concreta.')
args = parser.parse_args()
url = 'http://beta.dockerlabs.es/#/'

response = requests.get(url)


if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    docker_rows = soup.find_all("div", 'item')
    dificultad = [unidecode.unidecode(d).lower() for d in ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']]


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

    if args.dificultad:
        filtered_machines = [machine for machine in machines if machine[1] == args.dificultad.lower()]
        if filtered_machines:
            if args.random:
                random_machine = random.choice(filtered_machines)
                print(f"{VERDE}[+] La máquina de nivel {random_machine[1].capitalize()} que te ha tocado es:{NORMAL}")
                print(f"{AZUL}Nombre: {random_machine[0].capitalize()}{NORMAL}")
                print(f"{PURPLE}Tamaño de descarga: {random_machine[3]}{NORMAL}")
                print(f"{PURPLE}Link de descarga: {random_machine[2]}{NORMAL}")
            else:
                print(f"{VERDE}[+] Las máquinas de nivel {args.dificultad.capitalize()} son:{NORMAL}")
                for machine in filtered_machines:
                    print(f"{AZUL}Nombre: {machine[0].capitalize()}{NORMAL}")
                    print(f"{PURPLE}Tamaño de descarga: {machines[3][3]}{NORMAL}")
                    print(f"{PURPLE}Link de descarga: {machine[2]}{NORMAL}")
        else:
            print(f"{AMARILLO}[!] No hay máquinas de dificultad {args.dificultad}.{NORMAL}")
    elif args.nombre:
        found_machine = next((machine for machine in machines if machine[0] == args.nombre.lower()), None)
        if found_machine:
            print(f"{VERDE}[+]======================> {found_machine[1].capitalize()}{NORMAL}")
            print(f"{AZUL}Nombre: {found_machine[0].capitalize()}{NORMAL}")
            print(f"{PURPLE}Tamaño de descarga: {found_machine[3]}{NORMAL}")
            print(f"{PURPLE}Link de descarga: {found_machine[2]}{NORMAL}")
        else:
            print(f"{AMARILLO}[!] No hay ninguna máquina con el nombre de {args.nombre}.{NORMAL}")
        
    else:
        if args.random:
            random_machine = random.choice(machines)
            print(f"{VERDE}[+]======================> {random_machine[1].capitalize()}{NORMAL}")
            print(f"{AZUL}Nombre: {random_machine[0].capitalize()}{NORMAL}")
            print(f"{PURPLE}Tamaño de descarga: {random_machine[3]}{NORMAL}")
            print(f"{PURPLE}Link de descarga: {random_machine[2]}{NORMAL}")
        else:
            for dif in dificultad:
                filtered_machines = [machine for machine in machines if machine[1] == dif.lower()]
                if filtered_machines:
                    print(f"{VERDE}[+]======================> {dif.capitalize()}{NORMAL}")
                    for machine in filtered_machines:
                        print(f"{AZUL}Nombre: {machine[0].capitalize()}{NORMAL}")
                        print(f"{PURPLE}Tamaño de descarga: {machine[3]}{NORMAL}")
                        print(f"{PURPLE}Link de descarga: {machine[2]}{NORMAL}")
                        print() 
                else:
                    print(f"{AMARILLO}[!] No hay máquinas de dificultad {dif}.{NORMAL}")
                print()  

else:
    print(f"{ROJO}[x] Error al acceder a la página: {response.status_code}{NORMAL}")

