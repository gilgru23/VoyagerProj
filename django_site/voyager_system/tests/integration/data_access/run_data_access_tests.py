import sys
import manage

if __name__ == '__main__':
    args = [sys.argv[0], 'test', 'voyager_system.tests.integration.data_access.test_database_proxy']
    sys.argv = args
    manage.main()

