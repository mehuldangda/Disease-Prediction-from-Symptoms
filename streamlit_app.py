"""
🩺 DiagnoWise AI - Streamlit Entry Point Wrapper
Seamlessly invokes the main app.py application for Streamlit Cloud and local execution.
"""

import os
import sys
import runpy

# Ensure root directory is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Run the master app.py
app_path = os.path.join(ROOT_DIR, "app.py")
runpy.run_path(app_path, run_name="__main__")
