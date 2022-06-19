
import sys
import manage

# args = [sys.argv[0], 'test', 'voyager_system.tests.integration']
args = [sys.argv[0], 'test', 'voyager_system.tests.integration.domain.medicalCenter.test_marketplace']
sys.argv = args
manage.main()
