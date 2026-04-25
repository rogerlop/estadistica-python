"""
plotting.py
===========

Funciones de visualización reutilizables para el curso de
Estadística en Python — CENACE.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes


def histograma_con_estadisticas(
    serie: pd.Series | np.ndarray,
    titulo: str = "Distribución",
    etiqueta_x: str = "Valor",
    bins: int = 30,
    mostrar_media: bool = True,
    mostrar_mediana: bool = True,
    ax: matplotlib.axes.Axes | None = None,
) -> matplotlib.axes.Axes:
    """Genera un histograma con líneas para la media y la mediana.

    Parámetros
    ----------
    serie:
        Vector numérico a graficar.
    titulo:
        Título del gráfico.
    etiqueta_x:
        Etiqueta del eje x.
    bins:
        Número de barras del histograma.
    mostrar_media:
        Si True, dibuja una línea vertical roja para la media.
    mostrar_mediana:
        Si True, dibuja una línea vertical azul para la mediana.
    ax:
        Eje de matplotlib existente. Si es None, crea uno nuevo.

    Retorna
    -------
    matplotlib.axes.Axes
        Eje con el gráfico generado.
    """
    arr = _a_array(serie)
    arr = arr[~np.isnan(arr)]

    if ax is None:
        _, ax = plt.subplots()

    ax.hist(arr, bins=bins, color="steelblue", edgecolor="black", linewidth=0.3)

    if mostrar_media:
        media = np.mean(arr)
        ax.axvline(media, color="red", linewidth=2, label=f"Media ({media:.2f})")

    if mostrar_mediana:
        mediana = np.median(arr)
        ax.axvline(mediana, color="blue", linewidth=2,
                   label=f"Mediana ({mediana:.2f})")

    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel("Frecuencia")

    if mostrar_media or mostrar_mediana:
        ax.legend()

    return ax


def boxplot_grupos(
    grupos: dict[str, pd.Series | np.ndarray],
    titulo: str = "Comparación por grupos",
    etiqueta_y: str = "Valor",
    ax: matplotlib.axes.Axes | None = None,
) -> matplotlib.axes.Axes:
    """Genera un boxplot comparativo para múltiples grupos.

    Parámetros
    ----------
    grupos:
        Diccionario ``{nombre_grupo: datos}`` con los grupos a comparar.
    titulo:
        Título del gráfico.
    etiqueta_y:
        Etiqueta del eje y.
    ax:
        Eje de matplotlib existente. Si es None, crea uno nuevo.

    Retorna
    -------
    matplotlib.axes.Axes
        Eje con el gráfico generado.
    """
    if ax is None:
        _, ax = plt.subplots()

    nombres = list(grupos.keys())
    datos = [_a_array(v)[~np.isnan(_a_array(v))] for v in grupos.values()]

    bp = ax.boxplot(datos, patch_artist=True,
                    medianprops=dict(color="black"),
                    flierprops=dict(marker="o", markerfacecolor="red",
                                    markersize=4))

    colores = plt.cm.tab10.colors
    for patch, color in zip(bp["boxes"], colores):
        patch.set_facecolor(color)

    ax.set_xticklabels(nombres, rotation=15, ha="right")
    ax.set_title(titulo)
    ax.set_ylabel(etiqueta_y)

    return ax


def grafico_regresion(
    x: pd.Series | np.ndarray,
    y: pd.Series | np.ndarray,
    titulo: str = "Regresión lineal",
    etiqueta_x: str = "x",
    etiqueta_y: str = "y",
    ax: matplotlib.axes.Axes | None = None,
) -> matplotlib.axes.Axes:
    """Genera un diagrama de dispersión con línea de regresión lineal.

    Parámetros
    ----------
    x:
        Variable independiente.
    y:
        Variable dependiente.
    titulo:
        Título del gráfico.
    etiqueta_x:
        Etiqueta del eje x.
    etiqueta_y:
        Etiqueta del eje y.
    ax:
        Eje de matplotlib existente. Si es None, crea uno nuevo.

    Retorna
    -------
    matplotlib.axes.Axes
        Eje con el gráfico generado.
    """
    xarr = _a_array(x)
    yarr = _a_array(y)
    mask = ~np.isnan(xarr) & ~np.isnan(yarr)
    xarr, yarr = xarr[mask], yarr[mask]

    if ax is None:
        _, ax = plt.subplots()

    ax.scatter(xarr, yarr, color="steelblue", edgecolors="black",
               alpha=0.7, s=40, label="Datos")

    m, b = np.polyfit(xarr, yarr, 1)
    x_line = np.linspace(xarr.min(), xarr.max(), 200)
    ax.plot(x_line, m * x_line + b, color="red", linewidth=2,
            label=f"Ajuste: y = {m:.3f}x + {b:.3f}")

    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    ax.legend()

    return ax


def grafico_correlacion(
    data: pd.DataFrame,
    variables: list[str] | None = None,
    titulo: str = "Matriz de correlación",
    ax: matplotlib.axes.Axes | None = None,
) -> matplotlib.axes.Axes:
    """Genera un mapa de calor de la matriz de correlación.

    Parámetros
    ----------
    data:
        DataFrame con las variables numéricas.
    variables:
        Lista de columnas a incluir. Si es None, usa todas las numéricas.
    titulo:
        Título del gráfico.
    ax:
        Eje de matplotlib existente. Si es None, crea uno nuevo.

    Retorna
    -------
    matplotlib.axes.Axes
        Eje con el gráfico generado.
    """
    if variables is not None:
        data = data[variables]

    corr_matrix = data.select_dtypes(include=[np.number]).corr()

    if ax is None:
        _, ax = plt.subplots()

    cax = ax.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(cax, ax=ax)

    labels = corr_matrix.columns.tolist()
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
                    ha="center", va="center", fontsize=9)

    ax.set_title(titulo)
    return ax


# ---------------------------------------------------------------------------
# Utilidades internas
# ---------------------------------------------------------------------------


def _a_array(serie: pd.Series | np.ndarray) -> np.ndarray:
    """Convierte una Serie de pandas o array a np.ndarray de floats."""
    if isinstance(serie, pd.Series):
        return serie.to_numpy(dtype=float)
    return np.asarray(serie, dtype=float)
