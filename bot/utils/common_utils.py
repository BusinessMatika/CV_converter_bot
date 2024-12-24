from common.enums import Style

from .style_utils import set_marker_style


def add_text(paragraph, text, font_style, font_size, new_line=False):
    """Adds text to paragraph with certain font style and size."""
    run = paragraph.add_run(text)
    font_style(run, font_size=font_size)
    if new_line:
        paragraph.add_run('\n')
    return run


def add_bullet_list(paragraph, items, font_style, font_size, bullet_color):
    """Adds bulleted list."""
    for item in items:
        bullet_paragraph = paragraph.add_paragraph(style=Style.BULLET.value)
        set_marker_style(bullet_paragraph, bullet_color, font_size)
        bullet_text = bullet_paragraph.add_run(item)
        font_style(bullet_text, font_size=font_size)


def add_section(
        document, title, content,
        title_style, content_style,
        font_size=Style.NINE.value
):
    """Add section with header and data."""
    paragraph = document.add_paragraph()
    if title:
        add_text(paragraph, title, title_style, font_size=Style.TEN.value)
    if content:
        add_text(paragraph, content, content_style, font_size)
    return paragraph
