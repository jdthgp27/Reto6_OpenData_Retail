# ============================================================
# RETO 6 — Análisis comparativo y visualizaciones
# Comparación: dataset original vs dataset enriquecido
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Rutas ---
BASE = Path(__file__).resolve().parent.parent
RUTA_ENRIQUECIDO = BASE / "datos" / "enriquecido" / "Dataset_Enriquecido_Reto6_JuditGiravent.csv"
RUTA_FIGURAS = BASE / "salidas" / "figuras"
RUTA_RESULTADOS = BASE / "salidas" / "resultados"
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

# --- Estilo ---
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ============================================================
# 1. CARGA
# ============================================================
print("=" * 60)
print("ANÁLISIS COMPARATIVO — RETO 6")
print("=" * 60)

df = pd.read_csv(RUTA_ENRIQUECIDO)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print(f"\nDataset enriquecido cargado: {len(df):,} filas, {df.shape[1]} columnas")

# ============================================================
# 2. AGREGACIÓN POR AÑO
# ============================================================
print("\n" + "=" * 60)
print("AGREGACIÓN POR AÑO")
print("=" * 60)

df_anual = df.groupby('Year').agg(
    Ventas_Totales=('TotalPrice', 'sum'),
    Ventas_Ajustadas_Inflacion=('TotalPrice_Ajustado_Inflacion', 'sum'),
    Pedidos=('InvoiceNo', 'nunique'),
    Clientes=('CustomerID', 'nunique'),
    GDP_USD=('GDP_USD', 'first'),
    Inflation_pct=('Inflation_pct', 'first'),
    Unemployment_pct=('Unemployment_pct', 'first'),
    Population_Total=('Population_Total', 'first')
).reset_index()

# Calcular ventas per cápita (a nivel anual)
df_anual['Ventas_per_Capita'] = df_anual['Ventas_Totales'] / df_anual['Population_Total']
df_anual['Ventas_por_Millon_PIB'] = df_anual['Ventas_Totales'] / (df_anual['GDP_USD'] / 1e6)

print(df_anual.to_string(index=False))

df_anual.to_csv(RUTA_RESULTADOS / "analisis_anual.csv", index=False)

# ============================================================
# 3. COMPARATIVA ANTES/DESPUÉS — VENTAS AJUSTADAS
# ============================================================
print("\n" + "=" * 60)
print("COMPARATIVA: VENTAS ORIGINALES vs AJUSTADAS POR INFLACIÓN")
print("=" * 60)

comparativa_ajuste = df_anual[['Year', 'Ventas_Totales', 'Ventas_Ajustadas_Inflacion']].copy()
comparativa_ajuste['Diferencia'] = comparativa_ajuste['Ventas_Totales'] - comparativa_ajuste['Ventas_Ajustadas_Inflacion']
comparativa_ajuste['Diferencia_pct'] = (
    comparativa_ajuste['Diferencia'] / comparativa_ajuste['Ventas_Totales'] * 100
)
print(comparativa_ajuste.to_string(index=False))

comparativa_ajuste.to_csv(RUTA_RESULTADOS / "comparativa_ajuste_inflacion.csv", index=False)

# ============================================================
# 4. CORRELACIONES
# ============================================================
print("\n" + "=" * 60)
print("CORRELACIONES VENTAS vs INDICADORES")
print("=" * 60)

# Usar solo 2010 y 2011 (2009 está incompleto)
df_anual_completo = df_anual[df_anual['Year'] >= 2010].copy()

correlaciones = {
    'Ventas vs GDP': df_anual_completo['Ventas_Totales'].corr(df_anual_completo['GDP_USD']),
    'Ventas vs Inflación': df_anual_completo['Ventas_Totales'].corr(df_anual_completo['Inflation_pct']),
    'Ventas vs Desempleo': df_anual_completo['Ventas_Totales'].corr(df_anual_completo['Unemployment_pct']),
    'Ventas vs Población': df_anual_completo['Ventas_Totales'].corr(df_anual_completo['Population_Total'])
}

print("\nCoeficientes de correlación (2010-2011):")
for k, v in correlaciones.items():
    print(f"   {k}: {v:.4f}")

pd.DataFrame(list(correlaciones.items()), columns=['Relación', 'Correlación']).to_csv(
    RUTA_RESULTADOS / "correlaciones.csv", index=False
)

# ============================================================
# VISUALIZACIÓN 1: Ventas vs PIB por año
# ============================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = 'steelblue'
color2 = 'darkorange'

ax1.bar(df_anual['Year'], df_anual['Ventas_Totales'] / 1e6, color=color1, alpha=0.7, label='Ventas')
ax1.set_xlabel('Año')
ax1.set_ylabel('Ventas (£ millones)', color=color1)
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(df_anual['Year'])

ax2 = ax1.twinx()
ax2.plot(df_anual['Year'], df_anual['GDP_USD'] / 1e12, color=color2,
         marker='o', linewidth=2, markersize=10, label='PIB UK')
ax2.set_ylabel('PIB (£ billones)', color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Ventas vs PIB del Reino Unido (2009-2011)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig(RUTA_FIGURAS / "01_ventas_vs_pib.png", dpi=100, bbox_inches='tight')
plt.close()
print("\n✅ Guardado: 01_ventas_vs_pib.png")

# ============================================================
# VISUALIZACIÓN 2: Ventas vs Inflación
# ============================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(df_anual['Year'], df_anual['Ventas_Totales'] / 1e6,
        color='steelblue', alpha=0.7, label='Ventas')
ax1.set_xlabel('Año')
ax1.set_ylabel('Ventas (£ millones)', color='steelblue')
ax1.set_xticks(df_anual['Year'])

ax2 = ax1.twinx()
ax2.plot(df_anual['Year'], df_anual['Inflation_pct'],
         color='crimson', marker='s', linewidth=2, markersize=10, label='Inflación')
ax2.set_ylabel('Inflación (%)', color='crimson')

plt.title('Ventas vs Inflación (2009-2011)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig(RUTA_FIGURAS / "02_ventas_vs_inflacion.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 02_ventas_vs_inflacion.png")

# ============================================================
# VISUALIZACIÓN 3: Ventas originales vs ajustadas por inflación
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(df_anual))
width = 0.35

ax.bar(x - width/2, df_anual['Ventas_Totales'] / 1e6, width,
       label='Ventas originales', color='steelblue')
ax.bar(x + width/2, df_anual['Ventas_Ajustadas_Inflacion'] / 1e6, width,
       label='Ventas ajustadas por inflación', color='darkorange')

ax.set_xlabel('Año')
ax.set_ylabel('Ventas (£ millones)')
ax.set_title('Comparativa: Ventas originales vs ajustadas por inflación',
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df_anual['Year'])
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "03_ventas_ajustadas.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 03_ventas_ajustadas.png")

# ============================================================
# VISUALIZACIÓN 4: Ventas per cápita
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(df_anual['Year'], df_anual['Ventas_per_Capita'] * 1e6,
       color='mediumseagreen', edgecolor='black')
ax.set_xlabel('Año')
ax.set_ylabel('Ventas per cápita (millonésimas de £)')
ax.set_title('Ventas per cápita por año (ventas / población UK)',
             fontsize=14, fontweight='bold')
ax.set_xticks(df_anual['Year'])
ax.grid(True, alpha=0.3)

for i, v in enumerate(df_anual['Ventas_per_Capita'] * 1e6):
    ax.text(df_anual['Year'][i], v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "04_ventas_per_capita.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 04_ventas_per_capita.png")

# ============================================================
# VISUALIZACIÓN 5: Ventas vs Desempleo
# ============================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(df_anual['Year'], df_anual['Ventas_Totales'] / 1e6,
        color='steelblue', alpha=0.7, label='Ventas')
ax1.set_xlabel('Año')
ax1.set_ylabel('Ventas (£ millones)', color='steelblue')
ax1.set_xticks(df_anual['Year'])

ax2 = ax1.twinx()
ax2.plot(df_anual['Year'], df_anual['Unemployment_pct'],
         color='purple', marker='^', linewidth=2, markersize=10, label='Desempleo')
ax2.set_ylabel('Desempleo (%)', color='purple')

plt.title('Ventas vs Desempleo en UK (2009-2011)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig(RUTA_FIGURAS / "05_ventas_vs_desempleo.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 05_ventas_vs_desempleo.png")

# ============================================================
# VISUALIZACIÓN 6: Matriz de correlaciones
# ============================================================
cols_corr = ['Ventas_Totales', 'GDP_USD', 'Inflation_pct', 'Unemployment_pct', 'Population_Total']
matriz_corr = df_anual[cols_corr].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(matriz_corr, annot=True, fmt='.3f', cmap='coolwarm',
            center=0, square=True, linewidths=1, ax=ax,
            cbar_kws={'label': 'Correlación'})
ax.set_title('Matriz de correlaciones (2009-2011)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "06_matriz_correlaciones.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 06_matriz_correlaciones.png")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "=" * 60)
print("✅ ANÁLISIS COMPARATIVO COMPLETADO")
print("=" * 60)
print(f"\nFiguras guardadas en: {RUTA_FIGURAS}")
print(f"Resultados CSV en: {RUTA_RESULTADOS}")