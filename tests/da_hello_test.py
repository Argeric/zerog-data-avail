#!/usr/bin/env python3
import sys
sys.path.append("../zerog_storage_kv/tests")
import time

from da_test_framework.da_test_framework import DATestFramework


class DAHelloTest(DATestFramework):
    def setup_params(self):
        self.num_blockchain_nodes = 1
        self.num_nodes = 2

        print("===============================================")
        print("root dir:", self.root_dir)
        print("blockchain binary:", self.blockchain_binary)
        print("zgs binary:", self.zgs_binary)
        print("CLI binary:", self.cli_binary)
        print("contract path:", self.contract_path)
        print("token contract path:", self.token_contract_path)
        print("mine contract path:", self.mine_contract_path)
        print("===============================================")

    def run_test(self):
        print("hello")
        time.sleep(300)


if __name__ == "__main__":
    DAHelloTest(blockchain_node_configs=dict(
        [(0, dict(mode="dev", dev_block_interval_ms=50))])).main()
