import os
import sys

from enum import Enum, unique
from test_framework.blockchain_node import TestNode
from utility.utils import blockchain_rpc_port
from config.node_config import GENESIS_PRIV_KEY

sys.path.append("../../zerog_storage_kv/tests")
__file_path__ = os.path.dirname(os.path.realpath(__file__))


@unique
class DANodeType(Enum):
    DA_LOCAL_STACK = 3
    DA_ENCODER = 4
    DA_BATCHER = 5
    DA_SERVER = 6


class LocalStack(TestNode):
    def __init__(
            self,
            root_dir,
            binary,
            updated_config,
            log,
    ):
        local_conf = dict(log_config_file="log_config")

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "localstack")
        # rpc_url = "http://" + local_conf["rpc_listen_address"]
        super().__init__(
            DANodeType.DA_LOCAL_STACK,
            0,
            data_dir,
            None,
            binary,
            local_conf,
            log,
            None,
        )
        print(f"localstack binary =================== {binary}")
        self.args = [binary, "--localstack-port", "4566", "--deploy-resources", "true", "localstack"]
        print(f"localstack =================== {self.args}")

    def start(self):
        self.log.info("Start localstack")
        super().start()

    def wait_for_rpc_connection(self):
        # self._wait_for_rpc_connection(lambda rpc: rpc.zgs_getStatus() is not None)
        print("Localstack wait_for_rpc_connection need to implement")

    def stop(self):
        self.log.info("Stop localstack")
        os.system("docker stop localstack-test")


class DAEncoder(TestNode):
    def __init__(
            self,
            root_dir,
            binary,
            updated_config,
            log,
    ):
        local_conf = dict(log_config_file="log_config")

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "da_encoder")
        # rpc_url = "http://" + local_conf["rpc_listen_address"]
        super().__init__(
            DANodeType.DA_ENCODER,
            0,
            data_dir,
            None,
            binary,
            local_conf,
            log,
            None,
        )
        print(f"root_dir =================== {root_dir}")
        print(f"__file_path__ =================== {__file_path__}")
        self.args = [binary, "--disperser-encoder.grpc-port", "34000",
                     "--disperser-encoder.metrics-http-port", "9109",
                     "--kzg.g1-path", f"{__file_path__}/../../inabox/resources/kzg/g1.point.300000",
                     "--kzg.g2-path", f"{__file_path__}/../../inabox/resources/kzg/g2.point.300000",
                     "--kzg.cache-path", f"{__file_path__}/../../inabox/resources/kzg/SRSTables",
                     "--kzg.srs-order", "300000",
                     "--kzg.num-workers", "12",
                     "--disperser-encoder.log.level-std", "trace",
                     "--disperser-encoder.log.level-file", "trace"]
        print(f"DAEncoder =================== {self.args}")

    def start(self):
        self.log.info("Start DA encoder")
        super().start()

    def wait_for_rpc_connection(self):
        # self._wait_for_rpc_connection(lambda rpc: rpc.zgs_getStatus() is not None)
        print("DA encoder wait_for_rpc_connection need to implement")

    def stop(self):
        self.log.info("Stop DA encoder")
        try:
            super().stop(kill=True, wait=False)
        except AssertionError as e:
            err = repr(e)
            print(f"DA encoder =============1111====================== {err}")
            if "no RPC connection" in err:
                print("DA encoder =============2222====================== no RPC connection")
                self.log.debug(f"Stop DA encoder: no RPC connection")
            else:
                raise e


class DABatcher(TestNode):
    def __init__(
            self,
            root_dir,
            binary,
            updated_config,
            log_contract_address,
            log,
    ):
        local_conf = {
            "log_config_file": "log_config",
            "log_contract_address": log_contract_address,
            "blockchain_rpc_endpoint": f"http://127.0.0.1:{blockchain_rpc_port(0)}",
        }

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "da_batcher")
        # rpc_url = "http://" + local_conf["rpc_listen_address"]
        super().__init__(
            DANodeType.DA_BATCHER,
            0,
            data_dir,
            None,
            binary,
            local_conf,
            log,
            None,
        )
        self.args = [binary, "--batcher.pull-interval", "10s",
                     "--chain.rpc", local_conf['blockchain_rpc_endpoint'],
                     "--chain.private-key", GENESIS_PRIV_KEY,
                     "--batcher.finalizer-interval", "20s",
                     "--batcher.aws.region", "us-east-1",
                     "--batcher.aws.access-key-id", "localstack",
                     "--batcher.aws.secret-access-key", "localstack",
                     "--batcher.aws.endpoint-url", "http://0.0.0.0:4566",
                     "--batcher.s3-bucket-name", "test-zgda-blobstore",
                     "--batcher.dynamodb-table-name", "test-BlobMetadata",
                     "--encoder-socket", "0.0.0.0:34000",
                     "--batcher.batch-size-limit", "10000",
                     "--batcher.srs-order", "300000",
                     "--encoding-timeout", "10s",
                     "--chain-read-timeout", "12s",
                     "--chain-write-timeout", "13s",
                     "--batcher.storage.node-url", "http://0.0.0.0:5678",
                     "--batcher.storage.node-url", "http://0.0.0.0:6789",
                     "--batcher.storage.kv-url", "http://0.0.0.0:7890",
                     "--batcher.storage.kv-stream-id",
                     "000000000000000000000000000000000000000000000000000000000000f2bd",
                     "--batcher.storage.flow-contract", local_conf['log_contract_address']]
        print(f"DABatcher =================== {self.args}")

    def start(self):
        self.log.info("Start DA batcher")
        super().start()

    def wait_for_rpc_connection(self):
        # self._wait_for_rpc_connection(lambda rpc: rpc.zgs_getStatus() is not None)
        print("DA batcher wait_for_rpc_connection need to implement")

    def stop(self):
        self.log.info("Stop DA batcher")
        try:
            super().stop(kill=True, wait=False)
        except AssertionError as e:
            err = repr(e)
            print(f"DA encoder =============3333====================== {err}")
            if "no RPC connection" in err:
                print("DA encoder =============5555====================== no RPC connection")
                self.log.debug(f"Stop DA encoder: no RPC connection")
            else:
                raise e


class DAServer(TestNode):
    def __init__(
            self,
            root_dir,
            binary,
            updated_config,
            log,
    ):
        local_conf = dict(log_config_file="log_config")

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "da_server")
        # rpc_url = "http://" + local_conf["rpc_listen_address"]
        super().__init__(
            DANodeType.DA_SERVER,
            0,
            data_dir,
            None,
            binary,
            local_conf,
            log,
            None,
        )
        self.args = [binary, "--disperser-server.grpc-port", "51001",
                     "--disperser-server.s3-bucket-name", "test-zgda-blobstore",
                     "--disperser-server.dynamodb-table-name", "test-BlobMetadata",
                     "--disperser-server.aws.region", "us-east-1",
                     "--disperser-server.aws.access-key-id", "localstack",
                     "--disperser-server.aws.secret-access-key", "localstack",
                     "--disperser-server.aws.endpoint-url", "http://0.0.0.0:4566"]
        print(f"DAServer =================== {self.args}")

    def start(self):
        self.log.info("Start DA server")
        super().start()

    def wait_for_rpc_connection(self):
        # self._wait_for_rpc_connection(lambda rpc: rpc.zgs_getStatus() is not None)
        print("DA server wait_for_rpc_connection need to implement")

    def stop(self):
        self.log.info("Stop DA server")
        super().stop(kill=True, wait=False)
