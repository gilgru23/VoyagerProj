
import sys
import manage

# args = [sys.argv[0], 'test', 'voyager_system.tests.unit']
args = [sys.argv[0], 'test', 'voyager_system.tests.unit.domain.medicalCenter']
sys.argv = args
manage.main()

