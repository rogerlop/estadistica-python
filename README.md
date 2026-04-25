# Estadística Python — CENACE

Curso en línea de estadística en Python, desarrollado con [Quarto](https://quarto.org/) y [uv](https://docs.astral.sh/uv/) para el Centro Nacional de Control de Energía (CENACE).

## Estructura del proyecto

```
estadistica-python/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
│
├── slides/
│   ├── _metadata.yml
│   ├── 05_estadistica_descriptiva/
│   │   └── lecture_05_estadistica_descriptiva.qmd
│   └── 06_estadistica_inferencial/
│       └── lecture_06_estadistica_inferencial.qmd
│
├── live/
│   ├── lecture_05_live.py
│   └── lecture_06_live.py
│
├── exercises/
│   ├── 05_estadistica_descriptiva/
│   │   ├── exercise_05_template.py
│   │   └── exercise_05_solution.py
│   └── 06_estadistica_inferencial/
│       ├── exercise_06_template.py
│       └── exercise_06_solution.py
│
├── src/
│   └── estadistica_python_cenace/
│       ├── __init__.py
│       ├── descriptive.py
│       ├── inference.py
│       ├── simulation.py
│       └── plotting.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── docs/
│
└── assets/
    ├── Imagenes/
    └── custom.css
```

## Requisitos

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) como gestor de dependencias
- [Quarto](https://quarto.org/) para renderizar las diapositivas

## Instalación

```bash
# Instalar dependencias con uv
uv sync

# Activar el entorno virtual
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows
```

## Uso

### Renderizar diapositivas

```bash
# Renderizar la clase 5 (Estadística Descriptiva)
quarto render slides/05_estadistica_descriptiva/lecture_05_estadistica_descriptiva.qmd

# Renderizar la clase 6 (Estadística Inferencial)
quarto render slides/06_estadistica_inferencial/lecture_06_estadistica_inferencial.qmd
```

### Ejecutar pruebas

```bash
uv run pytest
```

### Verificar calidad del código

```bash
uv run ruff check .
```

## Contenido del curso

### Clase 5 — Estadística Descriptiva

- Medidas de tendencia central (media, mediana, moda)
- Medidas de dispersión (rango, IQR, varianza, desviación estándar)
- Simetría y curtosis
- Covarianza y correlación

### Clase 6 — Estadística Inferencial

- Distribuciones de probabilidad
- Intervalos de confianza
- Pruebas de hipótesis (t-test, ANOVA, chi-cuadrado)
- Regresión lineal simple y múltiple

## Datos

Los datos utilizados en el curso provienen del
[Fondo Monetario Internacional (FMI)](https://www.imf.org/en/Data) y están
disponibles en `data/raw/`.

## Licencia

Uso educativo exclusivo — CENACE.
