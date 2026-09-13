# INFORME DE ANÁLISIS
## Reto 6 — Creación de un dataset enriquecido con Open Data
### El Mercado de las Especias de Dataclysm

---

**Autora:** Judit Giravent  
**Fecha:** 09/2026  
**Herramientas:** Python 3.13 · pandas · matplotlib · seaborn · World Bank Open Data · ONS Nomis  
**Dataset principal:** Online Retail II (UCI Machine Learning Repository) — 767.853 transacciones limpias  
**Open Data:** World Bank (UK Economic Indicators) + ONS (Población por región)

---

## Índice

1. Resumen ejecutivo
2. Introducción y contexto
3. Paso 1: Selección del dataset principal
4. Paso 2: Búsqueda y selección de Open Data
5. Paso 3: Preparación de datos
6. Paso 4: Integración de datasets
7. Paso 5: Análisis comparativo
8. Paso 6: Conclusiones y recomendaciones
9. Anexos

---

## 1. Resumen ejecutivo

Este proyecto enriquece un dataset comercial de ventas con **Open Data** procedente del **World Bank** y del **ONS (Office for National Statistics)**, para realizar un análisis comparativo que revele insights imposibles de obtener con los datos internos por sí solos.

### Resultados principales

- **Dataset enriquecido:** 767.853 transacciones con 25 columnas (18 originales + 4 Open Data + 3 derivadas).
- **Impacto de la inflación:** las ventas reales de 2011 perdieron **£282.555** (3,71%) por el aumento de la inflación (2,49% → 3,86%).
- **Caída del Q4 2011:** la campaña navideña cayó un **16,9%** respecto a 2010, coincidiendo con el pico de inflación y desempleo.
- **Divergencia con la economía:** el PIB UK creció un **+7,2%** entre 2010 y 2011, mientras las ventas de la tienda cayeron un **-7%**.

### Conclusión principal

El Open Data ha permitido **contextualizar las ventas en el entorno macroeconómico británico**, revelando que la tienda **no está aprovechando el crecimiento económico del país** y que sufre especialmente en períodos de alta inflación.

---

## 2. Introducción y contexto

### 2.1 Contexto narrativo

En la isla de Dataclysm, los mercaderes del Mercado de las Especias han acumulado grandes volúmenes de datos internos. Sin embargo, para comprender su posición real en el mercado, necesitan **comparar sus operaciones con información del mundo exterior**.

La **Torre del Conocimiento** simboliza el acceso a la vasta red de **Open Data** — datos públicos, gratuitos y abiertos — que permiten enriquecer el análisis con contexto económico, demográfico y social.

### 2.2 Objetivo del reto

Utilizar datos abiertos para enriquecer un conjunto de datos comerciales y realizar un **análisis comparativo** que revele nuevas perspectivas.

### 2.3 Metodología

| Paso | Descripción | Herramienta |
|---|---|---|
| 1 | Selección del dataset principal | UCI Repository |
| 2 | Búsqueda de Open Data | World Bank + ONS |
| 3 | Preparación de datos | pandas |
| 4 | Integración de datasets | pandas (merge) |
| 5 | Análisis comparativo | matplotlib + seaborn |
| 6 | Conclusiones y recomendaciones | Análisis de negocio |

---

## 3. Paso 1: Selección del dataset principal

### 3.1 Enfoque del análisis

Se decidió trabajar con **datos de ventas** porque permiten:
- Analizar tendencias temporales y estacionalidad.
- Detectar patrones de comportamiento del cliente.
- Evaluar el impacto de factores externos (economía, inflación, desempleo).

### 3.2 Dataset seleccionado

**Nombre:** Online Retail II  
**Fuente:** UCI Machine Learning Repository  
**URL:** https://archive.ics.uci.edu/dataset/502/online+retail+ii  
**Periodo:** Diciembre 2009 – Diciembre 2011  
**País:** Reino Unido

| Característica | Valor |
|---|---|
| Instancias originales | 1.067.371 |
| Instancias tras limpieza | **767.853** |
| Variables | 18 columnas |
| Tipo | Transacciones de comercio electrónico |

### 3.3 Justificación

1. **Dataset real y grande** (casi 1M transacciones).
2. **Variable temporal** (`InvoiceDate`) que permite cruzar con Open Data por año.
3. **País identificado** (`Country`) que permite cruzar con indicadores UK.
4. **Volumen suficiente** para un análisis comparativo significativo.

### 3.4 Estructura del dataset principal

| Variable | Tipo | Descripción |
|---|---|---|
| `InvoiceNo` | Texto | Número de factura |
| `StockCode` | Texto | Código de producto |
| `Description` | Texto | Nombre del producto |
| `Quantity` | Entero | Cantidad vendida |
| `InvoiceDate` | Fecha | Fecha y hora de la transacción |
| `UnitPrice` | Decimal | Precio unitario |
| `CustomerID` | Entero | Identificador del cliente |
| `Country` | Texto | País de residencia |
| `TotalPrice` | Decimal | Importe total (Quantity × UnitPrice) |
| `Year` | Entero | Año de la transacción |

---

## 4. Paso 2: Búsqueda y selección de Open Data

### 4.1 Tipos de Open Data seleccionados

Se decidió buscar **indicadores económicos del Reino Unido** porque:
- El dataset principal es de una tienda británica.
- Los indicadores macroeconómicos permiten contextualizar las ventas.
- Permiten crear variables derivadas (ventas ajustadas por inflación, ventas per cápita, etc.).

### 4.2 Fuentes seleccionadas

| Fuente | Open Data | Años |
|---|---|---|
| **World Bank Open Data** | PIB (GDP, current US$) | 2009-2011 |
| **World Bank Open Data** | Inflación (CPI, annual %) | 2009-2011 |
| **World Bank Open Data** | Desempleo (Unemployment, total %) | 2009-2011 |
| **World Bank Open Data** | Población total UK | 2009-2011 |
| **ONS Nomis** | Población por región UK | 2009-2011 |

### 4.3 Justificación de la elección

| Criterio | Cumple |
|---|---|
| **Fuente confiable** | World Bank y ONS son organismos oficiales |
| **Datos gratuitos y abiertos** | Licencia Open Data |
| **Compatible estructuralmente** | Variable común: `Year` |
| **Período coincidente** | 2009-2011 (igual que el dataset principal) |
| **Aporte de valor** | Contexto macroeconómico y demográfico |

### 4.4 Indicadores obtenidos

| Indicador | 2009 | 2010 | 2011 |
|---|---|---|---|
| **PIB (US$)** | 2,43 B | 2,50 B | 2,68 B |
| **Inflación (%)** | 1,96% | 2,49% | 3,86% |
| **Desempleo (%)** | 7,68% | 7,97% | 8,20% |
| **Población total** | 62.276.270 | 62.766.365 | 63.258.810 |

---

## 5. Paso 3: Preparación de datos

### 5.1 Limpieza del dataset principal

| Paso | Filas antes | Filas después | Eliminadas |
|---|---|---|---|
| Carga inicial | 995.416 | — | — |
| Eliminar nulos en CustomerID y Description | 995.416 | 767.853 | -227.563 |
| Eliminar duplicados | 767.853 | 767.853 | 0 |
| Eliminar Quantity/UnitPrice ≤ 0 | 767.853 | 767.853 | 0 |

**Resultado:** 767.853 filas limpias (77,1% del original).

### 5.2 Limpieza del Open Data

Para cada archivo del World Bank (PIB, inflación, desempleo, población):
1. **Filtrar solo United Kingdom** (Country Code = GBR).
2. **Seleccionar los años 2009, 2010, 2011**.
3. **Transformar de formato ancho a largo** (de columnas de años a filas).
4. **Unir todos los indicadores** en una sola tabla por año.

Para el archivo ONS de población por región:
1. **Leer el archivo Excel** (12 regiones × 3 años).
2. **Transformar de formato ancho a largo**.
3. **Guardar como CSV limpio**.

### 5.3 Estructura compatible

Ambos datasets se han alineado con la variable común **`Year`** (entero) para permitir el cruce.

---

## 6. Paso 4: Integración de datasets

### 6.1 Tipo de integración

Se utilizó un **Left Join** (unión a la izquierda) porque:
- Preserva **todas las filas** del dataset principal.
- Añade los indicadores económicos donde coincida el año.
- Los años del principal (2009-2011) coinciden perfectamente con los del Open Data.

### 6.2 Resultado de la integración

| Métrica | Valor |
|---|---|
| Filas antes | 767.853 |
| Filas después | **767.853** |
| Columnas antes | 18 |
| Columnas después | **25** |
| Nulos en columnas Open Data | **0** (100% coincidencia) |

### 6.3 Nuevas variables creadas

| Variable | Fórmula | Uso |
|---|---|---|
| `TotalPrice_Ajustado_Inflacion` | TotalPrice / (1 + Inflation_pct/100) | Valor real de las ventas |
| `Ventas_por_PIB` | TotalPrice / GDP_USD × 10⁹ | Contribución relativa al PIB |
| `Ventas_per_Capita` | TotalPrice / Population_Total | Gasto por habitante |

---

## 7. Paso 5: Análisis comparativo

### 7.1 Agregación anual

| Año | Ventas Totales | Ventas Ajustadas | Pérdida Inflación | Pedidos | Clientes |
|---|---|---|---|---|---|
| 2009 | £641.499 | £629.157 | 1,92% | 1.500 | 952 |
| 2010 | £8.186.504 | £7.987.406 | 2,43% | 18.145 | 4.208 |
| 2011 | £7.610.008 | £7.327.453 | **3,71%** | 16.990 | 4.202 |

**Nota:** 2009 es un año parcial (solo diciembre).

### 7.2 Hallazgo 1 — Impacto de la inflación en las ventas

![Ventas nominales vs ajustadas](salidas/figuras/09_ventas_nominales_vs_ajustadas.png)

**Análisis:**
- **2011 fue el año con mayor inflación** (3,86%), y por tanto, la mayor pérdida de poder adquisitivo.
- Las ventas nominales de 2011 (£7,61M) equivalen a solo **£7,33M en precios de 2010**.
- **Pérdida real: £282.555** por el aumento de la inflación.

**Implicación:** el negocio **creció menos de lo que parece** en términos nominales. La inflación erosiona márgenes si no se ajustan precios.

### 7.3 Hallazgo 2 — Caída del Q4 2011

![Comparativa trimestral 2010 vs 2011](salidas/figuras/10_comparativa_trimestral_2010_2011.png)

| Trimestre | 2010 | 2011 | Variación |
|---|---|---|---|
| Q1 | £1.635.045 | £1.444.573 | **-11,65%** |
| Q2 | £1.753.506 | £1.655.063 | -5,61% |
| Q3 | £1.899.494 | £2.101.657 | **+10,64%** |
| Q4 | £2.898.459 | £2.408.715 | **-16,90%** |

**Análisis:**
- El **Q4 (campaña navideña) cayó un 16,9%** en 2011.
- Coincide con el **pico de inflación (3,86%)** y desempleo (8,20%) en UK.
- Los consumidores redujeron el gasto discrecional navideño.
- **Pérdida estimada: £489.744** en el Q4.

**Implicación:** el Q4 es el trimestre más importante del año. Una caída del 16,9% tiene un impacto desproporcionado en el resultado anual.

### 7.4 Hallazgo 3 — Divergencia con el crecimiento del PIB

![Ventas vs PIB](salidas/figuras/01_ventas_vs_pib.png)

| Indicador | 2010 | 2011 | Variación |
|---|---|---|---|
| **PIB UK** | 2,50 B US$ | 2,68 B US$ | **+7,20%** |
| **Ventas tienda** | £8.186.504 | £7.610.008 | **-7,04%** |

**Análisis:**
- La economía británica **creció un 7,2%** entre 2010 y 2011.
- Las ventas de la tienda **cayeron un 7,0%** en el mismo período.
- **La tienda va en dirección contraria a la economía.**

**Implicación:** la tienda está **perdiendo cuota de mercado** o tiene un problema de competitividad. No está aprovechando el crecimiento económico del país.

### 7.5 Ratios económicos anuales

![Ratios económicos](salidas/figuras/11_ratios_economicos.png)

| Ratio | 2010 | 2011 | Variación |
|---|---|---|---|
| **Ventas per cápita** | £0,1304 | £0,1203 | -7,7% |
| **Ventas por billón PIB** | £3,28M | £2,84M | -13,4% |
| **Clientes por mil hab.** | 0,067 | 0,066 | -1,4% |

**Análisis:**
- Todos los ratios caen en 2011, confirmando el **deterioro relativo** del negocio.
- La tienda factura menos por cada libra de PIB generada.

### 7.6 Estacionalidad y contexto económico

![Estacionalidad y contexto](salidas/figuras/12_estacionalidad_contexto.png)

**Análisis:**
- La **estacionalidad navideña** (pico en Q4) se mantiene en ambos años.
- Pero el **pico de 2011 es más bajo** que el de 2010 (16,9% menos).
- La **inflación y el desempleo crecieron** en paralelo a la caída del Q4.

**Implicación:** el contexto económico adverso (inflación + desempleo) **amplificó la caída** en el trimestre clave.

---

## 8. Paso 6: Conclusiones y recomendaciones

### 8.1 Valor añadido del Open Data

El Open Data ha permitido:

| Sin Open Data | Con Open Data |
|---|---|
| Solo veíamos ventas nominales | Vemos ventas reales (ajustadas por inflación) |
| No sabíamos por qué caía el Q4 2011 | Sabemos que coincidió con inflación + desempleo altos |
| No podíamos comparar con la economía | Sabemos que la tienda va contra el PIB |
| No teníamos ratios de mercado | Tenemos ventas per cápita y penetración de PIB |

### 8.2 Conclusiones clave

1. **La inflación erosiona el 3,71% de las ventas reales** en 2011.
2. **El Q4 2011 cayó un 16,9%**, coincidiendo con el pico de inflación y desempleo.
3. **La tienda no aprovecha el crecimiento económico** del país (PIB +7,2% vs ventas -7%).

### 8.3 Recomendaciones

#### Recomendaciones estratégicas

1. **Revisar la política de precios** para compensar el efecto de la inflación.
2. **Reforzar las campañas del Q4** con antelación, ajustando promociones al contexto económico.
3. **Analizar la competitividad** del negocio (¿por qué no crecemos cuando el país crece?).

#### Recomendaciones operativas

1. **Ajustar el stock** en función del contexto económico: menos stock en períodos de alta inflación.
2. **Segmentar las promociones** por región (los datos del ONS muestran diferencias de población).
3. **Monitorizar indicadores macro** (inflación, desempleo) para anticipar caídas.

---

## 9. Anexos

### Anexo A: Estructura del proyecto

Reto6_OpenData_Retail/
├── datos/
│ ├── principal/ (Online Retail II limpio)
│ ├── open_data/ (Indicadores + población)
│ └── enriquecido/ (Dataset final)
├── scripts/ (6 scripts Python)
├── salidas/
│ ├── figuras/ (12 visualizaciones)
│ └── resultados/ (CSVs de resultados)
└── docs/ (4 entregables)


### Anexo B: Scripts desarrollados

| Script | Función |
|---|---|
| `02_limpieza_principal.py` | Limpieza del dataset principal |
| `03_limpieza_open_data.py` | Limpieza del Open Data |
| `04_integracion.py` | Integración de ambos datasets |
| `05c_analisis_comparativo_final.py` | Análisis comparativo |

### Anexo C: Fuentes de Open Data

| Fuente | URL |
|---|---|
| World Bank Open Data | https://data.worldbank.org |
| ONS Nomis | https://www.nomisweb.co.uk |

### Anexo D: Glosario

| Término | Definición |
|---|---|
| **Open Data** | Datos públicos, gratuitos y abiertos |
| **Left Join** | Unión que preserva todas las filas del dataset principal |
| **Inflación** | Aumento generalizado de precios |
| **PIB** | Producto Interior Bruto |
| **CPI** | Consumer Price Index (índice de precios al consumo) |

---

**FIN DEL INFORME**  
*Documento generado por Judit Giravent — 09/2026*

