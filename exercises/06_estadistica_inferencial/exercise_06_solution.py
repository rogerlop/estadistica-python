"""
Ejercicio 6 — Estadística Inferencial
Solución completa

Este archivo contiene la solución completa del Ejercicio 6. No lo consulte
antes de intentar resolver la plantilla por su cuenta.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Ejercicio 1: Carga de datos
# ---------------------------------------------------------------------------

data = pd.read_csv("../../data/raw/Data_FMI.csv")
data = data[(data["Año"] >= 2000) & (data["Año"] <= 2023)].reset_index(drop=True)
data_2023 = data[data["Año"] == 2023].copy()
gdppc = data_2023["GDPpc_usd"].dropna() / 1000

# ---------------------------------------------------------------------------
# Ejercicio 2: Intervalos de confianza
# ---------------------------------------------------------------------------

n = len(gdppc)
media = gdppc.mean()
se = gdppc.sem()
ic = stats.t.interval(0.95, df=n - 1, loc=media, scale=se)

print(f"IC 95 % para el PIB pc promedio en 2023:")
print(f"  Media: ${media:,.2f}k")
print(f"  IC:    [${ic[0]:,.2f}k, ${ic[1]:,.2f}k]")

# ---------------------------------------------------------------------------
# Ejercicio 3: Prueba t de una muestra
# ---------------------------------------------------------------------------

t_stat, p_value = stats.ttest_1samp(gdppc, popmean=15)
print(f"\nPrueba t (H₀: μ = 15k):")
print(f"  t = {t_stat:.4f}   p = {p_value:.4f}")
if p_value < 0.05:
    print("  → Rechazamos H₀: la media es significativamente diferente de $15k.")
else:
    print("  → No rechazamos H₀.")

# ---------------------------------------------------------------------------
# Ejercicio 4: Prueba t de dos muestras
# ---------------------------------------------------------------------------

africa = data_2023[data_2023["Continent"] == "Africa"]["GDPpc_usd"].dropna() / 1000
oceania = data_2023[data_2023["Continent"] == "Oceania"]["GDPpc_usd"].dropna() / 1000

t2, p2 = stats.ttest_ind(africa, oceania, equal_var=False)
print(f"\nPrueba t de Welch (África vs Oceanía):")
print(f"  Media África:   ${africa.mean():,.2f}k")
print(f"  Media Oceanía:  ${oceania.mean():,.2f}k")
print(f"  t = {t2:.4f}   p = {p2:.4f}")
if p2 < 0.05:
    print("  → Las medias son significativamente distintas.")
else:
    print("  → No hay evidencia de diferencia significativa.")

# ---------------------------------------------------------------------------
# Ejercicio 5: ANOVA
# ---------------------------------------------------------------------------

grupos = [
    data_2023[data_2023["Continent"] == c]["GDPpc_usd"].dropna() / 1000
    for c in data_2023["Continent"].dropna().unique()
]
f_stat, p_anova = stats.f_oneway(*grupos)
print(f"\nANOVA — PIB pc por continente (2023):")
print(f"  F = {f_stat:.4f}   p = {p_anova:.6f}")
if p_anova < 0.05:
    print("  → Al menos una región tiene media diferente.")

# ---------------------------------------------------------------------------
# Ejercicio 6: Regresión lineal simple
# ---------------------------------------------------------------------------

datos_reg = data_2023.dropna(subset=["GDPpc_usd", "rgrowth"]).copy()
datos_reg["GDPpc_miles"] = datos_reg["GDPpc_usd"] / 1000

modelo = smf.ols("rgrowth ~ GDPpc_miles", data=datos_reg).fit()
print("\nRegresión lineal: rgrowth ~ GDPpc_miles")
print(modelo.summary().tables[1])
print(f"R²: {modelo.rsquared:.4f}")

# Gráfico de regresión
x_line = np.linspace(datos_reg["GDPpc_miles"].min(),
                     datos_reg["GDPpc_miles"].max(), 200)
y_pred = modelo.params["Intercept"] + modelo.params["GDPpc_miles"] * x_line

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(datos_reg["GDPpc_miles"], datos_reg["rgrowth"],
           color="steelblue", edgecolors="black", alpha=0.7, s=40,
           label="Datos 2023")
ax.plot(x_line, y_pred, color="red", linewidth=2, label="Ajuste lineal")
ax.set_title("Regresión: Crecimiento PIB ~ PIB per cápita (2023)")
ax.set_xlabel("PIB per cápita (miles USD)")
ax.set_ylabel("Crecimiento del PIB real (%)")
ax.legend()
plt.tight_layout()
plt.savefig("../../outputs/figures/ejercicio_06.png", dpi=150)
plt.show()
print("\nFigura guardada en outputs/figures/ejercicio_06.png")
