"""
descriptive.py
==============

Funciones de estadística descriptiva reutilizables para el curso de
Estadística en Python — CENACE.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats


def media(serie: pd.Series | np.ndarray) -> float:
    """Calcula la media aritmética ignorando valores nulos.

    Parámetros
    ----------
    serie:
        Vector numérico (Series de pandas o array de NumPy).

    Retorna
    -------
    float
        Media aritmética de los valores no nulos.
    """
    arr = _a_array(serie)
    return float(np.nanmean(arr))


def mediana(serie: pd.Series | np.ndarray) -> float:
    """Calcula la mediana ignorando valores nulos.

    Parámetros
    ----------
    serie:
        Vector numérico.

    Retorna
    -------
    float
        Mediana de los valores no nulos.
    """
    arr = _a_array(serie)
    return float(np.nanmedian(arr))


def varianza(serie: pd.Series | np.ndarray, ddof: int = 0) -> float:
    """Calcula la varianza ignorando valores nulos.

    Parámetros
    ----------
    serie:
        Vector numérico.
    ddof:
        Grados de libertad (0 = varianza poblacional, 1 = muestral).

    Retorna
    -------
    float
        Varianza.
    """
    arr = _a_array(serie)
    return float(np.nanvar(arr, ddof=ddof))


def desviacion_estandar(serie: pd.Series | np.ndarray, ddof: int = 0) -> float:
    """Calcula la desviación estándar ignorando valores nulos.

    Parámetros
    ----------
    serie:
        Vector numérico.
    ddof:
        Grados de libertad.

    Retorna
    -------
    float
        Desviación estándar.
    """
    arr = _a_array(serie)
    return float(np.nanstd(arr, ddof=ddof))


def rango_intercuartil(serie: pd.Series | np.ndarray) -> float:
    """Calcula el rango intercuartil (IQR = Q3 − Q1) ignorando nulos.

    Parámetros
    ----------
    serie:
        Vector numérico.

    Retorna
    -------
    float
        Rango intercuartil.
    """
    arr = _a_array(serie)
    arr = arr[~np.isnan(arr)]
    q1, q3 = np.percentile(arr, [25, 75])
    return float(q3 - q1)


def simetria(serie: pd.Series | np.ndarray) -> float:
    """Calcula el coeficiente de asimetría (skewness) ignorando nulos.

    Parámetros
    ----------
    serie:
        Vector numérico.

    Retorna
    -------
    float
        Coeficiente de asimetría.
    """
    arr = _a_array(serie)
    arr = arr[~np.isnan(arr)]
    return float(scipy_stats.skew(arr))


def curtosis(serie: pd.Series | np.ndarray) -> float:
    """Calcula la curtosis (excess kurtosis) ignorando nulos.

    Parámetros
    ----------
    serie:
        Vector numérico.

    Retorna
    -------
    float
        Curtosis (excess kurtosis, referencia a la distribución normal = 0).
    """
    arr = _a_array(serie)
    arr = arr[~np.isnan(arr)]
    return float(scipy_stats.kurtosis(arr))


def resumen_descriptivo(serie: pd.Series | np.ndarray) -> pd.Series:
    """Genera un resumen descriptivo completo.

    Incluye: conteo, media, mediana, desviación estándar, mínimo, Q1,
    Q3, máximo, rango, IQR, simetría y curtosis.

    Parámetros
    ----------
    serie:
        Vector numérico.

    Retorna
    -------
    pd.Series
        Serie con todas las estadísticas descriptivas.
    """
    arr = _a_array(serie)
    arr_clean = arr[~np.isnan(arr)]

    q1, q3 = np.percentile(arr_clean, [25, 75])

    return pd.Series(
        {
            "n": len(arr_clean),
            "media": np.mean(arr_clean),
            "mediana": np.median(arr_clean),
            "desv_std": np.std(arr_clean, ddof=0),
            "varianza": np.var(arr_clean, ddof=0),
            "minimo": np.min(arr_clean),
            "Q1": q1,
            "Q3": q3,
            "maximo": np.max(arr_clean),
            "rango": np.max(arr_clean) - np.min(arr_clean),
            "IQR": q3 - q1,
            "simetria": scipy_stats.skew(arr_clean),
            "curtosis": scipy_stats.kurtosis(arr_clean),
        }
    )


# ---------------------------------------------------------------------------
# Utilidades internas
# ---------------------------------------------------------------------------


def _a_array(serie: pd.Series | np.ndarray) -> np.ndarray:
    """Convierte una Serie de pandas o array a np.ndarray de floats."""
    if isinstance(serie, pd.Series):
        return serie.to_numpy(dtype=float)
    return np.asarray(serie, dtype=float)
