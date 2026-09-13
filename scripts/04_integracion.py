# ============================================================
# RETO 6 — Integración de datasets (principal + Open Data)
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# --- Rutas ---
BASE = Path(__file__).resolve().parent.parent
RUTA_PRINCIPAL = BASE / "datos" / "principal" / "online_retail_limpio.csv"
RUTA_INDICADORES = BASE / "datos" / "open_data" / "indicadores_economicos.csv"
RUTA_POBLACION_REG = BASE / "datos" / "open_data" / "raw" / "ons_uk_population_by_region.xlsx"
RUTA_OUTPUT = BASE / "datos" / "enriquecido" / "Dataset_Enriquecido_Reto6_JuditGiravent.csv"

# ============================================================
# 1. CARGA DE DATOS
# ============================================================
print("=" * 60)
print("INTEGRACIÓN DE DATASETS")
print("=" * 60)

# Dataset principal
print("\n1. Cargando dataset principal...")
df_principal = pd.read_csv(RUTA_PRINCIPAL)
df_principal['InvoiceDate'] = pd.to_datetime(df_principal['InvoiceDate'])
print(f"   Filas: {len(df_principal):,}")
print(f"   Años disponibles: {sorted(df_principal['Year'].unique())}")

# Indicadores económicos
print("\n2. Cargando indicadores económicos...")
df_indicadores = pd.read_csv(RUTA_INDICADORES)
print(f"   Filas: {len(df_indicadores)}")
print(df_indicadores)

# Población por región
print("\n3. Cargando población por región...")
df_pob_region = pd.read_excel(RUTA_POBLACION_REG, skiprows=6)
print(f"   Filas: {len(df_pob_region)}")
print(f"   Columnas: {df_pob_region.columns.tolist()}")
print(df_pob_region)

# ============================================================
# 2. TRANSFORMAR POBLACIÓN POR REGIÓN (ancho → largo)
# ============================================================
print("\n" + "=" * 60)
print("TRANSFORMANDO POBLACIÓN POR REGIÓN")
print("=" * 60)

# Detectar columnas de años
columnas_anio = [c for c in df_pob_region.columns if str(c).isdigit()]
print(f"   Columnas de años detectadas: {columnas_anio}")

# Convertir de formato ancho a largo
df_pob_region_largo = df_pob_region.melt(
    id_vars=['region'],
    value_vars=columnas_anio,
    var_name='Year',
    value_name='Population_Region'
)

# Asegurar que Year es entero
df_pob_region_largo['Year'] = df_pob_region_largo['Year'].astype(int)

print(f"   Filas tras transformación: {len(df_pob_region_largo)}")
print(df_pob_region_largo.head(10))

# ============================================================
# 3. INTEGRACIÓN PRINCIPAL (JOIN POR AÑO)
# ============================================================
print("\n" + "=" * 60)
print("INTEGRACIÓN POR AÑO")
print("=" * 60)

# Left Join: preservamos todas las filas del dataset principal
filas_antes = len(df_principal)
df_enriquecido = df_principal.merge(df_indicadores, on='Year', how='left')
filas_despues = len(df_enriquecido)

print(f"   Filas antes: {filas_antes:,}")
print(f"   Filas después: {filas_despues:,}")
print(f"   Columnas nuevas: {[c for c in df_enriquecido.columns if c not in df_principal.columns]}")

# Verificar nulos en columnas del Open Data
print("\n   Verificación de coincidencias:")
for col in ['GDP_USD', 'Inflation_pct', 'Unemployment_pct', 'Population_Total']:
    nulos = df_enriquecido[col].isnull().sum()
    print(f"   - {col}: {nulos} nulos ({nulos/len(df_enriquecido)*100:.2f}%)")

# ============================================================
# 4. CREACIÓN DE NUEVAS VARIABLES
# ============================================================
print("\n" + "=" * 60)
print("CREACIÓN DE NUEVAS VARIABLES")
print("=" * 60)

# 4.1 Ventas ajustadas por inflación
# Fórmula: TotalPrice / (1 + Inflation_pct/100)
df_enriquecido['TotalPrice_Ajustado_Inflacion'] = (
    df_enriquecido['TotalPrice'] / (1 + df_enriquecido['Inflation_pct'] / 100)
)

# 4.2 Ventas por PIB (ratio de contribución al PIB)
# Fórmula: TotalPrice / GDP_USD * 10^9 (para escala)
df_enriquecido['Ventas_por_PIB'] = (
    df_enriquecido['TotalPrice'] / df_enriquecido['GDP_USD'] * 1e9
)

# 4.3 Ventas per cápita (a nivel nacional)
df_enriquecido['Ventas_per_Capita'] = (
    df_enriquecido['TotalPrice'] / df_enriquecido['Population_Total']
)

# 4.4 Crecimiento anual de ventas (por año)
ventas_por_anio = df_enriquecido.groupby('Year')['TotalPrice'].sum().reset_index()
ventas_por_anio['Crecimiento_Ventas_pct'] = ventas_por_anio['TotalPrice'].pct_change() * 100
print("\n   Crecimiento anual de ventas:")
print(ventas_por_anio)

print("\n   Nuevas variables creadas:")
print("   - TotalPrice_Ajustado_Inflacion")
print("   - Ventas_por_PIB")
print("   - Ventas_per_Capita")

# ============================================================
# 5. VERIFICACIÓN DE LA INTEGRACIÓN
# ============================================================
print("\n" + "=" * 60)
print("VERIFICACIÓN FINAL")
print("=" * 60)

print(f"\n   Dimensiones del dataset enriquecido: {df_enriquecido.shape}")
print(f"   Columnas: {df_enriquecido.columns.tolist()}")
print(f"\n   Primeras filas:")
print(df_enriquecido.head(3))

print(f"\n   Estadísticas de las nuevas variables:")
nuevas_vars = ['TotalPrice_Ajustado_Inflacion', 'Ventas_por_PIB', 'Ventas_per_Capita']
print(df_enriquecido[nuevas_vars].describe())

# ============================================================
# 6. GUARDAR DATASET ENRIQUECIDO
# ============================================================
print("\n" + "=" * 60)
print("GUARDANDO DATASET ENRIQUECIDO")
print("=" * 60)

df_enriquecido.to_csv(RUTA_OUTPUT, index=False)
print(f"\n✅ Guardado: {RUTA_OUTPUT}")
print(f"   Filas: {len(df_enriquecido):,}")
print(f"   Columnas: {len(df_enriquecido.columns)}")

# Guardar también la población por región transformada
ruta_pob_largo = BASE / "datos" / "open_data" / "poblacion_por_region.csv"
df_pob_region_largo.to_csv(ruta_pob_largo, index=False)
print(f"✅ Guardado: {ruta_pob_largo}")