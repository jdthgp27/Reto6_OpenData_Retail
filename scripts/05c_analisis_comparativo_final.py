# ============================================================
# RETO 6 — Análisis comparativo final
# Enfoque: valor añadido del Open Data sin correlaciones forzadas
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RUTA_ENRIQUECIDO = BASE / "datos" / "enriquecido" / "Dataset_Enriquecido_Reto6_JuditGiravent.csv"
RUTA_FIGURAS = BASE / "salidas" / "figuras"
RUTA_RESULTADOS = BASE / "salidas" / "resultados"

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

print("=" * 60)
print("ANÁLISIS COMPARATIVO FINAL — RETO 6")
print("=" * 60)

# ============================================================
# 1. CARGA Y AGREGACIÓN
# ============================================================
df = pd.read_csv(RUTA_ENRIQUECIDO)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Agregación anual
df_anual = df.groupby('Year').agg(
    Ventas_Totales=('TotalPrice', 'sum'),
    Ventas_Ajustadas=('TotalPrice_Ajustado_Inflacion', 'sum'),
    Pedidos=('InvoiceNo', 'nunique'),
    Clientes=('CustomerID', 'nunique'),
    GDP_USD=('GDP_USD', 'first'),
    Inflation=('Inflation_pct', 'first'),
    Desempleo=('Unemployment_pct', 'first'),
    Poblacion=('Population_Total', 'first')
).reset_index()

# Calcular ratios
df_anual['Ventas_per_Capita'] = df_anual['Ventas_Totales'] / df_anual['Poblacion']
df_anual['Ventas_por_Billón_PIB'] = df_anual['Ventas_Totales'] / (df_anual['GDP_USD'] / 1e12)
df_anual['Penetración_por_mil_hab'] = df_anual['Clientes'] / df_anual['Poblacion'] * 1000

# ============================================================
# 2. ANÁLISIS: IMPACTO REAL DE LA INFLACIÓN
# ============================================================
print("\n" + "=" * 60)
print("ANÁLISIS 1: IMPACTO DE LA INFLACIÓN EN LAS VENTAS")
print("=" * 60)

df_anual['Diferencia_Inflación'] = df_anual['Ventas_Totales'] - df_anual['Ventas_Ajustadas']
df_anual['Pérdida_por_Inflación_pct'] = (
    df_anual['Diferencia_Inflación'] / df_anual['Ventas_Totales'] * 100
)

print("\nVentas nominales vs ajustadas por inflación:")
for _, row in df_anual.iterrows():
    print(f"  {int(row['Year'])}: Nominal £{row['Ventas_Totales']:>12,.0f} | "
          f"Ajustada £{row['Ventas_Ajustadas']:>12,.0f} | "
          f"Pérdida por inflación: {row['Pérdida_por_Inflación_pct']:.2f}%")

# ============================================================
# 3. ANÁLISIS: INTENSIDAD DE MERCADO
# ============================================================
print("\n" + "=" * 60)
print("ANÁLISIS 2: INTENSIDAD DE MERCADO (ratios)")
print("=" * 60)

print("\nVentas per cápita (cuánto gasta cada británico):")
for _, row in df_anual.iterrows():
    print(f"  {int(row['Year'])}: £{row['Ventas_per_Capita']:.6f}")

print("\nVentas por billón de PIB (penetración en la economía):")
for _, row in df_anual.iterrows():
    print(f"  {int(row['Year'])}: £{row['Ventas_por_Billón_PIB']:,.2f} por billón de PIB")

print("\nClientes por mil habitantes (penetración de mercado):")
for _, row in df_anual.iterrows():
    print(f"  {int(row['Year'])}: {row['Penetración_por_mil_hab']:.4f} clientes por mil hab.")

# ============================================================
# 4. ANÁLISIS: ESTACIONALIDAD Y CONTEXTO ECONÓMICO
# ============================================================
print("\n" + "=" * 60)
print("ANÁLISIS 3: ESTACIONALIDAD vs CONTEXTO ECONÓMICO")
print("=" * 60)

# Ventas por trimestre
df['YQ'] = df['Year'].astype(str) + '-Q' + df['Quarter'].astype(str)
df_trim = df.groupby(['Year', 'Quarter', 'YQ']).agg(
    Ventas=('TotalPrice', 'sum'),
    Inflation=('Inflation_pct', 'first'),
    Desempleo=('Unemployment_pct', 'first')
).reset_index().sort_values(['Year', 'Quarter'])

# Excluir 2009 (incompleto)
df_trim_full = df_trim[df_trim['Year'] >= 2010].copy()

# Comparativa entre 2010 y 2011 (mismos trimestres)
print("\nComparación trimestre a trimestre (2010 vs 2011):")
for q in [1, 2, 3, 4]:
    v2010 = df_trim_full[(df_trim_full['Year']==2010) & (df_trim_full['Quarter']==q)]['Ventas'].values[0]
    v2011 = df_trim_full[(df_trim_full['Year']==2011) & (df_trim_full['Quarter']==q)]['Ventas'].values[0]
    variacion = (v2011 - v2010) / v2010 * 100
    print(f"  Q{q}: 2010=£{v2010:>10,.0f} | 2011=£{v2011:>10,.0f} | Variación: {variacion:+.2f}%")

# ============================================================
# 5. VISUALIZACIONES
# ============================================================

# --- Figura 1: Ventas nominales vs ajustadas por inflación ---
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(df_anual))
width = 0.35

bars1 = ax.bar(x - width/2, df_anual['Ventas_Totales'] / 1e6, width,
               label='Ventas nominales', color='steelblue', edgecolor='black')
bars2 = ax.bar(x + width/2, df_anual['Ventas_Ajustadas'] / 1e6, width,
               label='Ventas ajustadas por inflación', color='darkorange', edgecolor='black')

# Añadir valores sobre las barras
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'£{bar.get_height():.2f}M', ha='center', fontsize=9, fontweight='bold')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
            f'£{bar.get_height():.2f}M', ha='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Año')
ax.set_ylabel('Ventas (£ millones)')
ax.set_title('Ventas nominales vs ajustadas por inflación', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df_anual['Year'].astype(int))
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "09_ventas_nominales_vs_ajustadas.png", dpi=100, bbox_inches='tight')
plt.close()
print("\n✅ Guardado: 09_ventas_nominales_vs_ajustadas.png")

# --- Figura 2: Comparación trimestral 2010 vs 2011 ---
fig, ax = plt.subplots(figsize=(12, 6))

trim_2010 = df_trim_full[df_trim_full['Year'] == 2010]['Ventas'].values
trim_2011 = df_trim_full[df_trim_full['Year'] == 2011]['Ventas'].values

x = np.arange(4)
width = 0.35

bars1 = ax.bar(x - width/2, trim_2010 / 1e3, width,
               label='2010', color='steelblue', edgecolor='black')
bars2 = ax.bar(x + width/2, trim_2011 / 1e3, width,
               label='2011', color='coral', edgecolor='black')

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'£{bar.get_height():.0f}K', ha='center', fontsize=9)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'£{bar.get_height():.0f}K', ha='center', fontsize=9)

ax.set_xlabel('Trimestre')
ax.set_ylabel('Ventas (£ miles)')
ax.set_title('Comparación trimestral 2010 vs 2011', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "10_comparativa_trimestral_2010_2011.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 10_comparativa_trimestral_2010_2011.png")

# --- Figura 3: Ratios económicos por año ---
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Ventas per cápita
ax = axes[0]
ax.bar(df_anual['Year'].astype(int), df_anual['Ventas_per_Capita'] * 1e6,
       color='mediumseagreen', edgecolor='black')
for i, v in enumerate(df_anual['Ventas_per_Capita'] * 1e6):
    ax.text(df_anual['Year'].iloc[i], v + 0.005, f'{v:.3f}',
            ha='center', fontsize=10, fontweight='bold')
ax.set_title('Ventas per cápita', fontweight='bold')
ax.set_xlabel('Año')
ax.set_ylabel('Millonésimas de £')
ax.grid(True, alpha=0.3)

# Ventas por billón de PIB
ax = axes[1]
ax.bar(df_anual['Year'].astype(int), df_anual['Ventas_por_Billón_PIB'],
       color='coral', edgecolor='black')
for i, v in enumerate(df_anual['Ventas_por_Billón_PIB']):
    ax.text(df_anual['Year'].iloc[i], v + 0.05, f'{v:.2f}',
            ha='center', fontsize=10, fontweight='bold')
ax.set_title('Penetración en PIB', fontweight='bold')
ax.set_xlabel('Año')
ax.set_ylabel('£ por billón de PIB')
ax.grid(True, alpha=0.3)

# Clientes por mil habitantes
ax = axes[2]
ax.bar(df_anual['Year'].astype(int), df_anual['Penetración_por_mil_hab'],
       color='purple', edgecolor='black')
for i, v in enumerate(df_anual['Penetración_por_mil_hab']):
    ax.text(df_anual['Year'].iloc[i], v + 0.001, f'{v:.4f}',
            ha='center', fontsize=10, fontweight='bold')
ax.set_title('Penetración de mercado', fontweight='bold')
ax.set_xlabel('Año')
ax.set_ylabel('Clientes por mil hab.')
ax.grid(True, alpha=0.3)

plt.suptitle('Ratios económicos anuales', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "11_ratios_economicos.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 11_ratios_economicos.png")

# --- Figura 4: Estacionalidad con contexto económico ---
fig, ax1 = plt.subplots(figsize=(14, 6))

df_trim_plot = df_trim_full.copy()
x = range(len(df_trim_plot))

ax1.bar(x, df_trim_plot['Ventas'] / 1e3, color='steelblue', alpha=0.8,
        label='Ventas trimestrales', edgecolor='black')
ax1.set_xlabel('Trimestre')
ax1.set_ylabel('Ventas (£ miles)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.set_xticks(x)
ax1.set_xticklabels(df_trim_plot['YQ'], rotation=45, ha='right')

ax2 = ax1.twinx()
ax2.plot(x, df_trim_plot['Inflation'], color='crimson', marker='o',
         linewidth=2, markersize=10, label='Inflación (%)')
ax2.plot(x, df_trim_plot['Desempleo'], color='purple', marker='s',
         linewidth=2, markersize=8, label='Desempleo (%)', linestyle='--')
ax2.set_ylabel('Porcentaje (%)')
ax2.tick_params(axis='y')

# Leyendas
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Estacionalidad de ventas con contexto económico (2010-2011)',
          fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "12_estacionalidad_contexto.png", dpi=100, bbox_inches='tight')
plt.close()
print("✅ Guardado: 12_estacionalidad_contexto.png")

# ============================================================
# 6. GUARDAR RESULTADOS
# ============================================================
df_anual.to_csv(RUTA_RESULTADOS / "analisis_final_anual.csv", index=False)
df_trim_full.to_csv(RUTA_RESULTADOS / "analisis_final_trimestral.csv", index=False)

print("\n" + "=" * 60)
print("✅ ANÁLISIS COMPARATIVO FINAL COMPLETADO")
print("=" * 60)
print(f"\nFiguras: {RUTA_FIGURAS}")
print(f"Resultados: {RUTA_RESULTADOS}")