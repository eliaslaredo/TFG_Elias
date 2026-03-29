"""
File organization utilities for raw battery data.

Handles organizing raw cycler files by extraction date from filename patterns.
"""

import os
import shutil
import re
from pathlib import Path
from config import CYCLER_RANGE, CYCLING_PROCESSED_DIR


def organizar_archivos_por_fecha(carpeta_origen: str, cycler_id: int = None):
    """
    Organize files from a cycler folder into subfolders by extraction date.
    
    Searches for files matching the date pattern AAAA_MM_DD in filenames and creates
    corresponding date-based subfolders. Files are copied (not moved) to preserve originals.
    
    Parameters
    ----------
    carpeta_origen : str
        Path to the source folder containing raw cycler files
    cycler_id : int, optional
        Cycler identifier (1-6). If provided, files are organized into
        CYCLING_PROCESSED_DIR/{cycler_id}/{date}/ folders.
        If None, only scans without organizing.
    
    Returns
    -------
    dict
        Statistics: {"organized": count, "skipped": count, "errors": errors_list}
    
    Examples
    --------
    >>> result = organizar_archivos_por_fecha("data/raw/cicladores/ciclador_1", cycler_id=1)
    >>> print(f"Organized: {result['organized']} files")
    
    Notes
    -----
    - Expected filename format: something_2026_02_23_HH_MM_SS.txt
    - Date must be in AAAA_MM_DD format (e.g., 2026_02_23)
    - Files are copied, not moved, to preserve raw data integrity
    """
    
    # Expresión regular para buscar el formato de fecha AAAA_MM_DD
    # \d{4} = 4 dígitos (año), \d{2} = 2 dígitos (mes/día)
    patron_fecha = re.compile(r"(\d{4}_\d{2}_\d{2})")

    # Verificamos que la carpeta de origen exista
    if not os.path.exists(carpeta_origen):
        print(f"ERROR: La carpeta '{carpeta_origen}' no existe.")
        return {"organized": 0, "skipped": 0, "errors": [f"Source folder not found: {carpeta_origen}"]}

    stats = {"organized": 0, "skipped": 0, "errors": []}

    # Iterar sobre todos los elementos en la carpeta
    for nombre_archivo in os.listdir(carpeta_origen):
        ruta_completa_origen = os.path.join(carpeta_origen, nombre_archivo)

        # Nos aseguramos de procesar solo archivos (ignoramos carpetas)
        if not os.path.isfile(ruta_completa_origen):
            continue
            
        # Buscamos el patrón de la fecha en el nombre del archivo
        coincidencia = patron_fecha.search(nombre_archivo)
        
        if coincidencia:
            # Extraemos la fecha encontrada (ej. '2026_02_23')
            fecha_carpeta = coincidencia.group(1)
            
            if cycler_id is None:
                stats["skipped"] += 1
                continue
            
            # Definimos la ruta de la nueva carpeta destino
            ruta_carpeta_destino = CYCLING_PROCESSED_DIR / str(cycler_id) / fecha_carpeta
            
            try:
                # Si la carpeta de esa fecha no existe, la creamos
                ruta_carpeta_destino.mkdir(parents=True, exist_ok=True)
                
                # Copiamos el archivo (preservamos el original en raw)
                ruta_completa_destino = ruta_carpeta_destino / nombre_archivo
                shutil.copy(ruta_completa_origen, ruta_completa_destino)
                stats["organized"] += 1
                
            except Exception as e:
                stats["errors"].append((nombre_archivo, str(e)))
        else:
            stats["skipped"] += 1

    return stats


def organizar_todos_los_cicladores():
    """
    Organize all cycler folders (1-6) by date.
    
    Processes each cycler folder and prints statistics for each.
    """
    print("Organizando archivos de todos los cicladores por fecha...\n")
    
    total_stats = {"organized": 0, "skipped": 0, "errors": []}
    
    for i in CYCLER_RANGE:
        mi_carpeta = f"data/raw/cicladores/ciclador_{i}"
        print(f"Procesando: {mi_carpeta} ...")
        
        stats = organizar_archivos_por_fecha(mi_carpeta, cycler_id=i)
        
        print(f"  OK Organizados: {stats['organized']}")
        print(f"  SKIP Omitidos: {stats['skipped']}")
        if stats['errors']:
            print(f"  ERROR Errores: {len(stats['errors'])}")
        print()
        
        total_stats["organized"] += stats["organized"]
        total_stats["skipped"] += stats["skipped"]
        total_stats["errors"].extend(stats["errors"])
    
    print("OK: Todas las carpetas han sido organizadas!")
    print(f"\nResumen total:")
    print(f"  Organizados: {total_stats['organized']}")
    print(f"  Omitidos: {total_stats['skipped']}")
    if total_stats["errors"]:
        print(f"  Errores: {len(total_stats['errors'])}")
    
    return total_stats
