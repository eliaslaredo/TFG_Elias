"""
Analysis functions for battery selection and assessment.

Includes functions for finding compatible battery sets and evaluating battery health.
"""

from typing import List

import numpy as np

from src.models.bateria import Bateria
from config import BEST_BATTERIES_COUNT


def find_best_18(baterias: List[Bateria]) -> List[Bateria]:
    """
    Select the best compatible batteries for pack formation.
    
    Finds a set of batteries with the most similar SoH values by searching for a
    sliding window of 18 batteries (sorted by SoH) that minimizes the spread
    (i.e., difference between max and min SoH) while maintaining good average health.

    This algorithm ensures that selected batteries have similar capacity characteristics,
    which is important for:
    - Even load distribution during charging/discharging
    - Balanced cell voltages
    - Improved pack longevity and performance

    Parameters
    ----------
    baterias : List[Bateria]
        List of Bateria objects with SoH values measured. 
        Must have at least 18 batteries.

    Returns
    -------
    List[Bateria]
        List of 18 selected Bateria objects, sorted by original battery number,
        representing the most compatible set for pack formation.
    
    Raises
    ------
    ValueError
        If fewer than 18 batteries are provided.
    
    Notes
    -----
    Algorithm works as follows:
    1. Sorts all batteries by SoH value
    2. Slides a window of 18 batteries through the sorted list
    3. Calculates spread (max - min) for each window
    4. If spreads are equal, also considers mean SoH (prefers higher mean)
    5. Selects window with minimum spread (or highest mean if tied)
    6. Returns selected batteries sorted by original battery number
    """
    
    # Filter out None values
    valid_baterias = [b for b in baterias if b is not None]
    
    if len(valid_baterias) < BEST_BATTERIES_COUNT:
        raise ValueError(
            f"Need at least {BEST_BATTERIES_COUNT} batteries, but got {len(valid_baterias)}"
        )
    
    # Extract SoH values and get sorting indices
    values = np.array([b.soh for b in valid_baterias])
    sorted_indices = np.argsort(values)
    sorted_values = values[sorted_indices]

    best_window = 0
    best_spread = np.inf
    best_mean = -np.inf

    # Slide a window of 18 through the sorted values
    window_size = BEST_BATTERIES_COUNT
    for i in range(len(sorted_values) - window_size + 1):
        window = sorted_values[i : i + window_size]
        spread = window[-1] - window[0]
        mean = window.mean()
        
        # Prefer smaller spread, or if equal, higher mean SoH
        if spread < best_spread or (spread == best_spread and mean > best_mean):
            best_window = i
            best_spread = spread
            best_mean = mean

    # Get the indices of selected batteries in the original list
    selected_indices = sorted_indices[best_window : best_window + window_size]
    
    # Extract selected batteries and sort by original battery number
    selected = [valid_baterias[i] for i in sorted(selected_indices)]
    
    return selected
