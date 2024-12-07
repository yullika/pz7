import sys
import os

path= 'C:\Пз7_flask>'
if path not in sys.path:
    sys.path.append(path)
from app import app as application