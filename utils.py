import sys
import os

def resource_path(*parts):
    """Resolve resource paths when empacotado com PyInstaller (onefile)"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, *parts)

