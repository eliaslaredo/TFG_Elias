"""
Processing functions for cycling test data.

Handles trimming cycling files and building SoH (State of Health) matrices from battery test data.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional

from src.models.bateria import Bateria
from config import CYCLING_PROCESSED_DIR, BATTERIES_DIR, TEXT_FILE_ENCODING, SOH_MATRIX_CSV
from src.processing.eis import get_r0_impedance


def trim_txt_files(processed_dir: Optional[str] = None) -> dict:
    """
    Trim cycling data files to keep only header and last data row.
    
    For every .txt file under data/processed/cicladores/{1-6}/{dates}/:
      - Overwrites each file keeping only the header (line 1) and the last data row.
    For every .dat file in the same folders:
      - Deletes the file entirely.

    Parameters
    ----------
    processed_dir : str, optional
        Path to the 'processed' folder. If None, uses default from config.
        Defaults to "data/processed/cicladores".

    Returns
    -------
    dict
        Results dictionary with keys:
        - "processed": list of .txt files successfully trimmed
        - "skipped": list of .txt files skipped (< 2 lines or already trimmed)
        - "deleted": list of .dat files deleted
        - "errors": list of (filepath, error_message) tuples
    
    Examples
    --------
    >>> results = trim_txt_files()
    >>> print(f"Processed: {len(results['processed'])} files")
    OK Trimmed : 18 .txt files
    SKIP Skipped : 0 .txt files (already 2 lines or empty)
    DELETE Deleted : 0 .dat files
    ERROR Errors  : 0 files
    """
    if processed_dir is None:
        processed_dir = str(CYCLING_PROCESSED_DIR)
    
    base = Path(processed_dir)
    results = {"processed": [], "skipped": [], "deleted": [], "errors": []}

    def is_valid_folder(p: Path) -> bool:
        """Check if path is under a valid cycler folder (1-6)."""
        try:
            cycler_num = int(p.parts[-3])
            return 1 <= cycler_num <= 6
        except (ValueError, IndexError):
            return False

    # --- Process .txt files ---
    for filepath in sorted(base.glob("*/*/*.txt")):
        if not is_valid_folder(filepath):
            continue
        try:
            lines = filepath.read_text(encoding=TEXT_FILE_ENCODING).splitlines()

            if len(lines) < 2 or len(lines) == 2:
                results["skipped"].append(str(filepath))
                continue

            header = lines[0]
            last_row = lines[-1]

            filepath.write_text(header + "\n" + last_row + "\n", encoding=TEXT_FILE_ENCODING)
            results["processed"].append(str(filepath))

        except Exception as e:
            results["errors"].append((str(filepath), str(e)))

    # --- Delete .dat files ---
    for filepath in sorted(base.glob("*/*/*.dat")):
        if not is_valid_folder(filepath):
            continue
        try:
            filepath.unlink()
            results["deleted"].append(str(filepath))
        except Exception as e:
            results["errors"].append((str(filepath), str(e)))

    # Summary
    print(f"OK Trimmed : {len(results['processed'])} .txt files")
    print(f"SKIP Skipped : {len(results['skipped'])} .txt files (already 2 lines or empty)")
    print(f"DELETE Deleted : {len(results['deleted'])} .dat files")
    print(f"ERROR Errors  : {len(results['errors'])} files")
    if results["errors"]:
        for fp, err in results["errors"]:
            print(f"   {fp}: {err}")


def load_batteries_from_csv(csv_path: Optional[str] = None) -> List[Bateria]:
    """
    Load Bateria objects from the battery matrix CSV file.
    
    Reads the CSV file and converts each row to a Bateria object with all attributes
    (numero, soh, impedancia).

    Parameters
    ----------
    csv_path : str, optional
        Path to the battery matrix CSV. If None, uses default from config.
        Expected columns: Numero, SoH(Ah), Impedancia

    Returns
    -------
    List[Bateria]
        List of Bateria objects sorted by battery number, with impedance values.
    
    """
    if csv_path is None:
        csv_path = str(SOH_MATRIX_CSV)
    
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        
        baterias = []
        for _, row in df.iterrows():
            numero = int(row['Numero'])
            soh = float(row['SoH(Ah)'])
            impedancia = float(row['Impedancia']) if 'Impedancia' in row and pd.notna(row['Impedancia']) else 0.0
            
            bat = Bateria(numero=numero, soh=soh, impedancia=impedancia)
            baterias.append(bat)
        
        # Sort by battery number
        baterias = sorted(baterias, key=lambda b: b.numero)
        
        return baterias
    
    except Exception as e:
        print(f"ERROR loading batteries from CSV: {e}")
        return []


def build_soh_matrix(baterias_dir: Optional[str] = None, output_csv: Optional[str] = None) -> List[Optional[Bateria]]:
    """
    Build a matrix of battery SoH values from processed cycling files.
    
    Iterates over all battery folders in data/processed/baterias/ and extracts
    the SOH PS (Ah) value from the single data row of each .txt file.

    Expected file structure:
        baterias/{battery_number}/{file}.txt
    
    Each .txt file should have exactly 2 lines: header row and one data row (post-trimmed).

    Parameters
    ----------
    baterias_dir : str, optional
        Path to the 'baterias' folder. If None, uses default from config.
    output_csv : str, optional
        Path to save the output CSV. If None, uses default from config.

    Returns
    -------
    List[Optional[Bateria]]
        List of Bateria objects indexed by battery number (1-36).
        None entries indicate missing or invalid files for that battery.
    
    Examples
    --------
    >>> baterias = build_soh_matrix()
    >>> print(f"Loaded {len(baterias)} batteries")
    >>> print(baterias[0])
    Bateria(numero=1, soh=2.5Ah, impedancia=0Ω)
    """
    if baterias_dir is None:
        baterias_dir = str(BATTERIES_DIR)
    if output_csv is None:
        output_csv = str(SOH_MATRIX_CSV)
    
    base = Path(baterias_dir)
    battery_folders = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: int(p.name))

    if not battery_folders:
        print(f"ERROR: No folders found under '{base}'. Check the path.")
        return []

    baterias = []

    for folder in battery_folders:
        numero = int(folder.name)
        txt_files = list(folder.glob("*.txt"))

        if not txt_files:
            print(f"WARNING: No .txt file found in '{folder.name}' — inserting None.")
            baterias.append(None)
            continue

        if len(txt_files) > 1:
            print(f"WARNING: Multiple .txt files in '{folder.name}' — using first: {txt_files[0].name}")

        try:
            lines = txt_files[0].read_text(encoding=TEXT_FILE_ENCODING).splitlines()
            header_cols = [col.strip() for col in lines[0].split(",")]
            soh_value = float(lines[1].split(",")[header_cols.index("SOH PS (Ah)")])
            
            # Extract R0 impedance for this battery
            impedancia = get_r0_impedance(numero)
            
            baterias.append(Bateria(numero=numero, soh=soh_value, impedancia=impedancia))

        except Exception as e:
            print(f"ERROR with '{folder.name}': {e} — inserting None.")
            baterias.append(None)

    # --- Save matrix to CSV ---
    try:
        Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            # Write header
            writer.writerow(["Numero", "SoH(Ah)", "Impedancia(Ohm)"])
            
            # Write data
            for bat in baterias:
                if bat is None:
                    writer.writerow(["", "", ""])
                else:
                    writer.writerow([bat.numero, bat.soh, bat.impedancia])
                    
        print(f"\nOK: SoH matrix saved to: '{output_csv}'")
    except Exception as e:
        print(f"\nERROR saving CSV: {e}")

    return baterias
