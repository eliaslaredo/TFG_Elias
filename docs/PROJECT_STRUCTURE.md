# Project Structure

## Overview

This project has been restructured into a modular Python package following professional software engineering practices. All analysis logic has been extracted from Jupyter notebooks into reusable modules organized by functional domain.

## Main Analysis Notebook

**analisis_baterias.ipynb** is the primary entry point for running the complete analysis pipeline. It integrates all steps:
1. File organization by date
2. Cycling data processing and SoH extraction
3. EIS impedance data extraction
4. Battery matrix updates with impedance values
5. Selection of 18 best compatible batteries
6. Statistical analysis and results export

Simply open this notebook and run all cells in order to execute the complete analysis.

## Directory Structure

```
TFG_Elias/
│
├── config.py                    # Centralized configuration & paths
├── requirements.txt             # Python dependencies
│
├── src/                         # Main package (reusable modules)
│   ├── __init__.py
│   │
│   ├── models/                  # Data structures & models
│   │   ├── __init__.py
│   │   └── bateria.py          # Bateria class (battery data model)
│   │
│   ├── data_io/                 # File I/O operations
│   │   ├── __init__.py
│   │   ├── file_organization.py # Organize raw files by date
│   │   └── export.py            # Export analysis results to CSV
│   │
│   ├── processing/              # Data transformation & cleaning
│   │   ├── __init__.py
│   │   ├── cycling.py          # Cycle test file processing
│   │   └── eis.py              # EIS impedance data processing
│   │
│   ├── analysis/                # Data analysis functions
│   │   ├── __init__.py
│   │   └── soh.py              # SoH calculations & battery selection
│   │
│   └── utils/                   # Shared utilities (extensible)
│       └── __init__.py
│
├── docs/                        # Documentation
│   ├── PROJECT_STRUCTURE.md    # This file
│   └── SETUP.md                # Installation & usage guide
│
├── procesado_ciclados.ipynb    # Legacy notebook (kept for reference)
├── procesado_eis.ipynb         # Legacy notebook (kept for reference)
├── analisis_baterias.ipynb     # Main analysis notebook (complete pipeline)
│
├── data/                        # Data directories (unchanged)
│   ├── raw/
│   │   ├── cicladores/         # Raw cycling test data
│   │   └── eis/                # Raw EIS measurement files
│   ├── processed/
│   │   ├── baterias/           # Processed battery data
│   │   ├── cicladores/         # Processed cycling files
│   │   ├── matriz_baterias.csv # Battery SoH matrix (output)
│   │   └── matriz_zcurve.csv   # Impedance matrix (output)
│   └── output/
│       └── mejores_18_baterias.csv # Best 18 batteries export (output)
│
└── README.md                    # Project overview
```

## Module Reference

### `src/models/bateria.py`
**Purpose**: Data model representing a battery with health and impedance data.

**Main Class**:
- `Bateria(numero, soh, impedancia)` - Represents a lithium battery cell
  - Properties: numero (ID), soh (capacity in Ah), impedancia (resistance in Ω)
  - Methods:
    - `esta_en_buen_estado()` → bool - Check if battery is healthy
    - `resumen()` → str - Get formatted status string
    - `to_dict()` → dict - Convert to dictionary

**Example**:
```python
from src.models import Bateria

bat = Bateria(numero=1, soh=2.5, impedancia=0.15)
print(bat)  # Bateria(numero=1, soh=2.5Ah, impedancia=0.15Ω)
print(bat.esta_en_buen_estado())  # True or False
```

---

### `src/data_io/file_organization.py`
**Purpose**: Organize raw cycler files by extraction date from filename patterns.

**Main Functions**:
- `organizar_archivos_por_fecha(carpeta_origen, cycler_id)` → dict
  - Parses AAAA_MM_DD dates from filenames
  - Creates organized date-based folder structure
  - Copies (preserves) original raw files
  - Returns statistics: organized count, skipped, errors

- `organizar_todos_los_cicladores()` → dict
  - Convenience function to process all 6 cyclers
  - Prints summary statistics

**Example**:
```python
from src.data_io import organizar_archivos_por_fecha

result = organizar_archivos_por_fecha("data/raw/cicladores/ciclador_1", cycler_id=1)
print(f"Organized: {result['organized']} files")
```

---

### `src/data_io/export.py`
**Purpose**: Export analysis results and battery data to CSV files.

**Main Functions**:
- `export_batteries_to_csv(baterias, filepath, filename)` → Path
  - Exports a list of batteries to CSV
  - Includes columns: numero, soh, impedancia
  - Sorts by battery number for readability
  - Returns Path to created CSV file

- `export_best_18_batteries(baterias)` → Path
  - Exports 18 selected batteries to data/output/mejores_18_baterias.csv
  - Includes SoH and impedance values for each battery
  - Validates that exactly 18 batteries are provided
  - Returns Path to created CSV file

**Example**:
```python
from src.data_io import export_best_18_batteries
from src.analysis import find_best_18

best_batteries = find_best_18(all_batteries)
output_path = export_best_18_batteries(best_batteries)
print(f"Exported to: {output_path}")
```

---

### `src/processing/cycling.py`
**Purpose**: Process and analyze cycling test data.

**Main Functions**:
- `trim_txt_files(processed_dir)` → dict
  - Keeps only header and last data row per file
  - Deletes associated .dat files
  - Returns: processed count, skipped, deleted, errors

- `build_soh_matrix(baterias_dir, output_csv)` → List[Bateria]
  - Extracts SoH (State of Health) values from trimmed files
  - Creates Bateria objects
  - Saves CSV matrix: matriz_baterias.csv
  - Returns list of Bateria objects (may contain None)

**Example**:
```python
from src.processing import trim_txt_files, build_soh_matrix

# Clean up files
results = trim_txt_files()
print(f"Processed {len(results['processed'])} files")

# Build SoH matrix
baterias = build_soh_matrix()
print(f"Loaded {len(baterias)} batteries")
```

---

### `src/processing/eis.py`
**Purpose**: Process Electrochemical Impedance Spectroscopy (EIS) data.

**Main Functions**:
- `build_zcurve_matrix(eis_dir, output_csv)` → pd.DataFrame
  - Extracts ZCURVE data from .DTA files
  - Parses Zreal and Zimag impedance values
  - Saves CSV matrix: matriz_zcurve.csv
  - Returns DataFrame with impedance data

- `actualizar_impedancia(archivo_zcurve, archivo_baterias, output_csv)` → pd.DataFrame
  - Finds impedance at zero-crossing point (Zimag ≈ 0)
  - Updates battery matrix with impedance values
  - Returns updated battery DataFrame

**Example**:
```python
from src.processing.eis import build_zcurve_matrix, actualizar_impedancia

# Build impedance matrix
df_zcurve = build_zcurve_matrix()

# Update battery SoH matrix with impedance
df_batteries = actualizar_impedancia()
print(df_batteries[['Numero', 'SoH(Ah)', 'Impedancia']].head())
```

---

### `src/analysis/soh.py`
**Purpose**: Battery selection and health analysis functions.

**Main Functions**:
- `find_best_18(baterias)` → List[Bateria]
  - Selects 18 most compatible batteries for pack formation
  - Uses sliding window algorithm on SoH-sorted values
  - Minimizes spread (max - min SoH difference)
  - Returns selected batteries sorted by number

- `evaluate_battery_health(baterias)` → dict
  - Calculates SoH statistics
  - Returns: mean, std, min, max, range, healthy/degraded counts

**Example**:
```python
from src.analysis import find_best_18, evaluate_battery_health

best_batteries = find_best_18(all_batteries)
stats = evaluate_battery_health(best_batteries)
print(f"Mean SoH: {stats['mean_soh']:.3f} Ah")
print(f"Selected batteries: {[b.numero for b in best_batteries]}")
```

---

## Data Flow

```
Raw Data (data/raw/)
    ↓
┌───────────────────────────────────┐
│ Step 1: File Organization         │
│ organizar_archivos_por_fecha()    │
└───────────────────────────────────┘
    ↓ data/processed/cicladores/{cycler}/{date}/
┌───────────────────────────────────┐
│ Step 2: Trim Cycling Files        │
│ trim_txt_files()                  │
└───────────────────────────────────┘
    ↓ Keep only header + last row
┌───────────────────────────────────┐
│ Step 3: Extract SoH Values        │
│ build_soh_matrix()                │
└───────────────────────────────────┘
    ↓ matriz_baterias.csv
┌───────────────────────────────────┐
│ Step 4: Extract Impedance (EIS)   │
│ build_zcurve_matrix()             │
└───────────────────────────────────┘
    ↓ matriz_zcurve.csv
┌───────────────────────────────────┐
│ Step 5: Update Impedance Values   │
│ actualizar_impedancia()           │
└───────────────────────────────────┘
    ↓ Final: matriz_baterias.csv (with impedance)
┌───────────────────────────────────┐
│ Step 6: Select Best Pack          │
│ find_best_18()                    │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│ Step 7: Export Best Batteries     │
│ export_best_18_batteries()        │
└───────────────────────────────────┘
    ↓
Final Output (data/output/mejores_18_baterias.csv)
18 compatible battery pack with SoH and impedance values
```

---

## Configuration

All paths and parameters are centralized in `config.py`:

```python
# Data paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = DATA_DIR / "output"
BATTERIES_DIR = DATA_DIR / "processed/baterias"
EIS_RAW_DIR = DATA_DIR / "raw/eis"
SOH_MATRIX_CSV = DATA_DIR / "processed/matriz_baterias.csv"
ZCURVE_MATRIX_CSV = DATA_DIR / "processed/matriz_zcurve.csv"
BEST_BATTERIES_CSV = OUTPUT_DIR / "mejores_18_baterias.csv"

# Processing parameters
CYCLER_RANGE = range(1, 7)  # Cyclers 1-6
TEXT_FILE_ENCODING = "latin-1"
CSV_FILE_ENCODING = "utf-8"

# Analysis parameters
SOH_HEALTH_THRESHOLD = 0.3460 * 0.8  # 80% of nominal
BEST_BATTERIES_COUNT = 18
```

Update `config.py` if your directory structure changes.

---

## 🔌 Using in Notebooks

**Before (old way)**:
```python
# Functions embedded in notebook
def trim_txt_files():
    ...

# Call directly
trim_txt_files()
```

**After (new way)**:
```python
# Import from module
from src.processing.cycling import trim_txt_files

# Call via import
results = trim_txt_files()
```

Benefits:
- OK Cleaner notebooks (focus on analysis, not implementation)
- OK Reusable functions (can be used from scripts, other notebooks, tests)
- OK Better maintenance (change logic once, affects everywhere)
- OK Professional structure (looks like production code)

---

## Extending the Project

To add new functions:

1. **Choose the appropriate module** based on functionality
2. **Create or edit the file** in the relevant src/ subfolder
3. **Add import** to that module's `__init__.py`
4. **Import in notebooks** as needed
5. **Document with docstrings** (Google style)

Example - adding a new analysis function:

```python
# File: src/analysis/degradation.py
"""Degradation trend analysis."""

def analyze_degradation_trend(baterias_history):
    """Analyze how SoH degrades over time."""
    # implementation
    pass

# File: src/analysis/__init__.py
from src.analysis.degradation import analyze_degradation_trend
__all__ = ["find_best_18", "evaluate_battery_health", "analyze_degradation_trend"]
```

---

## References

- **Main Notebook**: [procesado_ciclados.ipynb](../procesado_ciclados.ipynb) - Cycling analysis
- **EIS Notebook**: [procesado_eis.ipynb](../procesado_eis.ipynb) - Impedance analysis
- **Configuration**: [config.py](../config.py) - Centralized settings
- **Setup Guide**: [SETUP.md](./SETUP.md) - Installation instructions
