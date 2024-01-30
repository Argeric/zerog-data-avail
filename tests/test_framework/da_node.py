import os
from enum import unique

from zerog_storage_kv.tests.test_framework.blockchain_node import TestNode
from zerog_storage_kv.tests.utility.utils import blockchain_rpc_port
from zerog_storage_kv.tests.config.node_config import GENESIS_PRIV_KEY
from zerog_storage_kv.tests.test_framework.blockchain_node import NodeType as ParentNodeType

@unique
class NodeType(ParentNodeType):
    DA_LOCAL_STACK = 3
    DA_ENCODER = 4
    DA_BATCHER = 5
    DA_SERVER = 6

class LocalStack(TestNode):
    def __init__(
        self,
        root_dir,
        updated_config,
        log,
    ):
        local_conf = dict(log_config_file="log_config")

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "local_stack")
        super().__init__(
            NodeType.DA_LOCAL_STACK,
            0,
            data_dir,
            None,
            None,
            local_conf,
            log,
            None,
        )
        self.args = ["go run ./deploy/cmd -localstack-port 4566 -deploy-resources true localstack"]

    def start(self):
        self.log.info("Start local stack")
        super().start()

class DAEncoder(TestNode):
    def __init__(
            self,
            root_dir,
            updated_config,
            log,
    ):
        local_conf = dict(log_config_file="log_config")

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "da_encoder")
        super().__init__(
            NodeType.DA_ENCODER,
            0,
            data_dir,
            None,
            None,
            local_conf,
            log,
            None,
        )
        self.args = ["go run ./disperser/cmd/encoder \
        --disperser-encoder.grpc-port 34000 \
        --disperser-encoder.metrics-http-port 9109 \
        --kzg.g1-path ../inabox/resources/kzg/g1.point.300000 \
        --kzg.g2-path ../inabox/resources/kzg/g2.point.300000 \
        --kzg.cache-path ../inabox/resources/kzg/SRSTables \
        --kzg.srs-order 300000 \
        --kzg.num-workers 12 \
        --disperser-encoder.log.level-std trace \
        --disperser-encoder.log.level-file trace"]

    def start(self):
        self.log.info("Start da encoder")
        super().start()

class DABatcher(TestNode):
    def __init__(
            self,
            root_dir,
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
        super().__init__(
            NodeType.DA_BATCHER,
            0,
            data_dir,
            None,
            None,
            local_conf,
            log,
            None,
        )
        self.args = [f"go run ./disperser/cmd/batcher \
        --batcher.pull-interval 10s \
        --chain.rpc {local_conf['blockchain_rpc_endpoint']} \
        --chain.private-key {GENESIS_PRIV_KEY} \
        --batcher.finalizer-interval 20s \
        --batcher.aws.region us-east-1 \
        --batcher.aws.access-key-id localstack \
        --batcher.aws.secret-access-key localstack \
        --batcher.aws.endpoint-url http://0.0.0.0:4566 \
        --batcher.s3-bucket-name test-zgda-blobstore \
        --batcher.dynamodb-table-name test-BlobMetadata \
        --encoder-socket 0.0.0.0:34000 \
        --batcher.batch-size-limit 10000 \
        --batcher.srs-order 300000 \
        --encoding-timeout 10s \
        --chain-read-timeout 12s \
        --chain-write-timeout 13s \
        --batcher.storage.node-url http://0.0.0.0:5678 \
        --batcher.storage.node-url http://0.0.0.0:6789 \
        --batcher.storage.kv-url http://0.0.0.0:7890 \
        --batcher.storage.kv-stream-id 000000000000000000000000000000000000000000000000000000000000f2bd \
        --batcher.storage.flow-contract	{local_conf['log_contract_address']}"]

    def start(self):
        self.log.info("Start da batcher")
        super().start()

class DAServer(TestNode):
    def __init__(
            self,
            root_dir,
            updated_config,
            log,
    ):
        local_conf = dict(log_config_file="log_config")

        # Overwrite with personalized configs.
        local_conf.update(updated_config)
        data_dir = os.path.join(root_dir, "da_server")
        super().__init__(
            NodeType.DA_SERVER,
            0,
            data_dir,
            None,
            None,
            local_conf,
            log,
            None,
        )
        self.args = ["go run ./disperser/cmd/apiserver \
        --disperser-server.grpc-port 51001 \
        --disperser-server.s3-bucket-name test-zgda-blobstore \
        --disperser-server.dynamodb-table-name test-BlobMetadata \
        --disperser-server.aws.region us-east-1 \
        --disperser-server.aws.access-key-id localstack \
        --disperser-server.aws.secret-access-key localstack \
        --disperser-server.aws.endpoint-url http://0.0.0.0:4566"]

    def start(self):
        self.log.info("Start da server")
        super().start()