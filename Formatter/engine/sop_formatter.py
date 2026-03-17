from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

class SOPFormatter:

    def __init__(self, source_doc):

        self.source = source_doc

        # NEW DOCUMENT (important)
        self.doc = Document()

        self.section_count = 0

        self.sub_count = 0

        self.current_section = 0


    # GLOBAL FONT RULE
    def apply_font(self,para,size=12):

        for run in para.runs:

            run.font.name="Times New Roman"

            run.font.size=Pt(size)


    # TITLE RULE
    def add_title(self,text):

        para=self.doc.add_paragraph(text)

        self.apply_font(para,16)

        for run in para.runs:

            run.bold=True


    # AUTHOR RULE
    def add_author(self,text):

        para=self.doc.add_paragraph(text)

        self.apply_font(para,12)

        for run in para.runs:

            run.italic=True


    # SECTION RULE
    def add_heading(self,text):

        NON_NUMBERED=["abstract","conclusion"]

        if text.lower() in NON_NUMBERED:

            para=self.doc.add_paragraph(text)

            self.apply_font(para)

            for run in para.runs:

                run.bold=True

                run.font.color.rgb=RGBColor(0,0,255)

            return


        self.section_count+=1

        self.sub_count=0

        self.current_section=self.section_count

        para=self.doc.add_paragraph(
            str(self.section_count)+". "+text
        )

        self.apply_font(para)

        for run in para.runs:

            run.bold=True

            run.font.color.rgb=RGBColor(0,0,255)


    # SUBSECTION RULE
    def add_subheading(self,text):

        self.sub_count+=1

        number=str(self.current_section)+"."+str(self.sub_count)

        para=self.doc.add_paragraph(
            number+" "+text
        )

        self.apply_font(para)

        for run in para.runs:

            run.bold=True


    # PARAGRAPH RULE
    def add_paragraph(self,text):

        para=self.doc.add_paragraph(text)

        self.apply_font(para)

        para.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY


    # TABLE RULE
    def copy_tables(self):

        for table in self.source.tables:

            rows=len(table.rows)

            cols=len(table.columns)

            new_table=self.doc.add_table(rows,cols)

            # small tables stay in column
            if cols<4:

                pass

            # large tables full width
            else:

                section=self.doc.sections[0]

                cols_xml=section._sectPr.xpath('./w:cols')[0]

                cols_xml.set(qn('w:num'),'1')


            for i in range(rows):

                for j in range(cols):

                    text=table.cell(i,j).text

                    new_table.cell(i,j).text=text

                    for para in new_table.cell(i,j).paragraphs:

                        self.apply_font(para,10)


            # restore columns
            section=self.doc.sections[0]

            cols_xml=section._sectPr.xpath('./w:cols')[0]

            cols_xml.set(qn('w:num'),'2')


    # IMAGE RULE
    def copy_images(self):

        for shape in self.source.inline_shapes:

            width=shape.width

            if width>4000000:

                width=4000000

            # placeholder paragraph
            self.doc.add_paragraph("[IMAGE]")



    # COLUMN RULE
    def apply_double_column(self):

        section=self.doc.sections[0]

        cols=section._sectPr.xpath('./w:cols')[0]

        cols.set(qn('w:num'),'2')


    # MAIN ENGINE
    def build(self,detector):

        for para in self.source.paragraphs:

            text=para.text.strip()

            if text=="":

                continue


            block=detector.classify(para)


            if block=="TITLE":

                self.add_title(text)


            elif block=="AUTHOR":

                self.add_author(text)


            elif block=="HEADING":

                self.add_heading(text)


            elif block=="SUBHEADING":

                self.add_subheading(text)


            else:

                self.add_paragraph(text)


        self.copy_tables()

        self.copy_images()

        self.apply_double_column()


        return self.doc