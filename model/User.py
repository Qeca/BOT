class User:
    def __init__(self, id: int, firstname: str, lastname: str, role: str, companyId: str):
        self.id: int = id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.role: str = role
        self.companyId: str = companyId