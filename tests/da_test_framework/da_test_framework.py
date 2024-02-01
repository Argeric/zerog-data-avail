import os
import sys
import argparse

sys.path.append("../../zerog_storage_kv/tests")

from test_framework.test_framework import TestFramework
from test_framework.blockchain_node import BlockChainNodeType
from utility.kv import MAX_STREAM_ID, to_stream_id
from utility.utils import is_windows_platform
from da_test_framework.da_node import LocalStack, DAEncoder, DABatcher, DAServer

__file_path__ = os.path.dirname(os.path.realpath(__file__))


class DATestFramework(TestFramework):

    def __init__(
            self,
            blockchain_node_type=BlockChainNodeType.Conflux,
            blockchain_node_configs={},
    ):
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
        super(DATestFramework, self).__init__()

    def setup_nodes(self):
        super().setup_nodes()
        # setup kv node, watch stream with id [0,100)
        self.stream_ids = [to_stream_id(i) for i in range(MAX_STREAM_ID)]
        self.stream_ids.reverse()
        super().setup_kv_node(0, self.stream_ids)
        self.setup_da_node()

    def stop_nodes(self):
        super().stop_nodes()
        for service in self.da_services:
            service.stop()

    def setup_da_node(self, updated_config={}):
        local_stack = LocalStack(self.root_dir, updated_config, self.log)
        self.da_services.append(local_stack)
        local_stack.setup_config()
        local_stack.start()

        da_encoder = DAEncoder(self.root_dir, updated_config, self.log)
        self.da_services.append(da_encoder)
        da_encoder.setup_config()
        da_encoder.start()

        da_batcher = DABatcher(self.root_dir, updated_config, self.contract.address(), self.log)
        self.da_services.append(da_batcher)
        da_batcher.setup_config()
        da_batcher.start()

        da_server = DAServer(self.root_dir, updated_config, self.log)
        self.da_services.append(da_server)
        da_server.setup_config()
        da_server.start()

    def __parse_arguments(self):
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

        da_options = parser.parse_args()
        var_type = type(da_options)
        print("da_options =================================== " + str(da_options) + "   " + str(var_type))

    def main(self):
        self.__parse_arguments()
        super().main()
