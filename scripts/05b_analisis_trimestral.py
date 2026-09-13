# ============================================================
# RETO 6 — Análisis comparativo a nivel trimestral
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

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ============================================================
# 1. CARGA
# ============================================================
print("=" * 60)
print("ANÁLISIS TRIMESTRAL — RETO 6")
print("=" * 60)

df = pd.read_csv(RUTA_ENRIQUECIDO)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# ============================================================
# 2. AGREGACIÓN TRIMESTRAL
# ============================================================
df['Year_Quarter'] = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)

df_trim = df.groupby(['Year', 'Quarter', 'Year_Quarter']).agg(
    Ventas_Totales=('TotalPrice', 'sum'),
    Ventas_Ajustadas=('TotalPrice_Ajustado_Inflacion', 'sum'),
    Pedidos=('InvoiceNo', 'nunique'),
    Clientes=('CustomerID', 'nunique'),
    GDP_USD=('GDP_USD', 'first'),
    Inflation_pct=('Inflation_pct', 'first'),
    Unemployment_pct=('Unemployment_pct', 'first'),
    Population_Total=('Population_Total', 'first')
).reset_index().sort_values(['Year', 'Quarter'])

df_trim['Ventas_per_Capita'] = df_trim['Ventas_Totales'] / df_trim['Population_Total']

print("\nAgregación trimestral:")
print(df_trim[['Year_Quarter', 'Ventas_Totales', 'Pedidos', 'Clientes',
               'Inflation_pct', 'Unemployment_pct']].to_string(index=False))

df_trim.to_csv(RUTA_RESULTADOS / "analisis_trimestral.csv", index=False)

# ============================================================
# 3. CORRELACIONES (excluyendo Q4 2009 que es incompleto)
# ============================================================
print("\n" + "=" * 60)
print("CORRELACIONES TRIMESTRALES (Q1 2010 – Q4 2011)")
print("=" * 60)

df_trim_ok = df_trim[df_trim['Year_Quarter'] != '2009-Q4'].copy()

correlaciones = {
    'Ventas vs GDP': df_trim_ok['Ventas_Totales'].corr(df_trim_ok['GDP_USD']),
    'Ventas vs Inflación': df_trim_ok['Ventas_Totales'].corr(df_trim_ok['Inflation_pct']),
    'Ventas vs Desempleo': df_trim_ok['Ventas_Totales'].corr(df_trim_ok['Unemployment_pct']),
    'Ventas vs Población': df_trim_ok['Ventas_Totales'].corr(df_trim_ok['Population_Total'])
}

print(f"\nNº de trimestres analizados: {len(df_trim_ok)}")
for k, v in correlaciones.items():
    interpretacion = "fuerte" if abs(v) > 0.7 else ("moderada" if abs(v) > 0.4 else "débil")
    signo = "positiva" if v > 0 else "negativa"
    print(f"   {k}: {v:+.4f} ({signo} {interpretacion})")

pd.DataFrame(list(correlaciones.items()), columns=['Relación', 'Correlación']).to_csv(
    RUTA_RESULTADOS / "correlaciones_trimestrales.csv", index=False
)

# ============================================================
# 4. VISUALIZACIÓN: Ventas trimestrales vs Indicadores
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# --- Ventas trimestrales ---
ax = axes[0, 0]
ax.bar(range(len(df_trim)), df_trim['Ventas_Totales'] / 1e3, color='steelblue')
ax.set_xticks(range(len(df_trim)))
ax.set_xticklabels(df_trim['Year_Quarter'], rotation=45, ha='right')
ax.set_ylabel('Ventas (£ miles)')
ax.set_title('Evolución trimestral de ventas', fontweight='bold')
ax.grid(True, alpha=0.3)

# --- Ventas vs Inflación ---
ax = axes[0, 1]
ax.scatter(df_trim_ok['Inflation_pct'], df_trim_ok['Ventas_Totales'] / 1e3,
           color='crimson', s=100, alpha=0.7)
for i, row in df_trim_ok.iterrows():
    ax.annotate(row['Year_Quarter'],
                (row['Inflation_pct'], row['Ventas_Totales'] / 1e3),
                fontsize=8, alpha=0.7)
ax.set_xlabel('Inflación (%)')
ax.set_ylabel('Ventas (£ miles)')
ax.set_title('Ventas vs Inflación', fontweight='bold')
ax.grid(True, alpha=0.3)

# --- Ventas vs Desempleo ---
ax = axes[1, 0]
ax.scatter(df_trim_ok['Unemployment_pct'], df_trim_ok['Ventas_Totales'] / 1e3,
           color='purple', s=100, alpha=0.7)
for i, row in df_trim_ok.iterrows():
    ax.annotate(row['Year_Quarter'],
                (row['Unemployment_pct'], row['Ventas_Totales'] / 1e3),
                fontsize=8, alpha=0.7)
ax.set_xlabel('Desempleo (%)')
ax.set_ylabel('Ventas (£ miles)')
ax.set_title('Ventas vs Desempleo', fontweight='bold')
ax.grid(True, alpha=0.3)

# --- Ventas vs GDP ---
ax = axes[1, 1]
ax.scatter(df_trim_ok['GDP_USD'] / 1e12, df_trim_ok['Ventas_Totales'] / 1e3,
           color='darkgreen', s=100, alpha=0.7)
for i, row in df_trim_ok.iterrows():
    ax.annotate(row['Year_Quarter'],
                (row['GDP_USD'] / 1e12, row['Ventas_Totales'] / 1e3),
                fontsize=8, alpha=0.7)
ax.set_xlabel('PIB UK (billones US$)')
ax.set_ylabel('Ventas (£ miles)')
ax.set_title('Ventas vs PIB', fontweight='bold')
ax.grid(True, alpha=0.3)

plt.suptitle('Análisis trimestral: Ventas vs Indicadores Económicos', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "07_analisis_trimestral.png", dpi=100, bbox_inches='tight')
plt.close()
print("\n✅ Guardado: 07_analisis_trimestral.png")

# ============================================================
# 5. MATRIZ CORRELACIONES TRIMESTRAL
# ============================================================
cols = ['Ventas_Totales', 'GDP_USD', 'Inflation_pct', 'Unemployment_pct', 'Population_Total']
matriz = df_trim_ok[cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(matriz, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, ax=ax,
            cbar_kws={'label': 'Correlación'})
ax.set_title('Matriz de correlaciones trimestrales (Q1 2010 – Q4 2011)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "08_matriz_correlaciones_trimestral.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 08_matriz_correlaciones_trimestral.png")

print("\n" + "=" * 60)
print("✅ ANÁLISIS TRIMESTRAL COMPLETADO")
print("=" * 60)