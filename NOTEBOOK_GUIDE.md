# Analysis Notebook Guide

## Overview

The project includes a single, comprehensive Jupyter notebook that executes all analysis steps in one place: **analisis_baterias.ipynb**

This notebook replaces the previous two-notebook system and provides a streamlined, production-ready analysis pipeline for your bachelor's thesis submission.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Open the Notebook

```bash
jupyter notebook analisis_baterias.ipynb
```

### 3. Execute All Cells

Run all cells in order (from top to bottom) to complete the full analysis:
- Cell 3: Import all modules
- Cell 5: Organize raw files by date
- Cell 7: Trim cycling files
- Cell 9: Extract SoH values
- Cell 11: Build ZCURVE impedance matrix
- Cell 13: Update battery matrix with impedance
- Cell 15: Select 18 best compatible batteries
- Cell 17: Display detailed battery information
- Cell 19: Export results to CSV

## What the Notebook Does

The notebook executes the complete battery analysis workflow:

1. **File Organization** - Organizes raw cycler files into date-based folder structure (preserves originals)

2. **Data Extraction (Cycling)**
   - Trims cycling files to keep only header and final state
   - Extracts SoH (State of Health) values for each battery
   - Creates matriz_baterias.csv with battery data

3. **Data Extraction (EIS)**
   - Processes Electrochemical Impedance Spectroscopy data from .DTA files
   - Extracts Zreal and Zimag impedance values
   - Creates matriz_zcurve.csv with impedance data

4. **Data Integration**
   - Merges impedance values with battery SoH data
   - Updates matriz_baterias.csv with complete battery information

5. **Battery Selection**
   - Selects 18 batteries with the most compatible (similar) SoH values
   - Uses sliding window algorithm to minimize SoH spread
   - Generates detailed statistics

6. **Results Export**
   - Exports the 18 selected batteries to:
     `data/output/mejores_18_baterias.csv`
   - CSV contains: numero (ID), soh (Ah), impedancia (Ohm)

## Output Files

After running the complete notebook, you will have:

1. **data/processed/matriz_baterias.csv**
   - Full matrix with all 36 batteries
   - Columns: Numero, SoH(Ah), Impedancia(Ω)

2. **data/processed/matriz_zcurve.csv**
   - Detailed impedance data from EIS
   - Zreal and Zimag values for each measurement point

3. **data/output/mejores_18_baterias.csv**
   - The 18 selected batteries for your battery pack
   - Ready for physical assembly and testing

## Key Features

- Single notebook, single execution flow (no switching between files)
- Integrated logging with clear progress indicators
- Error handling and validation
- Statistical summaries for all key results
- Production-ready code with no debugging artifacts
- No emoji characters (clean for thesis submission)
- Comprehensive markdown documentation in Spanish

## Troubleshooting

### ImportError: No module named 'src'

Make sure you're running the notebook from the project root directory:
```bash
cd /home/elias/Documents/TFG/Procesado_Datos/TFG_Elias
jupyter notebook analisis_baterias.ipynb
```

### ModuleNotFoundError

Ensure all dependencies are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Data Not Found

Verify your data directory structure:
```
data/
├── raw/
│   ├── cicladores/     (cycler 1-6 files)
│   └── eis/            (EIS .DTA files)
└── processed/
```

## Next Steps

After running the complete analysis:

1. Review the exported 18 batteries in `data/output/mejores_18_baterias.csv`
2. Verify the SoH and impedance values match your expectations
3. Check the statistics printed in the notebook for quality assurance
4. Prepare the selected batteries for physical assembly
5. Document the selected battery IDs in your thesis

## Legacy Notebooks

The original notebooks are preserved for reference:
- `procesado_ciclados.ipynb` - Previous cycling analysis
- `procesado_eis.ipynb` - Previous EIS analysis

These are no longer needed for analysis, but retained if you want to review the separate processing steps.
