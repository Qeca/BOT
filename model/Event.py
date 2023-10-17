class Event():
    def __init__(self, id: int, name: str, regStartDate: str, regEndDate: str,
                 eventStartDate: str, eventEndDate: str, place: str, organiser: str,
                 tags: str, link: str, info: str, status: str, students: list):
        self.id: int = id
        self.name: str = name
        self.regStartDate: str = regStartDate
        self.regEndDate: str = regEndDate
        self.eventStartDate: str = eventStartDate
        self.eventEndDate: str = eventEndDate
        self.place: str = place
        self.organiser: str = organiser
        self.tags: str = tags
        self.link: str = link
        self.info: str = info
        self.status: str = status
        self.students: list = students

    def __str__(self):
        return f"{self.id}): {self.name}"