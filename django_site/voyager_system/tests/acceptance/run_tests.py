import sys

import manage

if __name__ == '__main__':
    args = [sys.argv[0], 'test', 'voyager_system.tests.acceptance']
    sys.argv = args
    manage.main()
