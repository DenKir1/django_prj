from django.urls import path

from catalog.apps import MainappConfig
from catalog.views import *

app_name = MainappConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('category/', categories, name='categories'),
    path('create_prod/', create_prod, name='create_prod'),
    path('<int:pk>/category/', category_product, name='category_product'),
    path('<int:pk>/product/', product_to_view, name='product_to_view'),

]
