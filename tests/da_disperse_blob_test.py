#!/usr/bin/env python3
from tests.test_framework.test_framework import TestFramework

class DADisperseBlobTest(TestFramework):
    def setup_params(self):
        self.num_blockchain_nodes = 1
        self.num_nodes = 2

    def run_test(self):
        # tx_seq and data mapping
        self.next_tx_seq = 0
        self.data = {}
        self.get_blob_status_test()

    def get_blob_status_test(self):
        print("get_blob_status_test")

if __name__ == "__main__":
    DADisperseBlobTest(blockchain_node_configs=dict(
        [(0, dict(mode="dev", dev_block_interval_ms=50))])).main()