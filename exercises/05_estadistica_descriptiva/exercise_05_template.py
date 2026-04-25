"""
Ejercicio 5 — Estadística Descriptiva
Plantilla para el estudiante

Instrucciones:
- Complete cada sección donde se indica con `# TODO`.
- Utilice los datos del FMI disponibles en data/raw/Data_FMI.csv.
- Ejecute el script una vez completado para verificar sus respuestas.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# ---------------------------------------------------------------------------
# Ejercicio 1: Carga y exploración de datos
# ---------------------------------------------------------------------------
# TODO: Cargue el archivo 'data/raw/Data_FMI.csv' en un DataFrame llamado `data`.
# Filtre los años entre 2000 y 2023.
data = None  # reemplazar

# TODO: Imprima las primeras 5 filas y las dimensiones del DataFrame.


# ---------------------------------------------------------------------------
# Ejercicio 2: Medidas de tendencia central (año 2023)
# ---------------------------------------------------------------------------
# TODO: Filtre los datos del año 2023 y calcule para la columna GDPpc_usd/1000:
#   a) la media
#   b) la mediana
# Imprima los resultados con dos decimales.

gdppc_2023 = None  # reemplazar con la serie filtrada

media = None    # TODO
mediana = None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 3: Medidas de dispersión
# ---------------------------------------------------------------------------
# TODO: Con los datos de 2023 (gdppc_2023), calcule:
#   a) El rango (máximo - mínimo)
#   b) El rango intercuartil (IQR = Q3 - Q1)
#   c) La desviación estándar (ddof=0)
# Imprima los resultados.

rango = None   # TODO
iqr = None     # TODO
std_dev = None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 4: Simetría y curtosis
# ---------------------------------------------------------------------------
# TODO: Calcule la simetría y la curtosis del PIB per cápita en 2023.
# Interprete brevemente los resultados (como comentario en el código).

simetria = None  # TODO
curtosis = None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 5: Covarianza y correlación
# ---------------------------------------------------------------------------
# TODO: Filtre los datos de un país de su elección para años > 1990.
# Calcule la covarianza y la correlación entre 'rgrowth' e 'Inflacion'.
# Imprima los resultados e interprete.

pais = "Bolivia"  # puede cambiar
datos_pais = None  # TODO

cov_val = None   # TODO
corr_val = None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 6: Visualización
# ---------------------------------------------------------------------------
# TODO: Genere una figura con dos subgráficos:
#   1. Histograma del PIB per cápita en 2023 con líneas para media y mediana.
#   2. Boxplot del PIB per cápita en 2023.
# Guarde la figura en 'outputs/figures/ejercicio_05.png'.

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# TODO: completar los dos subgráficos

plt.tight_layout()
plt.savefig("../outputs/figures/ejercicio_05.png", dpi=150)
plt.show()
