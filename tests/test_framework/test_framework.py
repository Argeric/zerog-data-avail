from ..zerog_storage_kv.tests.test_framework.test_framework import TestFramework as ParentTestFramework
from ..zerog_storage_kv.tests.utility.kv import MAX_STREAM_ID, to_stream_id
from tests.test_framework.da_node import LocalStack, DAEncoder, DABatcher, DAServer

class TestFramework(ParentTestFramework):

    def setup_nodes(self):
        super.setup_nodes()
        # setup kv node, watch stream with id [0,100)
        self.stream_ids = [to_stream_id(i) for i in range(MAX_STREAM_ID)]
        self.stream_ids.reverse()
        super.setup_kv_node(0, self.stream_ids)
        self.setup_da_node()

    def stop_nodes(self):
        super.stop_nodes()
        for service in self.da_services:
            service.stop()

    def setup_da_node(self, updated_config={}):
        classes = [LocalStack, DAEncoder, DABatcher, DAServer]
        for Clazz in classes:
            if Clazz == DABatcher:
                service = Clazz(self.root_dir, updated_config, self.contract.address(), self.log)
            else:
                service = Clazz(self.root_dir, updated_config, self.log)
            self.da_services.append(service)
            service.setup_config()
            service.start()