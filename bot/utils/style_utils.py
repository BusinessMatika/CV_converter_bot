from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, RGBColor


def add_images_to_header_footer(
        document, header_image_path, footer_image_path
):
    """
    Add header and footer images to the document.
    """

    section = document.sections[0]

    # Add header
    header = section.header
    header_paragraph = (
        header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    )
    header_paragraph.clear()
    header_paragraph.add_run().add_picture(
        header_image_path, width=Cm(4.76), height=Cm(0.92)
    )

    # Add footer
    footer = section.footer
    footer_paragraph = (
        footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    )
    footer_paragraph.clear()
    footer_paragraph.add_run().add_picture(
        footer_image_path, width=Cm(3.56), height=Cm(1.09)
    )


def set_marker_style(paragraph, color, font_size):
    """
    Set the style for a paragraph marker with specified color and font size.
    """
    if isinstance(color, RGBColor):
        color = f"{color.red:02X}{color.green:02X}{color.blue:02X}"

    font_size_twips = str(int(font_size * 2))

    pPr = paragraph._element.get_or_add_pPr()
    numPr = pPr.find(qn('w:numPr')) or OxmlElement('w:numPr')
    pPr.append(numPr)

    rPr = pPr.find(qn('w:rPr')) or OxmlElement('w:rPr')
    pPr.append(rPr)

    color_element = rPr.find(qn('w:color')) or OxmlElement('w:color')
    rPr.append(color_element)
    color_element.set(qn('w:val'), color)

    size_element = rPr.find(qn('w:sz')) or OxmlElement('w:sz')
    rPr.append(size_element)
    size_element.set(qn('w:val'), font_size_twips)
