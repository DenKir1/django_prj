from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_categories_from_cache():
    #Проверил, без условия на CACHE_ENABLED тоже работает, так как в settings есть проверка локации
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set('category_list', category_list, 3600)
    else:
        category_list = Category.objects.all()
    return category_list
