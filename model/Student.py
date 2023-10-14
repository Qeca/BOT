class Student:
    def __init__(self, id: str, identificationNumber: str, firstname: str, lastname: str, patronymic: str, groupNumber: str, events: list, contests: list):
        self.id: str = id
        self.identificationNumber: str = identificationNumber
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.patronymic: str = patronymic
        self.groupNumber: str = groupNumber
        self.events: list = events
        self.contests: list = contests