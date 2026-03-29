"""
Configuration file for battery analysis project.

Centralized settings for data paths, processing parameters, and analysis configuration.
Update these paths if your data directory structure changes.
"""

from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"

# Data subdirectories
CYCLING_RAW_DIR = RAW_DATA_DIR / "cicladores"
EIS_RAW_DIR = RAW_DATA_DIR / "eis"
CYCLING_PROCESSED_DIR = PROCESSED_DATA_DIR / "cicladores"
BATTERIES_DIR = PROCESSED_DATA_DIR / "baterias"

# Output CSV files
SOH_MATRIX_CSV = PROCESSED_DATA_DIR / "matriz_baterias.csv"
ZCURVE_MATRIX_CSV = PROCESSED_DATA_DIR / "matriz_zcurve.csv"
BEST_BATTERIES_CSV = OUTPUT_DIR / "mejores_18_baterias.csv"

# ============================================================================
# PROCESSING PARAMETERS
# ============================================================================

# Cycling data - cycler indices (number of cyclers in the raw data)
CYCLER_RANGE = range(1, 7)  # cicladores 1-6

# File encoding for text files
TEXT_FILE_ENCODING = "latin-1"
CSV_FILE_ENCODING = "utf-8"

# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

# SoH threshold for battery health assessment (80% of nominal SoH value)
SOH_HEALTH_THRESHOLD = 0.3460 * 0.8

# Number of best batteries to select for pack formation
BEST_BATTERIES_COUNT = 18

# ============================================================================
# FUNCTIONS FOR VALIDATION
# ============================================================================


def validate_data_directories():
    """Check if all required data directories exist."""
    required_dirs = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        CYCLING_RAW_DIR,
        EIS_RAW_DIR,
    ]
    
    missing = [d for d in required_dirs if not d.exists()]
    if missing:
        print("WARNING: The following directories are missing:")
        for d in missing:
            print(f"   {d}")
        return False
    return True


if __name__ == "__main__":
    print("Configuration file for TFG Battery Analysis")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Data directory: {DATA_DIR}")
    validate_data_directories()
