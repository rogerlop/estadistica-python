"""
inference.py
============

Funciones de estadística inferencial reutilizables para el curso de
Estadística en Python — CENACE.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats


def intervalo_confianza(
    serie: pd.Series | np.ndarray,
    nivel: float = 0.95,
) -> tuple[float, float]:
    """Calcula el intervalo de confianza para la media poblacional.

    Utiliza la distribución t de Student (varianza desconocida).

    Parámetros
    ----------
    serie:
        Vector numérico con los datos muestrales.
    nivel:
        Nivel de confianza (por defecto 0.95 = 95 %).

    Retorna
    -------
    tuple[float, float]
        Límite inferior y superior del intervalo de confianza.
    """
    arr = _a_array(serie)
    arr = arr[~np.isnan(arr)]
    n = len(arr)
    media = np.mean(arr)
    se = scipy_stats.sem(arr)
    ic = scipy_stats.t.interval(nivel, df=n - 1, loc=media, scale=se)
    return float(ic[0]), float(ic[1])


def prueba_t_una_muestra(
    serie: pd.Series | np.ndarray,
    media_hipotetica: float,
    alternativa: str = "two-sided",
) -> dict[str, float]:
    """Realiza una prueba t de una muestra.

    Parámetros
    ----------
    serie:
        Vector numérico con los datos muestrales.
    media_hipotetica:
        Valor de la media bajo la hipótesis nula (H₀: μ = media_hipotetica).
    alternativa:
        Tipo de prueba: 'two-sided', 'less' o 'greater'.

    Retorna
    -------
    dict[str, float]
        Diccionario con 't_stat', 'p_value' y 'media_muestral'.
    """
    arr = _a_array(serie)
    arr = arr[~np.isnan(arr)]
    t_stat, p_value = scipy_stats.ttest_1samp(arr, popmean=media_hipotetica,
                                               alternative=alternativa)
    return {
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "media_muestral": float(np.mean(arr)),
    }


def prueba_t_dos_muestras(
    grupo1: pd.Series | np.ndarray,
    grupo2: pd.Series | np.ndarray,
    equal_var: bool = False,
    alternativa: str = "two-sided",
) -> dict[str, float]:
    """Realiza una prueba t de dos muestras independientes.

    Por defecto aplica la corrección de Welch (equal_var=False).

    Parámetros
    ----------
    grupo1:
        Primer grupo de datos.
    grupo2:
        Segundo grupo de datos.
    equal_var:
        Si True, asume varianzas iguales (prueba t clásica).
        Si False, aplica la corrección de Welch.
    alternativa:
        Tipo de prueba: 'two-sided', 'less' o 'greater'.

    Retorna
    -------
    dict[str, float]
        Diccionario con 't_stat', 'p_value', 'media_grupo1' y 'media_grupo2'.
    """
    a1 = _a_array(grupo1)
    a2 = _a_array(grupo2)
    a1 = a1[~np.isnan(a1)]
    a2 = a2[~np.isnan(a2)]

    t_stat, p_value = scipy_stats.ttest_ind(a1, a2, equal_var=equal_var,
                                             alternative=alternativa)
    return {
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "media_grupo1": float(np.mean(a1)),
        "media_grupo2": float(np.mean(a2)),
    }


def anova_una_via(
    *grupos: pd.Series | np.ndarray,
) -> dict[str, float]:
    """Realiza un ANOVA de una vía (F de Fisher).

    Parámetros
    ----------
    *grupos:
        Dos o más vectores numéricos que representan los grupos.

    Retorna
    -------
    dict[str, float]
        Diccionario con 'f_stat' y 'p_value'.
    """
    limpios = [_a_array(g)[~np.isnan(_a_array(g))] for g in grupos]
    f_stat, p_value = scipy_stats.f_oneway(*limpios)
    return {
        "f_stat": float(f_stat),
        "p_value": float(p_value),
    }


# ---------------------------------------------------------------------------
# Utilidades internas
# ---------------------------------------------------------------------------


def _a_array(serie: pd.Series | np.ndarray) -> np.ndarray:
    """Convierte una Serie de pandas o array a np.ndarray de floats."""
    if isinstance(serie, pd.Series):
        return serie.to_numpy(dtype=float)
    return np.asarray(serie, dtype=float)
