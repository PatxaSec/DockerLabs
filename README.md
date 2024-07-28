# DockerLabs CLI

Herramienta que mediante el scrapping de la web, permite obtener diferentes resultados.

Con esta herramienta puedes:
- Listar, ordenadas por dificultad, todas la máquinas disponibles junto con la memoria de descarga y su link.
- Listar Filtradas por la dificultad que escojas todas las máquinas disponibles en esa dificultad. `-d <dificultad>`
- Sacar una máquina aleatoria del listado completo. `-r`
- Sacar una máquina aleatoria de una dificultad concreta. `-r`+`-d <dificultad>`
- Guardar las máquinas ya hechas para que el output te avise, y al usaar la opción random no te salgan. `-D <nombre de maquina>`
- Buscar una máquina concreta por su nombre. `-n <nombre de máquina>`

## Instalación

```
git clone https://github.com/PatxaSec/DockerLabs.git
```
```
cd Dockerlabs
```
```
pip3 install -r requirements.txt
```

## Uso

```
usage: get_target.py [-h] [-d DIFICULTAD] [-r] [-n NOMBRE] [-nb] [-D DONE]

Busca tu máquina de Dockerlabs.

options:
  -h, --help            show this help message and exit
  -d DIFICULTAD, --dificultad DIFICULTAD
                        Filtrar por dificultad. ['Muy Fácil', 'Fácil', 'Medio', 'Difícil']
  -r, --random          Máquina aleatoria.
  -n NOMBRE, --nombre NOMBRE
                        Buscar una máquina concreta.
  -nb, --no-banner      Eliminar el banner del output.
  -D DONE, --Done DONE  Marcar una máquina como hecha.
```

## Ejemplos

### Sin filtros: El ouput es un listado de todas las máquinas ordenado por dificultad.
[Sin Filtros](ejemplos/sin_filtros.png)

### Random: El ouput es una máquina random del listado completo existente.
[Random](ejemplos/random.png)

### Random + Filtro de Dificultad: El ouput es una máquina random del listado de maquinas con la dificultad que escojas.
[Random y Por dificultad](ejemplos/random+Medio.png)

### Filtro de dificultad: El ouput es un listado de todas las máquinas con la dificultad que escojas.
[Por dificultad](ejemplos/dificultad.png)

### Filtro de nombre: El ouput es la información sobre máquina que escojas.
[Por nombre](ejemplos/nombre.png)
