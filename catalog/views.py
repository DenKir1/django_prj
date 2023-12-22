from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ContactDataForm, ProductForm, VersionForm
from catalog.models import Category, Product, ContactData, Version


class CategoryListView(ListView):
    model = Category
    extra_context = {'title': 'Категории', }


class ContactDataCreateView(CreateView):
    model = ContactData
    form_class = ContactDataForm
    success_url = reverse_lazy('catalog:home')


class ContactDataUpdateView(UpdateView):
    model = ContactData
    form_class = ContactDataForm
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
            context_data['title'] = f'Продукты категории - {category.name}'

        for product in context_data['object_list']:
            version = product.version_set.filter(is_active=True).first()
            if version:
                product.number = version.number
            else:
                product.number = 'Отсутствует'
        return context_data


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST)
        else:
            context_data['formset'] = ProductFormset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


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


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:home')


class VersionUpdateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:home')