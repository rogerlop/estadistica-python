"""
estadistica_python_cenace
=========================

Paquete de utilidades para el curso de Estadística en Python — CENACE.

Módulos disponibles:
- descriptive : medidas descriptivas (tendencia central, dispersión, forma)
- inference   : pruebas de hipótesis e intervalos de confianza
- simulation  : generación de datos sintéticos y simulaciones de Monte Carlo
- plotting    : funciones de visualización reutilizables
"""

from .descriptive import (
    resumen_descriptivo,
    media,
    mediana,
    varianza,
    desviacion_estandar,
    rango_intercuartil,
    simetria,
    curtosis,
)
from .inference import (
    intervalo_confianza,
    prueba_t_una_muestra,
    prueba_t_dos_muestras,
    anova_una_via,
)
from .simulation import simular_normal, simular_bootstrap
from .plotting import (
    histograma_con_estadisticas,
    boxplot_grupos,
    grafico_regresion,
    grafico_correlacion,
)

__all__ = [
    # descriptive
    "resumen_descriptivo",
    "media",
    "mediana",
    "varianza",
    "desviacion_estandar",
    "rango_intercuartil",
    "simetria",
    "curtosis",
    # inference
    "intervalo_confianza",
    "prueba_t_una_muestra",
    "prueba_t_dos_muestras",
    "anova_una_via",
    # simulation
    "simular_normal",
    "simular_bootstrap",
    # plotting
    "histograma_con_estadisticas",
    "boxplot_grupos",
    "grafico_regresion",
    "grafico_correlacion",
]
