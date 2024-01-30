import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
relative_path = os.path.join(current_path, '..', 'zerog_storage_kv')
sys.path.append(relative_path)

