# Estadística Aplicada en Python

Material del curso de **Estadística Aplicada en Python** para CENACE y UPSA.
Este repositorio reúne las presentaciones, datos y archivos de apoyo usados en
clase.

## Ver las presentaciones

La forma recomendada de revisar las clases es desde la página web del curso:

**https://rogerlop.github.io/estadistica-python/**

Clases disponibles por ahora:

| Clase | Tema | Presentación HTML |
| --- | --- | --- |
| 1 | Instalación y entorno de desarrollo | [Abrir clase 1](https://rogerlop.github.io/estadistica-python/slides/01_Instalacion/lecture_01_Python_Instalacion.html) |
| 2 | Fundamentos de Python | [Abrir clase 2](https://rogerlop.github.io/estadistica-python/slides/02_fundamentos_python/lecture_02_fundamentos_python.html) |
| 3 | Análisis de datos con pandas | [Abrir clase 3](https://rogerlop.github.io/estadistica-python/slides/03_analisis_python/lecture_03_analisis-python.html) |
| 4 | Visualización de datos en Python | [Abrir clase 4](https://rogerlop.github.io/estadistica-python/slides/04_dataviz/lecture_04_visualizacion.html) |

> Nota: si los enlaces aún no abren como página web, falta activar GitHub Pages
> en el repositorio. La configuración sugerida es **Settings > Pages > Deploy
> from a branch > main > /root**.

## Dónde está cada cosa

```text
estadistica-python/
├── index.html              # Portada web del curso para GitHub Pages
├── README.md               # Guía general del repositorio
├── slides/                 # Presentaciones del curso
│   ├── 01_Instalacion/
│   ├── 02_fundamentos_python/
│   ├── 03_analisis_python/
│   └── 04_dataviz/
├── data/
│   └── raw/                # Datos originales usados en clase
├── assets/                 # Imágenes, logo y estilos de las diapositivas
├── live/                   # Scripts para sesiones en vivo
├── exercises/              # Plantillas y soluciones de ejercicios
├── src/                    # Funciones auxiliares del curso
└── docs/                   # Documentos complementarios
```

## Datos

Los datos disponibles para las primeras clases están en [`data/raw/`](data/raw/):

- [`Data_FMI.csv`](data/raw/Data_FMI.csv)
- [`Data_FMI.xlsx`](data/raw/Data_FMI.xlsx)

Estos archivos se usan para practicar importación, exploración, limpieza,
análisis y visualización de datos con Python.

## Cómo usar este repositorio

Para estudiantes, no es necesario instalar nada para ver las presentaciones:
basta con entrar a la página web del curso y abrir la clase correspondiente.

Para ejecutar los ejemplos localmente, se recomienda usar Python 3.12 y crear el
entorno del proyecto con `uv`:

```bash
uv python install 3.12
uv sync
```

Para renderizar una presentación con Quarto:

```bash
./scripts/quarto-wrapper.sh render slides/01_Instalacion/lecture_01_Python_Instalacion.qmd
```

## Estado del material

Actualmente están publicadas las clases 1 a 4. Las clases posteriores pueden
aparecer en el repositorio como borradores o material en preparación.

## Licencia y uso

Material preparado para uso educativo en el curso. Si reutilizas parte del
contenido, cita este repositorio y al autor.
