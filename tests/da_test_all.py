#!/usr/bin/env python3
import os
import sys

sys.path.append("../zerog_storage_kv/zerog-storage-rust/tests")

from utility.run_all import run_all

__file_path__ = os.path.dirname(os.path.realpath(__file__))
print(f"__file__ {__file__}")
print(f"__real_path__ {os.path.realpath(__file__)}")
print(f"__file_path__ {__file_path__}")

if __name__ == "__main__":
    run_all(test_dir=os.path.dirname(__file__))
