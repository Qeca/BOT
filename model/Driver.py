class Driver:
    def __init__(self, id: int, firstname: str, lastname: str, companyId: str = None):
        self.id: int = id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.companyId: str = companyId
