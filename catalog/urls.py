from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import MainappConfig
from catalog.views import *

app_name = MainappConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('category/<int:pk>/', ProductListView.as_view(), name='product'),
    path('contacts/', ContactDataCreateView.as_view(), name='contacts'),
    path('category/', CategoryListView.as_view(), name='categories'),
    path('product/create/', never_cache(ProductCreateView.as_view()), name='create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('<int:pk>/product/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('version/create/', never_cache(VersionCreateView.as_view()), name='create_version'),
    path('version/update/', VersionUpdateView.as_view(), name='update_version'),

]
