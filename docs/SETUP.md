# Setup & Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended: `venv` or `conda`)

## Installation Steps

### 1. Activate Virtual Environment (if using one)

If you already have a `.venv` directory:
```bash
source .venv/bin/activate
```

Or create a new one:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# OR on Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `matplotlib` - Plotting (optional, for visualization)
- `jupyter` - Jupyter notebooks
- `ipython` - Enhanced Python shell

### 3. Verify Installation

Test that imports work:
```bash
python -c "from src.models import Bateria; from src.processing.cycling import trim_txt_files; print('OK: All imports successful!')"
```

---

## Usage

### Running Jupyter Notebooks

```bash
jupyter notebook
```

Then open: **analisis_baterias.ipynb**

This is the main analysis notebook that integrates all steps in sequence:
1. **Organizar archivos** - Organize raw cycler files by date
2. **Procesar ciclado** - Trim cycling files and extract SoH
3. **Construir matriz ZCURVE** - Extract impedance data from EIS files
4. **Actualizar impedancia** - Update battery matrix with impedance values
5. **Seleccionar 18 baterias** - Find best compatible batteries
6. **Exportar resultados** - Save results to CSV

Simply run all cells in order to complete the full analysis pipeline.

---

## Quick API Reference

### Import Modules

```python
# Models
from src.models import Bateria

# Data I/O
from src.data_io import organizar_archivos_por_fecha

# Processing
from src.processing.cycling import trim_txt_files, build_soh_matrix
from src.processing.eis import build_zcurve_matrix, actualizar_impedancia

# Analysis
from src.analysis import find_best_18, evaluate_battery_health
```

### Create Battery Object

```python
from src.models import Bateria

bat = Bateria(numero=1, soh=2.5, impedancia=0.15)
print(bat)
print(bat.esta_en_buen_estado())  # Health check
```

### Process Cycling Data

```python
from src.processing.cycling import trim_txt_files, build_soh_matrix

# Clean up files
results = trim_txt_files()

# Build SoH matrix
baterias = build_soh_matrix()
```

### Process EIS Data

```python
from src.processing.eis import build_zcurve_matrix, actualizar_impedancia

# Extract impedance
df_zcurve = build_zcurve_matrix()

# Update battery matrix
df_baterias = actualizar_impedancia()
```

### Select Best Batteries

```python
from src.analysis import find_best_18, evaluate_battery_health

best_18 = find_best_18(all_baterias)

stats = evaluate_battery_health(best_18)
print(f"Mean SoH: {stats['mean_soh']:.3f} Ah")
print(f"Range: {stats['min_soh']:.3f} - {stats['max_soh']:.3f} Ah")
```

### Export Results

```python
from src.data_io import export_best_18_batteries

# Export the 18 selected batteries to CSV
output_path = export_best_18_batteries(best_18)
print(f"Exported to: {output_path}")

# The CSV file will contain: numero, soh, impedancia
# File location: data/output/mejores_18_baterias.csv
```

---

## Configuration

All paths and parameters are in `config.py`. Key settings:

```python
# Data directories
DATA_DIR = PROJECT_ROOT / "data"
BATTERIES_DIR = DATA_DIR / "processed/baterias"
EIS_RAW_DIR = DATA_DIR / "raw/eis"

# Processing
CYCLER_RANGE = range(1, 7)  # Cyclers 1-6
TEXT_FILE_ENCODING = "latin-1"

# Analysis
SOH_HEALTH_THRESHOLD = 0.3460 * 0.8
BEST_BATTERIES_COUNT = 18
```

If you move your data folders, update the paths in `config.py`.

---

## File Structure Explanation

```
data/
├── raw/                          # Original, unmodified data
│   ├── cicladores/
│   │   ├── ciclador_1/          # Raw files from cycler 1
│   │   ├── ciclador_2/
│   │   ├── ... (cyclers 1-6)
│   │   └── Full Test 1C Elias/
│   └── eis/                      # EIS measurement files
│       ├── EIS_B1.DTA
│       ├── EIS_B2.DTA
│       └── ... (all 36 batteries)
│
├── processed/                    # Cleaned, transformed data
│   ├── cicladores/
│   │   ├── 1/
│   │   │   ├── 2026_02_23/      # Organized by date
│   │   │   └── ...
│   │   ├── 2/, 3/, ... (cyclers 1-6)
│   │   
│   ├── baterias/                # Processed battery files
│   │   ├── 1/
│   │   │   └── STP11_Charge_1C_Elias_2026_02_23_17_12_50.txt
│   │   ├── 2/
│   │   └── ... (one .txt per battery)
│   │
│   ├── matriz_baterias.csv      # SoH matrix (output)
│   │   # Columns: Numero, SoH(Ah), Impedancia
│   │   
│   └── matriz_zcurve.csv         # Impedance matrix (output)
│       # Columns: Bateria_Num, Zreal, Zimag, ...
│
└── output/                       # Final analysis results
    └── mejores_18_baterias.csv   # Best 18 batteries (output)
        # Columns: numero, soh, impedancia
```

---

## Troubleshooting

### ImportError: No module named 'src'

**Problem**: Projects run from wrong directory.

**Solution**:
```bash
cd /path/to/TFG_Elias
jupyter notebook
# or
python -m jupyter notebook
```

### ModuleNotFoundError: No module named 'pandas'

**Problem**: Dependencies not installed.

**Solution**:
```bash
pip install -r requirements.txt
```

### "Cannot find data files" errors

**Problem**: Data paths in `config.py` don't match your structure.

**Solution**:
1. Edit `config.py`
2. Update `PROJECT_ROOT` and data paths
3. Run `validate_data_directories()` from config:
   ```python
   from config import validate_data_directories
   validate_data_directories()
   ```

### Encoding errors when reading files

**Problem**: File encoding mismatch (e.g., `latin-1` vs `utf-8`).

**Solution**: Update in `config.py`:
```python
TEXT_FILE_ENCODING = "utf-8"  # or whatever your files use
```

---

## Next Steps

1. OK Verify installation: Run `python -c "from src.models import Bateria; print('OK')"`
2. OK Check data structure: Ensure `data/raw/` and `data/processed/` exist
3. OK Run cyclings notebook: `procesado_ciclados.ipynb`
4. OK Run EIS notebook: `procesado_eis.ipynb`
5. OK Verify outputs: Check `data/processed/matriz_baterias.csv`

---

## Documentation

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed module reference and architecture overview.

---

## Support

For issues or questions, check:
- Module docstrings: `help(function_name)` in Python
- Notebook markdown cells: Explain methodology and expected outputs
- Config file: All paths and parameters
- Project structure docs: Architecture and module purposes
