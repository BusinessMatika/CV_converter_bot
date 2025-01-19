from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.text.run import Run

from app.common.enums import Style


def set_font(run: Run, font_name: str, font_size: int) -> None:
    """
    Apply the specified font and size to a run.
    """

    run.font.name = font_name
    run.font.size = Pt(font_size)

    # Ensure the font is applied to both Western and East Asian characters
    r = run._element
    rPr = r.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        r.append(rPr)

    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)

    font_attrs = ['ascii', 'hAnsi', 'eastAsia', 'cs']
    [rFonts.set(qn(f'w:{attr}'), font_name) for attr in font_attrs]


def apply_font_style(
        run: Run, font_size: int,
        font_name: str, color: RGBColor
) -> None:
    """
    Apply font style with the specified size and color to a run.
    """
    run.font.color.rgb = color
    set_font(run, font_name, font_size)


def set_raleway(run: Run, font_size: int) -> None:
    """
    Apply Raleway font to a run with a specified size and grey color.
    """
    apply_font_style(
        run, font_size, Style.RALEWAY.value, Style.GREY.value
    )


def set_raleway_medium(run: Run, font_size: int) -> None:
    """
    Apply Raleway Medium font to a run with a specified size and black color.
    """

    apply_font_style(
        run, font_size, Style.RALEWAY_MEDIUM.value, Style.BLACK.value
    )
