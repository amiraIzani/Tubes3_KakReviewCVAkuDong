import os
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def get_cv_path(relative_path: str) -> str | None:
    if not os.path.exists(DATA_DIR):
        print(f"Data directory does not exist: {DATA_DIR}", file=sys.stderr)
        return None
    full_path = os.path.join(DATA_DIR, os.path.basename(relative_path))

    if os.path.exists(full_path):
        return full_path
    else:
        print(f"Warning: CV file not found at {full_path}")
        return None
    
def open_file_with_default_app(filepath: str):
    # Opens a file with system's default application (for "View CV" feature)
    if not filepath or not os.path.exists(filepath):
        print(f"Error: Cannot open file. Path doesn not exist: {filepath}")
        return
    
    try:
        if sys.platform.startswith('win32'):
            os.startfile(filepath)
        elif sys.platform.startswith('darwin'): # macOS
            subprocess.run(['open', filepath], check=True)
        else: # linux
            subprocess.run(['xdg-open', filepath], check=True)
    except Exception as e:
        print(f"Error opening file {filepath}: {e}", file=sys.stderr)
        return