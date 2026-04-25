"""
Ejercicio 5 — Estadística Descriptiva
Solución completa

Este archivo contiene la solución completa del Ejercicio 5. No lo consulte
antes de intentar resolver la plantilla por su cuenta.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import scipy.stats as stats

# ---------------------------------------------------------------------------
# Ejercicio 1: Carga y exploración de datos
# ---------------------------------------------------------------------------

data = pd.read_csv("../../data/raw/Data_FMI.csv")
data = data[(data["Año"] >= 2000) & (data["Año"] <= 2023)].reset_index(drop=True)

print("Primeras 5 filas:")
print(data.head())
print(f"\nDimensiones: {data.shape}")

# ---------------------------------------------------------------------------
# Ejercicio 2: Medidas de tendencia central (año 2023)
# ---------------------------------------------------------------------------

data_2023 = data[data["Año"] == 2023].copy()
gdppc_2023 = data_2023["GDPpc_usd"].dropna() / 1000

media = gdppc_2023.mean()
mediana = gdppc_2023.median()

print(f"\nMedia PIB pc 2023:   ${media:,.2f}k")
print(f"Mediana PIB pc 2023: ${mediana:,.2f}k")

# ---------------------------------------------------------------------------
# Ejercicio 3: Medidas de dispersión
# ---------------------------------------------------------------------------

rango = gdppc_2023.max() - gdppc_2023.min()
q1 = gdppc_2023.quantile(0.25)
q3 = gdppc_2023.quantile(0.75)
iqr = q3 - q1
std_dev = gdppc_2023.std(ddof=0)

print(f"\nRango:             ${rango:,.2f}k")
print(f"IQR (Q3 - Q1):     ${iqr:,.2f}k")
print(f"Desv. estándar:    ${std_dev:,.2f}k")

# ---------------------------------------------------------------------------
# Ejercicio 4: Simetría y curtosis
# ---------------------------------------------------------------------------

simetria = gdppc_2023.skew()
curtosis = gdppc_2023.kurt()

print(f"\nSimetría: {simetria:.4f}")
# Simetría > 0 indica sesgo positivo (cola a la derecha),
# lo cual es esperado ya que hay países con PIB muy alto.

print(f"Curtosis: {curtosis:.4f}")
# Curtosis > 0 indica una distribución leptocúrtica (colas más pesadas que
# la normal), lo que refleja la presencia de valores atípicos (outliers).

# ---------------------------------------------------------------------------
# Ejercicio 5: Covarianza y correlación
# ---------------------------------------------------------------------------

pais = "Bolivia"
datos_pais = data[(data["Pais"] == pais) & (data["Año"] > 1990)].copy()

cov_val = datos_pais["rgrowth"].cov(datos_pais["Inflacion"])
corr_val = datos_pais["rgrowth"].corr(datos_pais["Inflacion"])

print(f"\nCovarianza crecimiento–inflación ({pais}): {cov_val:.4f}")
print(f"Correlación crecimiento–inflación ({pais}): {corr_val:.4f}")
# Una correlación negativa sugiere que cuando el crecimiento es alto,
# la inflación tiende a ser baja (o viceversa), aunque la magnitud es débil.

# ---------------------------------------------------------------------------
# Ejercicio 6: Visualización
# ---------------------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histograma
axes[0].hist(gdppc_2023, bins=40, color="steelblue",
             edgecolor="black", linewidth=0.3)
axes[0].axvline(media, color="red", linewidth=2, label=f"Media (${media:.1f}k)")
axes[0].axvline(mediana, color="blue", linewidth=2,
                label=f"Mediana (${mediana:.1f}k)")
axes[0].set_title("Distribución del PIB per cápita (2023)")
axes[0].set_xlabel("PIB per cápita (miles USD)")
axes[0].set_ylabel("Frecuencia")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}k"))
axes[0].legend()

# Boxplot
axes[1].boxplot(gdppc_2023.values, patch_artist=True, widths=0.4,
                boxprops=dict(facecolor="steelblue", color="black"),
                medianprops=dict(color="black"),
                flierprops=dict(marker="o", markerfacecolor="red", markersize=5))
axes[1].set_title("Boxplot del PIB per cápita (2023)")
axes[1].set_ylabel("PIB per cápita (miles USD)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}k"))
axes[1].set_xticks([])

plt.tight_layout()
plt.savefig("../../outputs/figures/ejercicio_05.png", dpi=150)
plt.show()
print("\nFigura guardada en outputs/figures/ejercicio_05.png")
