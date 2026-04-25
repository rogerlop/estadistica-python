"""
Clase 5 — Estadística Descriptiva
Archivo de práctica en vivo (live coding)

Este script acompaña la presentación de la Clase 5 del curso de
Estadística en Python para CENACE.

Temas:
- Medidas de tendencia central (media, mediana, moda)
- Medidas de dispersión (rango, IQR, varianza, desviación estándar)
- Simetría y curtosis
- Covarianza y correlación
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# ---------------------------------------------------------------------------
# 1. Carga y exploración de datos
# ---------------------------------------------------------------------------

data = pd.read_csv("../data/raw/Data_FMI.csv")
data = data[(data["Año"] >= 2000) & (data["Año"] <= 2023)].reset_index(drop=True)

print("Dimensiones:", data.shape)
print(data.head())

# Filtrar datos de 2023
data_2023 = data[data["Año"] == 2023].copy()
gdppc = data_2023["GDPpc_usd"].dropna() / 1000  # en miles USD

# ---------------------------------------------------------------------------
# 2. Medidas de tendencia central
# ---------------------------------------------------------------------------

# Media
media = gdppc.mean()
print(f"\nMedia PIB pc 2023: ${media:,.2f}k")

# Mediana
mediana = gdppc.median()
print(f"Mediana PIB pc 2023: ${mediana:,.2f}k")

# Moda (aproximada mediante histogram)
moda_bin = pd.cut(gdppc, bins=20).value_counts().idxmax()
print(f"Intervalo modal: {moda_bin}")

# ---------------------------------------------------------------------------
# 3. Medidas de dispersión
# ---------------------------------------------------------------------------

# Rango
rango = gdppc.max() - gdppc.min()
print(f"\nRango: ${rango:,.2f}k")

# Cuartiles y rango intercuartil (IQR)
q1 = gdppc.quantile(0.25)
q3 = gdppc.quantile(0.75)
iqr = q3 - q1
print(f"Q1: ${q1:,.2f}k  |  Q3: ${q3:,.2f}k  |  IQR: ${iqr:,.2f}k")

# Varianza y desviación estándar (poblacional, ddof=0)
varianza = gdppc.var(ddof=0)
std_dev = gdppc.std(ddof=0)
print(f"Varianza: {varianza:,.2f}  |  Desv. estándar: {std_dev:,.2f}k")

# ---------------------------------------------------------------------------
# 4. Simetría y curtosis
# ---------------------------------------------------------------------------

simetria = gdppc.skew()
curtosis = gdppc.kurt()
print(f"\nSimetría: {simetria:.4f}")
print(f"Curtosis: {curtosis:.4f}")

# ---------------------------------------------------------------------------
# 5. Covarianza y correlación
# ---------------------------------------------------------------------------

bolivia = data[(data["Pais"] == "Bolivia") & (data["Año"] > 1990)].copy()

cov_val = bolivia["rgrowth"].cov(bolivia["Inflacion"])
corr_val = bolivia["rgrowth"].corr(bolivia["Inflacion"])
print(f"\nCovarianza crecimiento-inflación (Bolivia): {cov_val:.4f}")
print(f"Correlación crecimiento-inflación (Bolivia): {corr_val:.4f}")

# ---------------------------------------------------------------------------
# 6. Visualizaciones rápidas
# ---------------------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histograma con media y mediana
axes[0].hist(gdppc, bins=40, color="steelblue", edgecolor="black", linewidth=0.3)
axes[0].axvline(media, color="red", linewidth=2, label=f"Media (${media:.1f}k)")
axes[0].axvline(mediana, color="blue", linewidth=2,
                label=f"Mediana (${mediana:.1f}k)")
axes[0].set_title("PIB per cápita 2023")
axes[0].set_xlabel("Miles USD")
axes[0].set_ylabel("Frecuencia")
axes[0].legend()

# Boxplot
axes[1].boxplot(gdppc.values, patch_artist=True,
                boxprops=dict(facecolor="steelblue"),
                medianprops=dict(color="black"),
                flierprops=dict(marker="o", markerfacecolor="red"))
axes[1].set_title("Boxplot PIB per cápita 2023")
axes[1].set_ylabel("Miles USD")
axes[1].set_xticks([])

plt.tight_layout()
plt.savefig("../outputs/figures/live_05_descriptiva.png", dpi=150)
plt.show()
print("\nFigura guardada en outputs/figures/live_05_descriptiva.png")
