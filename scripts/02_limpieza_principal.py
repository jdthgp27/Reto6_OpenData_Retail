# ============================================================
# RETO 6 — Limpieza del dataset principal
# Dataset: Online Retail II
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# --- Rutas ---
BASE = Path(__file__).resolve().parent.parent
RUTA_INPUT = BASE / "datos" / "principal" / "online_retail_completo.csv"
RUTA_OUTPUT = BASE / "datos" / "principal" / "online_retail_limpio.csv"

# --- Carga ---
print("=" * 60)
print("LIMPIEZA DEL DATASET PRINCIPAL")
print("=" * 60)

df = pd.read_csv(RUTA_INPUT)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print(f"\nFilas originales: {len(df):,}")
print(f"Columnas: {df.columns.tolist()}")

# --- Verificación de nulos ---
print("\n--- Nulos por columna ---")
print(df.isnull().sum())

# --- Eliminar nulos en columnas clave ---
filas_antes = len(df)
df = df.dropna(subset=['CustomerID', 'Description'])
print(f"\nFilas tras eliminar nulos en CustomerID y Description: {len(df):,} "
      f"(-{filas_antes - len(df):,})")

# --- Eliminar duplicados ---
filas_antes = len(df)
df = df.drop_duplicates()
print(f"Filas tras eliminar duplicados: {len(df):,} (-{filas_antes - len(df):,})")

# --- Eliminar valores negativos o cero en Quantity y UnitPrice ---
filas_antes = len(df)
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
print(f"Filas tras eliminar Quantity/UnitPrice <= 0: {len(df):,} "
      f"(-{filas_antes - len(df):,})")

# --- Recalcular TotalPrice ---
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# --- Añadir columna Year (por si no está) ---
df['Year'] = df['InvoiceDate'].dt.year

# --- Resumen final ---
print(f"\n--- Dataset principal limpio ---")
print(f"Filas finales: {len(df):,}")
print(f"Columnas: {len(df.columns)}")
print(f"Rango temporal: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")
print(f"Ingresos totales: £{df['TotalPrice'].sum():,.2f}")

# --- Guardar ---
df.to_csv(RUTA_OUTPUT, index=False)
print(f"\n✅ Guardado: {RUTA_OUTPUT}")