#!/usr/bin/env python3
from test_framework.test_framework import TestFramework

class DARetrieveBlobTest(TestFramework):
    def setup_params(self):
        self.num_blockchain_nodes = 1
        self.num_nodes = 2

    def run_test(self):
        self.setup_da_node()
        # tx_seq and data mapping
        self.next_tx_seq = 0
        self.data = {}
        self.retrieve_blob_test()

    def retrieve_blob_test(self):
        print("retrieve_blob_test")

if __name__ == "__main__":
    DARetrieveBlobTest(blockchain_node_configs=dict(
        [(0, dict(mode="dev", dev_block_interval_ms=50))])).main()