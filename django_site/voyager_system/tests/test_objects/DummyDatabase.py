from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Pod import Pod


class DummyDatabase:
    consumer_factory = None
    def __init__(self, consumer_factory):
        super(DummyDatabase, self).__init__()
        self.consumer_factory = consumer_factory

    # methods
    def get_consumer(self,consumer_id):
        print("DummyMapper: get_consumer was called")
        return self.consumer_factory(consumer_id)

    def get_pod(self, pod_serial_num):
        print("DummyMapper: get_pod was called")
        consumer: Consumer = self.consumer_factory(0)
        pods = consumer.get_pods()
        pods = {p.serial_number:p for p in pods}
        return pods[pod_serial_num]


    def get_consumer_pods(self, consumer_id):
        print("DummyMapper: get_consumer_pods was called")
        consumer: Consumer = self.consumer_factory(0)
        pods = consumer.get_pods()
        return pods

    def get_consumer_dosing(self,consumer_id):
        print("DummyMapper: get_consumer_dosing was called")
        consumer: Consumer = self.consumer_factory(0)
        dosings = consumer.get_dosage_history()
        return dosings

    def add_dosing(self, new_dosing):
        print("DummyMapper: add_dosing was called")
        pass
    
    def update_pod(self, pod, consumer_id):
        print("DummyMapper: update_pod was called")
        pass

    def set_dispenser_consumer(self, dispenser_serial_number, consumer_id):
        raise NotImplementedError("Should have implemented this")