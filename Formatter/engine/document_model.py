class SubSection:

    def __init__(self,title,number):

        self.title = title

        self.number = number

        self.content = []

        self.bullets = []


class Section:

    def __init__(self,title,number):

        self.title = title

        self.number = number

        self.content = []

        self.subsections = []

        self.bullets = []


class DocumentModel:

    def __init__(self):

        self.sections = []

    def add_section(self,section):

        self.sections.append(section)