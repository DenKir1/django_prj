from django.urls import path

from catalog.views import *

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('category/', categories, name='categories'),

]
