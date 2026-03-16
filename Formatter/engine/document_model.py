class SubSection:

    def __init__(self,title,number):

        self.title=title

        self.number=number

        self.content=[]


class Section:

    def __init__(self,title,number):

        self.title=title

        self.number=number

        self.content=[]

        self.subsections=[]


class DocumentModel:

    def __init__(self):

        self.sections=[]

    def add_section(self,section):

        self.sections.append(section)