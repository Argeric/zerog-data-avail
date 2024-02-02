#!/usr/bin/env python3

import os
import tempfile
import subprocess
import time

data_dir = '/mnt/zerog-data-avail/tests/tmp'
# args = ['/mnt/zerog-data-avail/tests/tmp/localstack', '-localstack-port 4566 -deploy-resources true localstack']
args = ['/mnt/zerog-data-avail/tests/tmp/da_encoder', '--disperser-encoder.grpc-port 34000         --disperser-encoder.metrics-http-port 9109         --kzg.g1-path ../inabox/resources/kzg/g1.point.300000         --kzg.g2-path ../inabox/resources/kzg/g2.point.300000         --kzg.cache-path ../inabox/resources/kzg/SRSTables         --kzg.srs-order 300000         --kzg.num-workers 12         --disperser-encoder.log.level-std trace         --disperser-encoder.log.level-file trace']
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

time.sleep(1000)
