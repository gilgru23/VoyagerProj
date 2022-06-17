import sys

import manage



if __name__ == '__main__':
    # args = [sys.argv[0], 'test', 'voyager_system.tests.service']
    args = [sys.argv[0], 'test', 'voyager_system.tests.service.test_consumer.TestConsumer.test_concurrent_pod_update_2']
    # args = [sys.argv[0], 'test', 'voyager_system.tests.service.test_consumer.TestConsumer.test_tests']
    sys.argv = args
    manage.main()
