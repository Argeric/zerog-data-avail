#!/usr/bin/env python3

import os
import tempfile
import subprocess

data_dir = '/mnt/zerog-data-avail/tests/tmp'
args = ['/mnt/zerog-data-avail/tests/tmp/localstack', '-localstack-port 4566 -deploy-resources true localstack']
stdout = tempfile.NamedTemporaryFile(
    dir=data_dir, prefix="stdout", delete=False
)
my_env = os.environ.copy()
localstack = subprocess.Popen(
    args,
    stdout=stdout,
    stderr=stdout,
    cwd=data_dir,
    env=my_env,
)
print(f"localstack pid ====== {localstack.pid}")
