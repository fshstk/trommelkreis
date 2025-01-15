from django import template
from django.template.defaultfilters import date as django_date

from markdown import markdown

register = template.Library()


@register.filter
def filecount(num_files):
    return "1 Eintrag" if num_files is 1 else f"{num_files} Einträge"


@register.filter
def dateformat(session):
    return session.date.strftime("%d.%m.%Y")


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
