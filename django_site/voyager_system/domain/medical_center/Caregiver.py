
from voyager_system.domain.system_management.Account import Account

class Caregiver(Account):

    def __init__(self) -> None:
        super().__init__()
        self.consumers = []  # list of associated consumers' ids.  (n-to-m relationship)
