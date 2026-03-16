import re

class StructureDetector:

    def clean_text(self,text):

        text = text.strip()

        if len(text)==0:
            return ""

        # ignore punctuation lines
        if re.match(r'^[^A-Za-z0-9]+$',text):

            return ""

        return text


    def is_title(self,para):

        text=self.clean_text(para.text)

        if text=="":
            return False

        for run in para.runs:

            if run.bold:

                if run.font.size:

                    if run.font.size.pt>=15:

                        return True

        return False


    def is_author(self,para):

        text=self.clean_text(para.text)

        if text=="":

            return False

        if "," not in text:

            return False

        for run in para.runs:

            if run.italic:

                return True

        return False


    def is_heading(self,para):

        text=self.clean_text(para.text)

        if text=="":

            return False

        # detect numbered section: 1 INTRODUCTION
        if re.match(r'^\d+\s+',text):

            return True

        # detect ABSTRACT
        if text.lower()=="abstract":

            return True

        return False


    def is_subheading(self,para):

        text=self.clean_text(para.text)

        if text=="":

            return False

        # detect 2.1 style headings
        if re.match(r'^\d+(\.\d+)+\.?\s*', text):

            return True

        return False


    def is_bullet(self,para):

        text=self.clean_text(para.text)

        if text=="":

            return False

        if re.match(r'^[•\-–]',text):

            return True

        return False


    def classify(self,para):

        text=self.clean_text(para.text)

        if text=="":
            return "IGNORE"

        if self.is_title(para):
            return "TITLE"

        if self.is_author(para):
            return "AUTHOR"

        if self.is_heading(para):
            return "HEADING"

        if self.is_subheading(para):
            return "SUBHEADING"

        if self.is_bullet(para):
            return "BULLET"

        return "PARAGRAPH"