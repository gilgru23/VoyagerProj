import sys

import manage



if __name__ == '__main__':
    args = [sys.argv[0], 'test', 'voyager_system.tests.service']
    # args = [sys.argv[0], 'test', 'voyager_system.tests.service.test_consumer_advanced']
    sys.argv = args
    manage.main()
