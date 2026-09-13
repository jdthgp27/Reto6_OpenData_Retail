# ============================================================
# RETO 6 — Limpieza de los Open Data
# World Bank + ONS
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# --- Rutas ---
BASE = Path(__file__).resolve().parent.parent
RUTA_RAW = BASE / "datos" / "open_data" / "raw"
RUTA_OUTPUT = BASE / "datos" / "open_data" / "open_data_limpio.csv"

# --- Función genérica para limpiar archivos del World Bank ---
def limpiar_world_bank(ruta_archivo, nombre_indicador, anios=[2009, 2010, 2011]):
    """
    Convierte un archivo CSV del World Bank de formato ancho a largo,
    filtrando por United Kingdom y los años indicados.
    """
    df = pd.read_csv(ruta_archivo, skiprows=4)
    # Filtrar solo UK
    df = df[df['Country Code'] == 'GBR'].copy()
    # Seleccionar columnas de años
    columnas_anios = [str(a) for a in anios]
    df = df[['Country Name'] + columnas_anios]
    # Convertir de ancho a largo
    df = df.melt(id_vars=['Country Name'],
                 value_vars=columnas_anios,
                 var_name='Year',
                 value_name=nombre_indicador)
    df['Year'] = df['Year'].astype(int)
    df = df.drop(columns=['Country Name'])
    return df

# ============================================================
# 1. Indicadores del World Bank
# ============================================================

print("=" * 60)
print("LIMPIEZA DE INDICADORES DEL WORLD BANK")
print("=" * 60)

# PIB
df_gdp = limpiar_world_bank(RUTA_RAW / "world_bank_uk_gdp.csv", "GDP_USD")
print(f"\nPIB:")
print(df_gdp)

# Inflación
df_infl = limpiar_world_bank(RUTA_RAW / "world_bank_uk_inflation.csv", "Inflation_pct")
print(f"\nInflación:")
print(df_infl)

# Desempleo
df_unemp = limpiar_world_bank(RUTA_RAW / "world_bank_uk_unemployment.csv", "Unemployment_pct")
print(f"\nDesempleo:")
print(df_unemp)

# Población total
df_pop = limpiar_world_bank(RUTA_RAW / "world_bank_uk_population.csv", "Population_Total")
print(f"\nPoblación total:")
print(df_pop)

# Unir todos los indicadores económicos
df_open = df_gdp.merge(df_infl, on='Year').merge(df_unemp, on='Year').merge(df_pop, on='Year')
print("\n--- Dataset Open Data consolidado ---")
print(df_open)

# ============================================================
# 2. Población por región (ONS)
# ============================================================

print("\n" + "=" * 60)
print("POBLACIÓN POR REGIÓN (ONS)")
print("=" * 60)

# Leer el archivo ONS (Excel)
ruta_ons = RUTA_RAW / "ons_uk_population_by_region.xlsx"

# Detectar si es CSV o XLSX
if ruta_ons.exists():
    df_ons = pd.read_excel(ruta_ons, skiprows=6)
else:
    ruta_ons_csv = RUTA_RAW / "ons_uk_population_by_region.csv"
    df_ons = pd.read_csv(ruta_ons_csv, skiprows=6)

print(f"\nColumnas del archivo ONS: {df_ons.columns.tolist()}")
print(f"Primeras filas:\n{df_ons.head(10)}")

# --- Guardar datasets intermedios ---
df_open.to_csv(BASE / "datos" / "open_data" / "indicadores_economicos.csv", index=False)
print(f"\n✅ Guardado: indicadores_economicos.csv")