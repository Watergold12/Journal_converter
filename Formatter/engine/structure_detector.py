import re

class StructureDetector:

    def clean_text(self,text):

        text=text.strip()

        if len(text)==0:
            return ""

        if re.match(r'^[^A-Za-z0-9]+$',text):

            return ""

        return text


    def get_numbering(self,para):

        try:

            if para._element.pPr is None:
                return False

            if para._element.pPr.numPr is not None:

                return True

        except:
            pass

        return False


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

        if self.get_numbering(para):

            try:

                level=para._element.pPr.numPr.ilvl.val

                if int(level)==0:

                    return True

            except:
                pass

        if text.lower()=="abstract":

            return True

        if re.match(r'^\d+\s+',text):

            return True

        return False


    def is_subheading(self,para):

        text=self.clean_text(para.text)

        if text=="":
            return False

        if re.match(r'^\d+(\.\d+)+\.?',text):

            return True

        if self.get_numbering(para):

            try:

                level=para._element.pPr.numPr.ilvl.val

                if int(level)>=1:

                    return True

            except:
                pass

        word_count=len(text.split())

        if word_count<=10:

            for run in para.runs:

                if run.bold:

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