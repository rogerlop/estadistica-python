"""
Ejercicio 6 — Estadística Inferencial
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
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Ejercicio 1: Carga de datos
# ---------------------------------------------------------------------------
# TODO: Cargue el archivo 'data/raw/Data_FMI.csv' y filtre 2000-2023.
data = None  # reemplazar
data_2023 = None  # reemplazar
gdppc = None  # reemplazar: GDPpc_usd / 1000 para 2023

# ---------------------------------------------------------------------------
# Ejercicio 2: Intervalos de confianza
# ---------------------------------------------------------------------------
# TODO: Calcule el intervalo de confianza al 95 % para la media del
# PIB per cápita en 2023. Use scipy.stats.t.interval().
# Imprima el resultado.

ic = None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 3: Prueba t de una muestra
# ---------------------------------------------------------------------------
# TODO: Pruebe si la media del PIB per cápita en 2023 es diferente de
# USD 15 000 (= 15 en miles).
# H₀: μ = 15    H₁: μ ≠ 15
# Use scipy.stats.ttest_1samp() e interprete el resultado.

t_stat, p_value = None, None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 4: Prueba t de dos muestras
# ---------------------------------------------------------------------------
# TODO: Compare el PIB per cápita promedio entre:
#   - África (Continent == "Africa")
#   - Oceanía (Continent == "Oceania")
# Use la prueba de Welch (equal_var=False).

africa = None    # TODO
oceania = None   # TODO
t2, p2 = None, None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 5: ANOVA
# ---------------------------------------------------------------------------
# TODO: Pruebe si las medias del PIB per cápita difieren entre continentes.
# Use scipy.stats.f_oneway() con los grupos por continente.

f_stat, p_anova = None, None  # TODO

# ---------------------------------------------------------------------------
# Ejercicio 6: Regresión lineal simple
# ---------------------------------------------------------------------------
# TODO: Ajuste un modelo de regresión lineal simple:
#   Variable dependiente: rgrowth
#   Variable independiente: GDPpc_usd / 1000 (llamar GDPpc_miles)
# Use statsmodels.formula.api.ols().
# Imprima el resumen del modelo y grafique la línea de regresión.

modelo = None  # TODO
