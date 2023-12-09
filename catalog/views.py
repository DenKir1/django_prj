from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Category, Product, ContactData


class CategoryListView(ListView):
    model = Category
    extra_context = {'title': 'Категории', }


class ContactDataCreateView(CreateView):
    model = ContactData
    fields = ('name', 'phone', 'message',)
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk'):
            queryset = queryset.filter(category=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.kwargs.get('pk'):
            category = Category.objects.get(pk=self.kwargs.get('pk'))
            context_data['title'] = f'Продукты категории - {category.name}',

        return context_data


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price',)
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price',)
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class ProductDetailView(DetailView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        product = Product.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'Продукт - {product.name}',

        return context_data
