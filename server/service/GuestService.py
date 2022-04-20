import domain.SystemManagement as SystemManagement

# from server.domain.SystemManagement import SystemManagement


# class GuestService:
#     def __init__(self) -> None:
#         self.system_management = SystemManagement()
#         pass

# email, pwd, phone, f_name, l_name, dob
def create_account(email: str, pwd: str, phone: str, f_name: str, l_name: str, dob: str) -> str:
    return SystemManagement.create_account(email, pwd, phone, f_name, l_name, dob)

def login(email: str, pwd: str) -> str:
    return SystemManagement.login(email, pwd)

def create_consumer_profile(id: int, residence:str, height:int, weight:int, units: str, gender:chr, goal:any) -> str:
    return SystemManagement.create_consumer_profile(id, residence, height, weight, units, gender, goal)
