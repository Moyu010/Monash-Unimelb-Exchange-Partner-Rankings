class University:
    def __init__(self, name="", rank="10000", link="", location="", faculty=""):
        self.name = name
        self.rank = rank
        self.link = link
        self.location = location
        self.faculty = faculty

    def __repr__(self):
        return self.name + "\nranked " + self.rank + " in the world"