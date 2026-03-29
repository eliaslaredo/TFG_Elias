"""
Processing functions for Electrochemical Impedance Spectroscopy (EIS) data.

Handles extraction of impedance data from EIS files and creation of impedance matrices.
"""

import csv
import re
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

from config import EIS_RAW_DIR, ZCURVE_MATRIX_CSV, TEXT_FILE_ENCODING, CSV_FILE_ENCODING


def get_r0_impedance(battery_number: int) -> float:
    """
    Extract R0 impedance (Zreal at Zimag ≈ 0) for a specific battery from its EIS .DTA file.
    
    Reads the EIS .DTA file for the given battery number, extracts ZCURVE data,
    and finds the Zreal value at the point where Zimag is closest to zero.
    This represents the charge transfer impedance (R0).

    Parameters
    ----------
    battery_number : int
        Battery identifier (1-36). Used to locate EIS_B{number}.DTA file.

    Returns
    -------
    float
        R0 impedance value in Ohms. Returns 0.0 if file not found or extraction fails.
    
    Examples
    --------
    >>> r0 = get_r0_impedance(1)
    >>> print(f"Battery 1 R0: {r0:.4f} Ohm")
    Battery 1 R0: 0.1450 Ohm
    
    Notes
    -----
    - Expected file location: data/raw/eis/EIS_B{number}.DTA
    - Extracts ZCURVE TABLE section
    - Finds minimum |Zimag| and returns corresponding Zreal
    - Returns 0.0 gracefully if any error occurs
    """
    try:
        # Construct expected filename
        eis_file = Path(EIS_RAW_DIR) / f"EIS_B{battery_number}.DTA"
        
        if not eis_file.exists():
            return 0.0
        
        # Parse ZCURVE data from the file
        filas_zcurve = []
        capturando = False
        
        with open(eis_file, mode="r", encoding=TEXT_FILE_ENCODING, errors="replace") as f:
            for linea in f:
                if linea.startswith("ZCURVE") and "TABLE" in linea:
                    capturando = True
                    continue
                
                if capturando:
                    # Remove only trailing newline, don't strip leading tab which maintains column indices
                    linea_limpia = linea.rstrip('\n')
                    if not linea_limpia.strip():  # Skip completely empty lines
                        continue
                    
                    # Split by tab, preserving all columns including leading empty one
                    columnas = [col.strip() for col in linea_limpia.split('\t')]
                    if len(columnas) > 1:  # At least one non-empty column
                        filas_zcurve.append(columnas)
        
        if not filas_zcurve or len(filas_zcurve) < 3:
            return 0.0
        
        # Skip header (row 0: column names, row 1: units)
        # Column indices after tab split: [0]=empty, [1]=Pt, [2]=Time, [3]=Freq, [4]=Zreal, [5]=Zimag, ...
        # Extract Zreal and Zimag values
        zreal_values = []
        zimag_values = []
        
        for fila in filas_zcurve[2:]:
            try:
                # Zreal is at index 4, Zimag is at index 5 (after tab split with leading empty column)
                zreal_str = fila[4].replace(',', '.')
                zimag_str = fila[5].replace(',', '.')
                zreal = float(zreal_str)
                zimag = float(zimag_str)
                zreal_values.append(zreal)
                zimag_values.append(zimag)
            except (ValueError, IndexError):
                continue
        
        if not zreal_values:
            return 0.0
        
        # Find index where |Zimag| is minimum (closest to zero)
        zimag_abs = np.array([abs(z) for z in zimag_values])
        min_idx = np.argmin(zimag_abs)
        
        # Return Zreal at that point (this is R0)
        r0 = zreal_values[min_idx]
        
        return float(r0)
    
    except Exception as e:
        return 0.0


def build_zcurve_matrix(eis_dir: Optional[str] = None, output_csv: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Extract ZCURVE data from EIS .DTA files and build a comprehensive impedance matrix.
    
    Searches for all .DTA files in eis_dir, extracts ZCURVE table data, and combines
    them into a single CSV where each row is a data point and columns are battery-specific.

    Parameters
    ----------
    eis_dir : str, optional
        Path to the EIS data directory. If None, uses default from config.
        Defaults to "data/raw/eis".
    output_csv : str, optional
        Path to save the output CSV. If None, uses default from config.
        Defaults to "data/processed/matriz_zcurve.csv".

    Returns
    -------
    Optional[pd.DataFrame]
        DataFrame with the extracted data, or None if no valid files found.
        Columns: Bateria_Num, Zreal (ohm), Zimag (ohm)
    
    Examples
    --------
    >>> df = build_zcurve_matrix()
    >>> print(df.head())
       Bateria_Num  Zreal (ohm)  Zimag (ohm)
    0            1        0.145        0.020
    1            1        0.146        0.018
    ...
    
    Notes
    -----
    - Expected .DTA file naming: EIS_B{number}.DTA (e.g., EIS_B1.DTA)
    - Extracts only rows between "ZCURVE TABLE" marker
    - Skips header rows (column names and units)
    - Converts comma decimal separators to periods
    """
    if eis_dir is None:
        eis_dir = str(EIS_RAW_DIR)
    if output_csv is None:
        output_csv = str(ZCURVE_MATRIX_CSV)
    
    base = Path(eis_dir)
    
    # Find all .DTA files (case-insensitive)
    todos_los_archivos = list(base.glob("*.[dD][tT][aA]"))
    
    if not todos_los_archivos:
        print(f"ERROR: No .DTA files found in '{base}'. Check the path.")
        return None

    # Extract battery number from filename (e.g. EIS_B1 -> 1) and store as tuple
    archivos_validos = []
    for archivo in todos_los_archivos:
        match = re.search(r'EIS_B(\d+)', archivo.name, re.IGNORECASE)
        if match:
            numero = int(match.group(1))
            archivos_validos.append((numero, archivo))
        else:
            print(f"SKIP: '{archivo.name}' — doesn't match format 'EIS_B#'.")

    # Sort by battery number
    archivos_validos.sort(key=lambda x: x[0])

    if not archivos_validos:
        print("ERROR: No valid files to process.")
        return None

    todas_las_filas = []
    encabezados_guardados = False

    # Process each file
    for numero, archivo_dta in archivos_validos:
        try:
            capturando = False
            filas_bateria = []
            
            with open(archivo_dta, mode="r", encoding=TEXT_FILE_ENCODING, errors="replace") as f:
                for linea in f:
                    if linea.startswith("ZCURVE") and "TABLE" in linea:
                        capturando = True
                        continue
                    
                    if capturando:
                        linea_limpia = linea.strip()
                        if not linea_limpia:
                            continue
                        
                        columnas = [col.strip() for col in linea_limpia.split('\t') if col.strip()]
                        if columnas:
                            filas_bateria.append(columnas)
            
            if filas_bateria:
                # Set up global headers once
                if not encabezados_guardados:
                    encabezados_globales = ["Bateria_Num"] + filas_bateria[0]
                    todas_las_filas.append(encabezados_globales)
                    encabezados_guardados = True
                
                # Extract numeric data (skip row 0: column names, row 1: units)
                for fila in filas_bateria[2:]:
                    # Convert comma to period for decimals
                    fila_numerica = [val.replace(',', '.') for val in fila]
                    # Add battery number at the beginning
                    todas_las_filas.append([numero] + fila_numerica)

        except Exception as e:
            print(f"ERROR processing '{archivo_dta.name}': {e} — skipping.")

    # --- Save matrix to CSV ---
    try:
        Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_csv, mode="w", newline="", encoding=CSV_FILE_ENCODING) as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(todas_las_filas)
            
        print(f"OK: ZCURVE matrix saved to: '{output_csv}'")
        
        # Return as DataFrame for convenience
        df = pd.read_csv(output_csv)
        return df
        
    except Exception as e:
        print(f"ERROR saving CSV: {e}")
        return None

import pandas as pd
import numpy as np

def actualizar_impedancia(archivo_zcurve="data/processed/matriz_zcurve.csv", 
                          archivo_baterias="data/processed/matriz_baterias.csv", 
                          output_csv="data/processed/matriz_baterias_actualizada.csv"):
    
    print("Cargando datos...")
    # 1. Cargar los archivos CSV
    df_zcurve = pd.read_csv(archivo_zcurve)
    df_baterias = pd.read_csv(archivo_baterias)

    # Buscar automáticamente el nombre exacto de las columnas (por si tienen espacios o unidades como 'Zreal (ohm)')
    col_zreal = [col for col in df_zcurve.columns if 'Zreal' in col][0]
    col_zimag = [col for col in df_zcurve.columns if 'Zimag' in col][0]

    # 2. Encontrar el Zreal donde Zimag es más cercano a 0
    # Calculamos el valor absoluto de Zimag para encontrar la distancia al cero
    df_zcurve['Zimag_abs'] = df_zcurve[col_zimag].abs()

    # Buscamos el índice (fila) del valor mínimo de 'Zimag_abs' para CADA batería
    indices_optimos = df_zcurve.groupby('Bateria_Num')['Zimag_abs'].idxmin()

    # Filtramos el dataframe original usando esos índices para quedarnos solo con los cruces por cero
    df_cruces = df_zcurve.loc[indices_optimos, ['Bateria_Num', col_zreal]]

    # 3. Cruzar la información con la matriz de baterías
    # Creamos un "diccionario" virtual que asocia: {Numero_Bateria : Valor_Zreal}
    mapa_impedancias = dict(zip(df_cruces['Bateria_Num'], df_cruces[col_zreal]))

    # Actualizamos la columna "Impedancia" buscando el "Numero" en nuestro mapa
    # Si alguna batería no tiene datos de impedancia, mantenemos el valor original (0) con fillna()
    df_baterias['Impedancia(Ohm)'] = df_baterias['Numero'].map(mapa_impedancias).fillna(df_baterias['Impedancia(Ohm)'])

    # 4. Guardar el nuevo CSV
    df_baterias.to_csv(output_csv, index=False)
    print(f"¡Listo! Se actualizaron las impedancias y el archivo se guardó como: '{output_csv}'")
    
    return df_baterias