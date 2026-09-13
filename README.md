# 🌍 Reto 6 — Dataset enriquecido con Open Data

Proyecto de **Business Intelligence** que enriquece un dataset comercial de ventas (Online Retail II) con **Open Data** del World Bank y del ONS (Office for National Statistics), realizando un análisis comparativo que revela insights imposibles de obtener con datos internos.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-3.0.5-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completado-success.svg)]()

---

## 📌 Descripción

Este proyecto demuestra cómo el **Open Data** puede transformar el análisis de negocio al aportar contexto económico y demográfico externo. Combinando ventas internas con indicadores macroeconómicos del Reino Unido, se descubren insights sobre el impacto de la inflación, el desempleo y el crecimiento económico.

---

## 🎯 Objetivo

Enriquecer un dataset comercial con datos abiertos y realizar un **análisis comparativo** que revele nuevas perspectivas sobre el negocio.

---

## 📊 Datasets utilizados

### Dataset principal
- **Fuente:** Online Retail II (UCI Machine Learning Repository)
- **Transacciones:** 767.853 (tras limpieza)
- **Periodo:** Diciembre 2009 – Diciembre 2011
- **País:** Reino Unido

### Open Data
- **World Bank Open Data:** PIB, inflación, desempleo, población
- **ONS Nomis:** Población por región UK

---

## 🔍 Hallazgos principales

| # | Hallazgo | Cifra |
|---|---|---|
| 1 | Impacto de la inflación en las ventas reales | **-£282.555** |
| 2 | Caída del Q4 2011 vs Q4 2010 | **-16,9%** |
| 3 | Divergencia con la economía UK | **+7,2% PIB vs -7% ventas** |

### Interpretación

- **La inflación erosiona el 3,71% de las ventas** en 2011.
- **La campaña navideña (Q4) cayó un 16,9%**, coincidiendo con el pico de inflación (3,86%) y desempleo (8,2%).
- **La tienda no aprovecha el crecimiento económico**: mientras el PIB UK crecía, las ventas caían.

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|---|---|
| **Python 3.13** | Lenguaje principal |
| **pandas** | Manipulación de datos |
| **matplotlib / seaborn** | Visualizaciones |
| **World Bank API** | Open Data económico |
| **ONS Nomis** | Open Data demográfico |

---

## 📁 Estructura del proyecto

```
Reto6_OpenData_Retail/
│
├── datos/
│   ├── principal/                    # Online Retail II limpio
│   ├── open_data/                    # Indicadores + población
│   │   └── raw/                      # Datos originales descargados
│   └── enriquecido/                  # Dataset final enriquecido
│
├── scripts/                          # Scripts Python
│   ├── 02_limpieza_principal.py
│   ├── 03_limpieza_open_data.py
│   ├── 04_integracion.py
│   └── 05c_analisis_comparativo_final.py
│
├── salidas/
│   ├── figuras/                      # 12 visualizaciones PNG
│   └── resultados/                   # CSVs de resultados
│
├── docs/                             # Entregables del reto
│   ├── Informe_Analisis_Reto6_JuditGiravent.pdf
│   ├── Visualizaciones_Reto6_JuditGiravent.pdf
│   ├── Conclusiones_Recomendaciones_Reto6_JuditGiravent.pdf
│   └── Presentacion_Reto6_JuditGiravent.pptx
│
├── .gitignore
├── LICENSE
└── README.md
```




## 🚀 Cómo reproducir

### 1. Clonar el repositorio

```bash
git clone https://github.com/jdthgp27/Reto6_OpenData_Retail.git
cd Reto6_OpenData_Retail
2. Instalar dependencias
bash
pip install pandas numpy matplotlib seaborn openpyxl
3. Descargar los datasets
Dataset principal: descargar desde UCI y colocar en datos/principal/.

Open Data: descargar los indicadores del World Bank y la población de ONS Nomis en datos/open_data/raw/.

4. Ejecutar los scripts en orden
bash
cd scripts
python 02_limpieza_principal.py
python 03_limpieza_open_data.py
python 04_integracion.py
python 05c_analisis_comparativo_final.py
📸 Visualizaciones destacadas
Ventas nominales vs ajustadas por inflación
[Ventas ajustadas](salidas/figuras/09_ventas_nominales_vs_ajustadas.png)


Comparativa trimestral 2010 vs 2011
[Ventas ajustadas](salidas/figuras/10_comparativa_trimestral_2010_2011.png)

Ratios económicos anuales
[Ventas ajustadas](salidas/figuras/11_ratios_economicos.png)

💡 Conclusiones
El Open Data ha permitido:

Sin Open Data	Con Open Data
Solo veíamos ventas nominales	Vemos ventas reales ajustadas
No sabíamos por qué caía el Q4	Coincide con inflación + desempleo
No podíamos comparar con la economía	Sabemos que vamos contra el PIB
Sin ratios de mercado	Ventas per cápita y por PIB
Recomendaciones
Revisar la política de precios para compensar la inflación.

Reforzar las campañas del Q4 con antelación.

Analizar la competitividad del negocio.

Monitorizar indicadores macro para anticipar caídas.

📄 Documentación
Informe de análisis

Visualizaciones comparativas

Conclusiones y recomendaciones

Presentación ejecutiva

👤 Autora
Judit Giravent

LinkedIn: judit-giravent-27b167156

GitHub: @jdthgp27

📜 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
