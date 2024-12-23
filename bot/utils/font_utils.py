from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from common.enums import Style  # изменить импорт


def check_fonts():
    """
    Check whether user has all the required fonts installed.
    """

    from tkinter import Tk, font
    root = Tk()
    available_fonts = font.families()
    root.destroy()
    missing_fonts = [
        f'"{font}"' for font in Style.AVAILABLE_FONTS.value
        if font not in available_fonts
    ]

    if missing_fonts:
        raise RuntimeError(
            f'Missing fonts: {", ".join(missing_fonts)} \n'
            'Please download Raleway fonts from '
            'https://fonts.google.com/specimen/Raleway '
            f'and install required .tff files from /static folder: '
        )


def set_font(run, font_name, font_size):
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


def apply_font_style(run, font_size, font_name, color):
    """
    Apply font style with the specified size and color to a run.
    """

    check_fonts()
    run.font.color.rgb = color
    set_font(run, font_name, font_size)


def set_raleway(run, font_size):
    """
    Apply Raleway font to a run with a specified size and grey color.
    """

    apply_font_style(
        run, font_size, Style.RALEWAY.value, Style.GREY.value
    )


def set_raleway_medium(run, font_size):
    """
    Apply Raleway Medium font to a run with a specified size and black color.
    """

    apply_font_style(
        run, font_size, Style.RALEWAY_MEDIUM.value, Style.BLACK.value
    )
