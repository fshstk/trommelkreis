from django import template

register = template.Library()


@register.filter
def duration_to_string(numseconds):
    return "{:02d}:{:02d}".format(numseconds // 60, numseconds % 60)
