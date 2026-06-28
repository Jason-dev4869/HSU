#!/usr/bin/env python3
"""
Application Entry Point
Author: Senior Machine Learning Engineer
Description: Initializes and spins up the UI App Window loop context.
"""

import sys
from pathlib import Path

# Force add runtime root context paths mapping to prevent package resolving exceptions
sys.path.append(str(Path(__file__).parent))

from src.ui.app_window import AppWindow


def main():
    # Initialize the complete system application loop
    app = AppWindow()
    app.run = app.launch()


if __name__ == "__main__":
    main()