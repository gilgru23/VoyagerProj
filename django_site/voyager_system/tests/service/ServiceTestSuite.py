import sys

import manage



if __name__ == '__main__':
    args = [sys.argv[0], 'test', 'voyager_system.tests.service.test_consumer']
    # args = [sys.argv[0], 'test', 'voyager_system.tests.service.test_guest']
    # args = [sys.argv[0], 'test', 'voyager_system.tests.service']
    sys.argv = args
    manage.main()
