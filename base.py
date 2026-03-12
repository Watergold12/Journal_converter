import pdfplumber

with pdfplumber.open("ZEPHYR_VISHAL_AA_24AD124_REPORT.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        first_page = pdf.pages[i - 1]
        im = first_page.to_image(resolution=300)
        im.save(f'output_image_{i}.png')

