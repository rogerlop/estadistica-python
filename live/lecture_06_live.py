"""
Clase 6 — Estadística Inferencial
Archivo de práctica en vivo (live coding)

Este script acompaña la presentación de la Clase 6 del curso de
Estadística en Python para CENACE.

Temas:
- Distribuciones de probabilidad
- Intervalos de confianza
- Pruebas de hipótesis (t-test, chi-cuadrado, ANOVA)
- Regresión lineal simple y múltiple
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# 1. Carga de datos
# ---------------------------------------------------------------------------

data = pd.read_csv("../data/raw/Data_FMI.csv")
data = data[(data["Año"] >= 2000) & (data["Año"] <= 2023)].reset_index(drop=True)
data_2023 = data[data["Año"] == 2023].copy()
gdppc = data_2023["GDPpc_usd"].dropna() / 1000

# ---------------------------------------------------------------------------
# 2. Distribuciones de probabilidad
# ---------------------------------------------------------------------------

# Distribución normal estándar
x = np.linspace(-4, 4, 300)
y_norm = stats.norm.pdf(x)
plt.figure(figsize=(8, 4))
plt.plot(x, y_norm, color="steelblue", linewidth=2, label="Normal estándar")
plt.fill_between(x, y_norm, where=(np.abs(x) <= 1.96),
                 color="steelblue", alpha=0.3, label="95 %")
plt.title("Distribución Normal Estándar")
plt.xlabel("z")
plt.ylabel("f(z)")
plt.legend()
plt.tight_layout()
plt.show()

# Distribución t vs normal
x_t = np.linspace(-4, 4, 300)
plt.figure(figsize=(8, 4))
plt.plot(x_t, stats.norm.pdf(x_t), "k--", linewidth=2, label="Normal")
for df in [1, 5, 30]:
    plt.plot(x_t, stats.t.pdf(x_t, df=df), linewidth=1.8, label=f"t (ν={df})")
plt.title("Distribución t vs Normal")
plt.xlabel("Valor")
plt.ylabel("Densidad")
plt.legend()
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 3. Intervalos de confianza
# ---------------------------------------------------------------------------

n = len(gdppc)
media = gdppc.mean()
se = gdppc.sem()
ic = stats.t.interval(0.95, df=n - 1, loc=media, scale=se)

print(f"IC 95 % para PIB pc promedio 2023:")
print(f"  Media: ${media:,.2f}k")
print(f"  IC:    [${ic[0]:,.2f}k, ${ic[1]:,.2f}k]")

# ---------------------------------------------------------------------------
# 4. Prueba t de una muestra
# ---------------------------------------------------------------------------

t_stat, p_value = stats.ttest_1samp(gdppc, popmean=20)
print(f"\nPrueba t (H₀: μ = 20k):")
print(f"  t = {t_stat:.4f}   p = {p_value:.4f}")

# ---------------------------------------------------------------------------
# 5. Prueba t de dos muestras (Welch)
# ---------------------------------------------------------------------------

europa = data_2023[data_2023["Continent"] == "Europe"]["GDPpc_usd"].dropna() / 1000
americas = data_2023[data_2023["Continent"] == "Americas"]["GDPpc_usd"].dropna() / 1000

t_stat2, p_val2 = stats.ttest_ind(europa, americas, equal_var=False)
print(f"\nPrueba t de dos muestras (Europa vs Américas):")
print(f"  Media Europa:   ${europa.mean():,.2f}k")
print(f"  Media Américas: ${americas.mean():,.2f}k")
print(f"  t = {t_stat2:.4f}   p = {p_val2:.6f}")

# ---------------------------------------------------------------------------
# 6. ANOVA de una vía
# ---------------------------------------------------------------------------

grupos = [
    data_2023[data_2023["Continent"] == c]["GDPpc_usd"].dropna() / 1000
    for c in data_2023["Continent"].dropna().unique()
]
f_stat, p_val_anova = stats.f_oneway(*grupos)
print(f"\nANOVA — PIB pc por región (2023):")
print(f"  F = {f_stat:.4f}   p = {p_val_anova:.6f}")

# ---------------------------------------------------------------------------
# 7. Regresión lineal simple
# ---------------------------------------------------------------------------

datos_reg = data_2023.dropna(subset=["GDPpc_usd", "rgrowth"]).copy()
datos_reg["GDPpc_miles"] = datos_reg["GDPpc_usd"] / 1000

modelo = smf.ols("rgrowth ~ GDPpc_miles", data=datos_reg).fit()
print("\nRegresión lineal simple: rgrowth ~ GDPpc_miles")
print(modelo.summary().tables[1])
print(f"R²: {modelo.rsquared:.4f}")

# Gráfico de regresión
x_line = np.linspace(datos_reg["GDPpc_miles"].min(),
                     datos_reg["GDPpc_miles"].max(), 200)
y_pred = modelo.params["Intercept"] + modelo.params["GDPpc_miles"] * x_line

plt.figure(figsize=(8, 5))
plt.scatter(datos_reg["GDPpc_miles"], datos_reg["rgrowth"],
            color="steelblue", edgecolors="black", alpha=0.7, s=40)
plt.plot(x_line, y_pred, color="red", linewidth=2)
plt.title("Regresión: Crecimiento PIB ~ PIB per cápita")
plt.xlabel("PIB per cápita (miles USD)")
plt.ylabel("Crecimiento del PIB real (%)")
plt.tight_layout()
plt.savefig("../outputs/figures/live_06_regresion.png", dpi=150)
plt.show()
print("\nFigura guardada en outputs/figures/live_06_regresion.png")
