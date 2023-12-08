from django import template

from catalog.models import Product

register = template.Library()


@register.filter()
def mediapath(value):
    if value:
        return f'/media/{value}'
    return '/media/fruits.jpg'


@register.filter()
def cut_100(value):
    if value:
        return value[:100]
    return 'Нет описания.'


@register.simple_tag()
def mediapath(value):
    if value:
        return f'/media/{value}'
    return '/media/fruits.jpg'


@register.simple_tag()
def next_prod(value):

    prod_ids = [a.id for a in Product.objects.all()]
    if value in prod_ids:
        if value == max(prod_ids):
            return f'/{value}/product/'
        else:
            return f'/{prod_ids[prod_ids.index(value) + 1]}/product/'
    return f'/{max(prod_ids)}/product/'


@register.simple_tag()
def prev_prod(value):

    prod_ids = [a.id for a in Product.objects.all()]
    if value in prod_ids:
        if value == min(prod_ids):
            return f'/{value}/product/'
        else:
            return f'/{prod_ids[prod_ids.index(value) - 1]}/product/'
    return f'/{min(prod_ids)}/product/'


@register.simple_tag()
def button_p_prod(value):
    a_blu = "p-2 btn btn-outline-primary"
    a_gre = "p-2 btn btn-outline-secondary"
    prod_ids = [a.id for a in Product.objects.all()]
    if value == min(prod_ids):
        return a_gre
    return a_blu


@register.simple_tag()
def button_n_prod(value):
    a_blu = "p-2 btn btn-outline-primary"
    a_gre = "p-2 btn btn-outline-secondary"
    prod_ids = [a.id for a in Product.objects.all()]
    if value == max(prod_ids):
        return a_gre
    return a_blu

