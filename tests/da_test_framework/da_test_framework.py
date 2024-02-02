import os
import sys
import argparse
import time

sys.path.append("../../zerog_storage_kv/tests")

from test_framework.test_framework import TestFramework
from test_framework.blockchain_node import BlockChainNodeType
from utility.kv import MAX_STREAM_ID, to_stream_id
from utility.utils import is_windows_platform
from da_test_framework.da_node import LocalStack, DAEncoder, DABatcher, DAServer

__file_path__ = os.path.dirname(os.path.realpath(__file__))


# go build -o ./tests/tmp/localstack ./inabox/deploy/cmd
# go build -o ./tests/tmp/da_encoder ./disperser/cmd/encoder
# go build -o ./tests/tmp/da_batcher ./disperser/cmd/batcher
# go build -o ./tests/tmp/da_server ./disperser/cmd/apiserver

class DATestFramework(TestFramework):

    def __init__(
            self,
            blockchain_node_type=BlockChainNodeType.Conflux,
            blockchain_node_configs={},
    ):
        self.localstack_binary = None
        self.da_encoder_binary = None
        self.da_batcher_binary = None
        self.da_server_binary = None
        self.stream_ids = None
        self.da_services = []
        binary_ext = ".exe" if is_windows_platform() else ""
        tests_dir = os.path.dirname(__file_path__)
        self.__default_localstack_binary__ = os.path.join(
            tests_dir, "tmp", "localstack" + binary_ext
        )
        self.__default_da_encoder_binary__ = os.path.join(
            tests_dir, "tmp", "da_encoder" + binary_ext
        )
        self.__default_da_batcher_binary__ = os.path.join(
            tests_dir, "tmp", "da_batcher" + binary_ext
        )
        self.__default_da_server_binary__ = os.path.join(
            tests_dir, "tmp", "da_server" + binary_ext
        )
        super(DATestFramework, self).__init__(blockchain_node_type, blockchain_node_configs)

    def setup_nodes(self):
        super().setup_nodes()
        # setup kv node, watch stream with id [0,100)
        self.stream_ids = [to_stream_id(i) for i in range(MAX_STREAM_ID)]
        self.stream_ids.reverse()
        super().setup_kv_node(0, self.stream_ids)
        self.setup_da_node()

    def stop_nodes(self):
        # super().stop_nodes()
        # for service in self.da_services:
        #     service.stop()
        print("stop_nodes need to implement")

    def setup_da_node(self, updated_config={}):
        self.log.info("Start deploy DA services")
        local_stack = LocalStack(self.root_dir, self.localstack_binary, updated_config, self.log)
        self.da_services.append(local_stack)
        local_stack.setup_config()
        local_stack.start()
        time.sleep(1)
        local_stack.wait_for_rpc_connection()

        # da_encoder = DAEncoder(self.root_dir, self.da_encoder_binary, updated_config, self.log)
        # self.da_services.append(da_encoder)
        # da_encoder.setup_config()
        # da_encoder.start()
        # time.sleep(1)
        # da_encoder.wait_for_rpc_connection()
        #
        # da_batcher = DABatcher(self.root_dir, self.da_batcher_binary, updated_config, self.contract.address(), self.log)
        # self.da_services.append(da_batcher)
        # da_batcher.setup_config()
        # da_batcher.start()
        # time.sleep(1)
        # da_batcher.wait_for_rpc_connection()
        #
        # da_server = DAServer(self.root_dir, self.da_server_binary, updated_config, self.log)
        # self.da_services.append(da_server)
        # da_server.setup_config()
        # da_server.start()
        # time.sleep(1)
        # da_server.wait_for_rpc_connection()
        self.log.info("All DA service started")

    def __da_parse_arguments(self):
        parser = argparse.ArgumentParser(usage="%(prog)s [options]")

        parser.add_argument(
            "--localstack-binary",
            dest="localstack",
            default=self.__default_localstack_binary__,
            type=str,
        )

        parser.add_argument(
            "--da-encoder-binary",
            dest="da_encoder",
            default=self.__default_da_encoder_binary__,
            type=str,
        )

        parser.add_argument(
            "--da-batcher-binary",
            dest="da_batcher",
            default=self.__default_da_batcher_binary__,
            type=str,
        )

        parser.add_argument(
            "--da-server-binary",
            dest="da_server",
            default=self.__default_da_server_binary__,
            type=str,
        )

        parser.add_argument("--randomseed", dest="random_seed", type=int, help="Set a random seed")

        parser.add_argument("--port-min", dest="port_min", default=11000, type=int)

        self.da_options = parser.parse_args()

    def main(self):
        self.__da_parse_arguments()
        self.localstack_binary = self.da_options.localstack
        self.da_encoder_binary = self.da_options.da_encoder
        self.da_batcher_binary = self.da_options.da_batcher
        self.da_server_binary = self.da_options.da_server
        assert os.path.exists(self.localstack_binary), (
                "localstack binary not found: %s" % self.localstack_binary
        )
        assert os.path.exists(self.da_encoder_binary), (
                "da encoder binary not found: %s" % self.da_encoder_binary
        )
        assert os.path.exists(self.da_batcher_binary), (
                "da batcher binary not found: %s" % self.da_batcher_binary
        )
        assert os.path.exists(self.da_server_binary), (
                "da server binary not found: %s" % self.da_server_binary
        )
        super().main()
