class ResponseManager:
    def __init__(self, id: int, firstname: str, lastname: str, company: str = None):
        self.id: int = id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.company: str = company