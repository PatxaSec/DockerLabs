# DockerLabs CLI

Herramienta que mediante el scrapping de la web, permite obtener diferentes resultados.

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
