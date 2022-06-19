import sys

import manage



if __name__ == '__main__':
    # args = [sys.argv[0], 'test', 'voyager_system.tests.service']
    args = [sys.argv[0], 'test', 'voyager_system.tests.service.test_consumer.TestConsumer.test_concurrent_pod_register']
    sys.argv = args
    manage.main()
