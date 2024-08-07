
# DOCKERLABS CLI

Dockerlabs es una plataforma de CTF con las máquinas creadas en docker. Fácil de iniciar, con gasto bajo de recursos, y facil de borrar. Plataforma creada por [@elpingüinodemario](https://github.com/Maalfer), y a quien tenemos que agradecer su pasión y esfuerzo.

# DockerLabs CLI
- v2.0


## Instalación

```
git clone https://github.com/PatxaSec/DockerLabs.git
```
```
cd DockerLabs
```
```
pip3 install -r requirements.txt 
```


---

# seeTarget.py (Desarrolado en ![Python](https://img.shields.io/badge/python-3.11.9-3670A0?style=flat&logo=python&logoColor=ffdd54))

Probado en:  ![Python](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11-3670A0?style=flat&logo=python&logoColor=ffdd54)

Con este script puedes:
- Listar, ordenadas por dificultad, todas la máquinas disponibles junto con la memoria de descarga y su link.
- Listar Filtradas por la dificultad que escojas todas las máquinas disponibles en esa dificultad. `-d <dificultad>`
- Sacar una máquina aleatoria del listado completo. `-r`
- Sacar una máquina aleatoria de una dificultad concreta. `-r`+`-d <dificultad>`
- Guardar las máquinas ya hechas para que el output te avise, y al usar la opción random no te salgan. `-D <nombre de maquina>`
- Listar todas las maquinas ya hechas ordenadas por Dificultad. `-p`
- Buscar una máquina concreta por su nombre. `-n <nombre de máquina>`
- Buscar máquinas por creador. `-nc <nombre creador>`
- Sacar una máquina aleatoria de un creador concreto. `-r` + `-nc <nombre creador>`
- Listar máquinas ordenadas por creador. `-c`
- eliminar el color del output. `--no-colors`

## Uso

```
seeTarget.py [-h] [-d DIFICULTAD] [-r] [-n NOMBRE] [-p] [-nb] [-D DONE] [-c] [-nc NOMBRE_CREADOR] [--no-colors]
```

## opciones
```
 -h, --help            show this help message and exit
  -d DIFICULTAD, --dificultad DIFICULTAD
                        Filtrar por dificultad. ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']
  -r, --random          Máquina aleatoria.
  -n NOMBRE, --nombre NOMBRE
                        Buscar una máquina concreta.
  -p, --pwn3d           Listar todas las maquinas marcadas como hechas
  -nb, --no-banner      Eliminar el banner del output.
  -D DONE, --Done DONE  Marcar una máquina como hecha.
  -c, --creador         Listar máquinas por creador.
  -nc NOMBRE_CREADOR, --nombre_creador NOMBRE_CREADOR
                        Buscar máquinas por nombre de creador.
  --no-colors           Eliminar colores del output.

```



---
# geTarget.py  (Desarrolado en ![Python](https://img.shields.io/badge/python-3.10.12_slim-3670A0?style=flat&logo=python&logoColor=ffdd54))

probado en:   ![Python](https://img.shields.io/badge/python-3.10.12_slim-3670A0?style=flat&logo=python&logoColor=ffdd54)

Con este script puedes:
- Listar, ordenadas por dificultad, todas la máquinas disponibles junto con la memoria de descarga y su link.
- Listar Filtradas por la dificultad que escojas todas las máquinas disponibles en esa dificultad. `-d <dificultad>`
- Sacar una máquina aleatoria del listado completo. `-r`
- Sacar una máquina aleatoria de una dificultad concreta. `-r`+`-d <dificultad>`
- Guardar las máquinas ya hechas para que el output te avise, y al usar la opción random no te salgan. `-D <nombre de maquina>`
- Listar todas las maquinas ya hechas ordenadas por Dificultad. `-p`
- Buscar una máquina concreta por su nombre. `-n <nombre de máquina>`
- Buscar máquinas por creador. `-nc <nombre creador>`
- Sacar una máquina aleatoria de un creador concreto. `-r` + `-nc <nombre creador>`
- Listar máquinas ordenadas por creador. `-c`
- Descarga de una máquina concreta usando filtros random o búsqueda por nombre y añadiendo `-w <ruta/para/descarga>`. 
- Barra de progreso a descarga: (en desarrollo)

## Uso

```
geTarget.py [-h] [-d DIFICULTAD] [-r] [-n NOMBRE] [-p] [-nb] [-D DONE] [-c] [-nc NOMBRE_CREADOR] [-w WEB_GET]
```

## opciones
```
 -h, --help            show this help message and exit
  -d DIFICULTAD, --dificultad DIFICULTAD
                        Filtrar por dificultad. ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']
  -r, --random          Máquina aleatoria.
  -n NOMBRE, --nombre NOMBRE
                        Buscar una máquina concreta.
  -p, --pwn3d           Listar todas las maquinas marcadas como hechas
  -nb, --no-banner      Eliminar el banner del output.
  -D DONE, --Done DONE  Marcar una máquina como hecha.
  -c, --creador         Listar máquinas por creador.
  -nc NOMBRE_CREADOR, --nombre_creador NOMBRE_CREADOR
                        Buscar máquinas por nombre de creador.
  -w WEB_GET, --web-get <directorio de descarga>
                        Descargar máquina.

```
---

# Ejemplos

![descarga](ejemplos/descarga.png)

---

![marcar y verificar](ejemplos/marcar_hecha_y_verificar.png)

---

![random+medio](ejemplos/random+Medio.png)
