from django import template
from django.shortcuts import reverse

register = template.Library()

# These are the most common
# tags you can find in a navbar.

# Complete this list the icon
# that you want if you wish to
# implement additional ones.

ICONS = {
    'home': 'fa fa-home',
    'search': 'fa fa-search',
    'login': 'fa fa-sign-in',
    'signin': 'fa fa-sign-in',
    'account': 'fa fa-person',
    'profile': 'fa fa-person',
    'logout': 'fa fa-sign-out',
    'signout': 'fa fa-sign-out',
    'cart': 'fa fa-shopping-cart',
    'checkout': 'fa fa-shopping-cart'
}


def normalize_url(url):
    return url.lower()


@register.inclusion_tag('project_components/navs/links/icon.html')
def icon_links(*urls):
    context = {
        'urls': []
    }
    for url in urls:
        try:
            icon = ICONS[normalize_url(url)]
        except KeyError:
            icon = 'fa fa-ban red'
        else:
            context['urls'].append(
                (icon, reverse(normalize_url(url)))
            )
    return context


@register.inclusion_tag('project_components/navs/links/text.html')
def text_links(*urls):
    context = {
        'urls': []
    }
    for url in urls:
        context['urls'].append(
            (url, reverse(normalize_url(url)))
        )
    return context
