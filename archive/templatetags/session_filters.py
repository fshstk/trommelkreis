from django import template

register = template.Library()


@register.filter
def filecount_string(files):
    filecount = len(files)
    if filecount is 0:
        return "Keine Einträge"
    elif filecount is 1:
        return "1 Eintrag"
    else:
        return "{} Einträge".format(filecount)


@register.filter
def date_string(date):
    return date.strftime("%d.%m.%Y")
