"""
Export functionality for battery data and analysis results.

Provides functions to export battery information and analysis results to CSV files.
"""

from pathlib import Path
from typing import List, Optional

import pandas as pd

from config import BEST_BATTERIES_CSV, CSV_FILE_ENCODING, OUTPUT_DIR
from src.models.bateria import Bateria


def export_batteries_to_csv(
    baterias: List[Bateria],
    filepath: Optional[Path] = None,
    filename: str = "baterias.csv"
) -> Path:
    """
    Export a list of batteries to a CSV file.
    
    Creates a CSV file with battery information (numero, soh, impedancia) from
    a list of Bateria objects. Useful for saving analysis results and selected
    battery sets.

    Parameters
    ----------
    baterias : List[Bateria]
        List of Bateria objects to export
    filepath : Path, optional
        Directory where the CSV will be saved. Defaults to OUTPUT_DIR.
    filename : str, optional
        Name of the output CSV file. Defaults to "baterias.csv"

    Returns
    -------
    Path
        Path to the created CSV file

    Examples
    --------
    >>> from src.models.bateria import Bateria
    >>> baterias = [Bateria(1, 2.5, 0.15), Bateria(2, 2.48, 0.16)]
    >>> filepath = export_batteries_to_csv(baterias, filename="selected.csv")
    >>> print(f"Exported to: {filepath}")
    """
    if filepath is None:
        filepath = OUTPUT_DIR
    
    # Ensure directory exists
    filepath.mkdir(parents=True, exist_ok=True)
    
    # Convert batteries to list of dictionaries
    data = [bat.to_dict() for bat in baterias]
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by battery number for readability
    df = df.sort_values("numero").reset_index(drop=True)
    
    # Save to CSV
    output_file = filepath / filename
    df.to_csv(output_file, index=False, encoding=CSV_FILE_ENCODING)
    
    return output_file


def export_best_18_batteries(baterias: List[Bateria]) -> Path:
    """
    Export the 18 best batteries to a dedicated CSV file.
    
    Takes a list of 18 selected batteries and exports them to the best batteries
    CSV file in the output directory with SoH and impedance values.

    Parameters
    ----------
    baterias : List[Bateria]
        List of 18 best Bateria objects to export

    Returns
    -------
    Path
        Path to the created CSV file (data/output/mejores_18_baterias.csv)
    
    Raises
    ------
    ValueError
        If the list does not contain exactly 18 batteries
    """
    if len(baterias) != 18:
        raise ValueError(f"Expected 18 batteries, got {len(baterias)}")
    
    # Use the centralized best batteries CSV path from config
    return export_batteries_to_csv(
        baterias,
        filepath=OUTPUT_DIR,
        filename="mejores_18_baterias.csv"
    )
