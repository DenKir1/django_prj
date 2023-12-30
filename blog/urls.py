from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import *

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='main'),
    path('<int:pk>/detail/', BlogDetailView.as_view(), name='detail'),
    path('create/', never_cache(BlogCreateView.as_view()), name='create'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),

]
