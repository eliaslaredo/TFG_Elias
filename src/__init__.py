"""
TFG Elias - Battery Analysis Package

A modular Python package for analyzing lithium battery recycling data from vape devices.
Includes data processing, SoH calculation, impedance analysis, and visualization.

Modules:
  - models: Data structures (Bateria class)
  - data_io: File input/output operations
  - processing: Data cleaning and transformation
  - analysis: Analysis functions (SoH, impedance, statistics)
  - utils: Shared utilities
"""

__version__ = "1.0.0"
__author__ = "Elias Laredo Fernández"

from src.models import Bateria

__all__ = ["Bateria"]
