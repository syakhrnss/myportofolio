from django import template

register = template.Library()


@register.filter
def split_sentences(value):
    return [item.strip() for item in value.split(".") if item.strip()]