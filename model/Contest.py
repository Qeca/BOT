class Contest():
    def __init__(self, id: int, name: str, regStartDate: str, regEndDate: str,
                 eventStartDate: str, eventEndDate: str, place: str, value: str,
                 period: str, link: str, tag: str, status: str, students: list):
        self.id: int = id
        self.name: str = name
        self.regStartDate: str = regStartDate
        self.regEndDate: str = regEndDate
        self.eventStartDate: str = eventStartDate
        self.eventEndDate: str = eventEndDate
        self.place: str = place
        self.value: str = value
        self.period: str = period
        self.link: str = link
        self.tag: str = tag
        self.status: str = status
        self.students: list = students
