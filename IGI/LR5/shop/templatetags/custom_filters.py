from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """Конвертирует URL YouTube в embed-формат"""
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        return f"https://www.youtube.com/embed/{match.group(1)}"
    return url