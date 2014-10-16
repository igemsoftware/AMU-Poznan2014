"""
.. module:: shweb.designer.templatetags
   :platform: Unix, Windows
   :synopsis: Module which contains custom template tags for sh-miR designer
"""

from django import template

from designer.utils import ShmirDesigner as shmir

register = template.Library()


@register.simple_tag
def get_pdf_url(pdf_dirs):
    return shmir.build_pdf_url(pdf_dirs)
