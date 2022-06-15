import sys

import manage



if __name__ == '__main__':
    args = [sys.argv[0], 'test', 'voyager_system.tests.service']
    sys.argv = args
    manage.main()

    #
    # # !/usr/bin/env python
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'voyager_system.tests.test_settings'
    # django.setup()
    # TestRunner = get_runner(settings)
    # test_runner = TestRunner()
    # failures = test_runner.run_tests(["voyager_system.tests.acceptance"])
    # sys.exit(bool(failures))
