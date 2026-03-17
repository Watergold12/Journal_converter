import re

class StructureDetector:

    SECTION_KEYWORDS = {
        "abstract",
        "introduction",
        "review of literature",
        "literature review",
        "methodology",
        "result and discussion",
        "results and discussion",
        "conclusion",
        "acknowledgements",
        "acknowledgments",
        "references",
    }

    def clean_text(self,text):

        text=text.strip()

        if len(text)==0:
            return ""

        if re.match(r'^[^A-Za-z0-9]+$',text):

            return ""

        return text


    def normalize_text(self,text):

        text=self.clean_text(text)

        if text=="":
            return ""

        text=re.sub(r"\s+"," ",text)

        return text.strip()


    def get_numbering_level(self,para):

        try:

            if para._element.pPr is None:
                return None

            numPr=para._element.pPr.numPr

            if numPr is None:
                return None

            level=numPr.ilvl.val

            return int(level)

        except:
            return None


    def get_numbering(self,para):

        return self.get_numbering_level(para) is not None


    def has_bold_run(self,para):

        for run in para.runs:

            if run.bold:

                return True

        return False


    def has_font_size_above(self,para,threshold):

        for run in para.runs:

            if run.font.size and run.font.size.pt:

                if run.font.size.pt>threshold:

                    return True

        return False


    def is_title(self,para):

        text=self.normalize_text(para.text)

        if text=="":
            return False

        return self.has_font_size_above(para,12)


    def is_author(self,para):

        text=self.normalize_text(para.text)

        if text=="":
            return False

        if "," not in text:
            return False

        for run in para.runs:

            if run.italic:

                return True

        return False


    def is_heading(self,para):

        text=self.normalize_text(para.text)

        if text=="":
            return False

        normalized=text.lower().rstrip(":")
        word_count=len(text.split())

        if normalized in self.SECTION_KEYWORDS:

            return True

        # Uppercase short lines are very likely section headings.
        if text.isupper() and word_count<=8 and ":" not in text:

            return True

        # Explicit "1 INTRODUCTION" or "1. INTRODUCTION" style.
        if re.match(r'^\d+[\.\)]?\s+[A-Za-z]',text):

            if word_count<=12 and ":" not in text and not text.endswith("."):

                return True

        return False


    def is_subheading(self,para):

        text=self.normalize_text(para.text)

        if text=="":
            return False

        if re.match(r'^\d+\.\d+(\.\d+)*\.?\s+',text):

            return True

        level=self.get_numbering_level(para)

        if level is not None:

            try:

                if int(level)>=1:

                    if len(text.split())<=14:

                        return True

            except:
                pass

        word_count=len(text.split())

        if word_count<=10:

            if text.isupper():
                return False

            if self.has_bold_run(para):

                if not text.endswith("."):

                    return True

        return False


    def is_bullet(self,para):

        text=self.normalize_text(para.text)

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
