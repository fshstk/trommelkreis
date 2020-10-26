from django import template
from django.template.defaultfilters import date as django_date

from markdown import markdown

register = template.Library()


@register.filter
def filecount(session):
    filecount = len(session.files)
    if filecount == 0:
        return "Keine Einträge"
    elif filecount == 1:
        return "1 Eintrag"
    else:
        return "{} Einträge".format(filecount)


@register.filter
def dateformat(session):
    return session.date.strftime("%d.%m.%Y")


@register.filter
def duration(file):
    return "{:02d}:{:02d}".format(file.duration // 60, file.duration % 60)


@register.filter
def markdownify(text):
    return markdown(text) if text else ""


@register.filter
def month(session):
    # return session.date.strftime("%B")
    return django_date(session.date, "F")


@register.filter
def year(session):
    # return session.date.strftime("%Y")
    return django_date(session.date, "Y")
