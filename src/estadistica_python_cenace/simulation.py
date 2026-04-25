"""
simulation.py
=============

Funciones de simulación y generación de datos sintéticos para el curso de
Estadística en Python — CENACE.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simular_normal(
    n: int,
    media: float = 0.0,
    desv_std: float = 1.0,
    semilla: int | None = None,
) -> np.ndarray:
    """Genera una muestra aleatoria de una distribución normal.

    Parámetros
    ----------
    n:
        Tamaño de la muestra.
    media:
        Media de la distribución (μ).
    desv_std:
        Desviación estándar de la distribución (σ).
    semilla:
        Semilla para reproducibilidad. Si es None, no se fija semilla.

    Retorna
    -------
    np.ndarray
        Array de `n` valores generados de N(media, desv_std²).

    Ejemplos
    --------
    >>> datos = simular_normal(100, media=50, desv_std=10, semilla=42)
    >>> len(datos)
    100
    """
    rng = np.random.default_rng(semilla)
    return rng.normal(loc=media, scale=desv_std, size=n)


def simular_bootstrap(
    datos: pd.Series | np.ndarray,
    estadistico,
    n_iter: int = 1000,
    semilla: int | None = None,
) -> np.ndarray:
    """Aplica bootstrap para estimar la distribución muestral de un estadístico.

    Parámetros
    ----------
    datos:
        Vector numérico original (muestra observada).
    estadistico:
        Función que calcula el estadístico de interés sobre un array.
        Por ejemplo, ``np.mean``, ``np.median`` o una función personalizada.
    n_iter:
        Número de iteraciones de bootstrap.
    semilla:
        Semilla para reproducibilidad.

    Retorna
    -------
    np.ndarray
        Array de `n_iter` valores del estadístico calculado sobre cada
        muestra bootstrap.

    Ejemplos
    --------
    >>> datos = np.array([2.0, 3.0, 5.0, 7.0, 11.0])
    >>> medias_boot = simular_bootstrap(datos, np.mean, n_iter=500, semilla=0)
    >>> len(medias_boot)
    500
    """
    if isinstance(datos, pd.Series):
        arr = datos.to_numpy(dtype=float)
    else:
        arr = np.asarray(datos, dtype=float)

    arr = arr[~np.isnan(arr)]
    rng = np.random.default_rng(semilla)
    resultados = np.empty(n_iter)

    for i in range(n_iter):
        muestra = rng.choice(arr, size=len(arr), replace=True)
        resultados[i] = estadistico(muestra)

    return resultados
