# templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})



@register.filter
def multiply(value, arg):
    return value * arg

from django import template

register = template.Library()

from django import template
register = template.Library()
@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):  # Check if field is a form field object
        return field.as_widget(attrs={'class': css_class})
    return field  # Return the field unchanged if it's not a form field object

