# TFG: Reciclado de Baterías de Litio de Vapeadores Desechables

**Autor**: Elias Laredo Fernández  
**Programa**: Ingeniería de Sonido e Imagen  
**Universidad**: UC3M - 2025/2026  
**Licencia**: GNU General Public License v3.0

---

## Descripcion del Proyecto

Este proyecto analiza datos experimentales de 36 baterías de litio 13300 extraídas de vapeadores desechables. Se realizaron dos ensayos principales:

### Ensayos Realizados

1. **Ciclado (Cycling Tests)**
   - Objetivo: Obtener el Estado de Salud (SoH) de cada batería
   - Proceso: Ciclo completo de carga → descarga → carga
   - Resultado: Matriz de SoH [Ah] para todas las baterías

2. **Espectroscopia de Impedancia Electroquímica (EIS)**
   - Objetivo: Medir la impedancia interna detallada
   - Proceso: Escaneo de frecuencia (ZCURVE)
   - Resultado: Matriz de impedancia [Ω] a varios puntos de operación

### Objetivo Final

Seleccionar **18 baterías compatibles** (con SoH similar) para formar un pack homogéneo destinado a reciclado/reutilización.

---

## Estructura del Proyecto

```
TFG_Elias/
├── src/                         # Código modular reutilizable
│   ├── models/                  # Estructuras de datos
│   ├── data_io/                 # Lectura/escritura de archivos
│   ├── processing/              # Procesamiento de datos
│   └── analysis/                # Análisis (SoH, selección)
│
├── docs/                        # Documentación completa
│   ├── PROJECT_STRUCTURE.md     # Referencia de módulos
│   └── SETUP.md                 # Guía de instalación
│
├── config.py                    # Configuración centralizada
├── requirements.txt             # Dependencias Python
│
├── procesado_ciclados.ipynb    # Análisis de ciclado (importa src.*)
├── procesado_eis.ipynb         # Análisis de impedancia (importa src.*)
│
└── data/                        # Datos (sin cambios)
    ├── raw/                     # Datos originales
    │   ├── cicladores/          # Archivos de cicladores (1-6)
    │   └── eis/                 # Archivos .DTA (EIS)
    ├── processed/               # Datos procesados
    │   ├── cicladores/          # Archivos organizados por fecha
    │   ├── baterias/            # Datos por batería
    │   ├── matriz_baterias.csv  # Salida: SoH + Impedancia
    │   └── matriz_zcurve.csv    # Salida: Datos ZCURVE
    └── output/                  # Resultados finales
        └── mejores_18_baterias.csv  # Salida: 18 baterías seleccionadas
```

---

## Quick Start

### 1. Instalación

```bash
pip install -r requirements.txt
```

### 2. Ejecutar Análisis

```bash
jupyter notebook
```

Abrir y ejecutar: `analisis_baterias.ipynb`

Este cuaderno integrado ejecuta todos los pasos del análisis en orden:
1. Organizacion de archivos por fecha
2. Extraccion de SoH
3. Extraccion de impedancia (EIS)
4. Seleccion de 18 baterias compatibles
5. Exportacion de resultados

### 3. Resultados

- `data/processed/matriz_baterias.csv` - Tabla final con SoH e impedancia
- `data/processed/matriz_zcurve.csv` - Datos detallados de impedancia
- `data/output/mejores_18_baterias.csv` - Las 18 baterías seleccionadas con SoH e impedancia

---

## Documentación

Para información completa, ver:

- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - Referencia de módulos y API
- **[docs/SETUP.md](docs/SETUP.md)** - Guía de instalación y configuración
- **[config.py](config.py)** - Parámetros y rutas configurables

---

## Arquitectura Modular

El código ha sido restructurado en una arquitectura profesional:

```
Datos Raw (data/raw/)
    ↓
Organización por Fecha (data_io)
    ↓
Procesamiento (processing: trim, extract)
    ↓
Análisis (analysis: SoH, selection)
    ↓
Notebooks (Visualización & Resultados)
```

**Beneficios**:
- OK Código reutilizable y modular
- OK Notebooks limpios (importan funciones)
- OK Fácil de mantener y extender
- OK Profesional para presentación en tesis

---

## Modulos Principales

| Módulo | Función | Entrada | Salida |
|--------|---------|---------|--------|
| `data_io` | Organizar archivos brutos | raw/ | processed/cicladores |
| `data_io.export` | Exportar resultados a CSV | Bateria[] | output/mejores_18_baterias.csv |
| `processing.cycling` | Procesar & extraer SoH | processed/cicladores | Bateria[] + CSV |
| `processing.eis` | Extraer impedancia EIS | raw/eis | ZCURVE matrix + CSV |
| `analysis.soh` | Seleccionar pack óptimo | Bateria[] | 18 baterías compatibles |

Ver [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) para API completa.

---

## Datos de Ejemplo

**Entrada**: 36 baterías 13300 Li-ion de vapeadores  
**Salida**: Tabla con SoH (Ah) e Impedancia (Ω)

```
Numero | SoH(Ah) | Impedancia(Ω)
-------|---------|----------------
   1   |  2.50   |    0.145
   2   |  2.48   |    0.148
  ...  |  ...    |     ...
   18  |  2.43   |    0.142
```

Las 18 baterías seleccionadas tienen SoH similar → mejor compatibilidad en el pack.

---

## Configuracion

Todos los parámetros se centralizan en `config.py`:

```python
# Rutas
DATA_DIR = Path(__file__).parent / "data"
BATTERIES_DIR = DATA_DIR / "processed/baterias"

# Parámetros
SOH_HEALTH_THRESHOLD = 0.3460 * 0.8  # 80% nominal
BEST_BATTERIES_COUNT = 18
```

Editar si la estructura de carpetas cambia.

---

## Estructura de Carpetas de Datos

```
data/
├── raw/
│   ├── cicladores/
│   │   ├── ciclador_1/          (archivos brutos del ciclador 1)
│   │   ├── ciclador_2/
│   │   └── ... (1-6)
│   └── eis/
│       ├── EIS_B1.DTA
│       ├── EIS_B2.DTA
│       └── ... (1-36)
│
└── processed/
    ├── cicladores/
    │   └── {1-6}/{YYYY_MM_DD}/    (organizados por fecha)
    ├── baterias/
    │   └── {1-36}/                (una carpeta por batería)
    ├── matriz_baterias.csv        ← Datos finales
    └── matriz_zcurve.csv          ← Datos EIS
```

