from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ContactDataForm, ProductForm, VersionForm, ModeratorForm
from catalog.models import Category, Product, ContactData, Version
from catalog.services import get_categories_from_cache


class CategoryListView(ListView):
    model = Category
    extra_context = {'title': 'Категории', }

    def get_object(self):
        #задание с кешированием категорий
        obj = get_categories_from_cache()
        return obj


class ContactDataCreateView(LoginRequiredMixin, CreateView):
    model = ContactData
    form_class = ContactDataForm
    success_url = reverse_lazy('catalog:home')


class ContactDataUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactData
    form_class = ContactDataForm
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product
    #permission_required = 'catalog.set_published'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('pk'):
            queryset = queryset.filter(category=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.kwargs.get('pk'):
            # задание с кешированием категорий
            category = get_categories_from_cache()
            category = category.get(pk=self.kwargs.get('pk'))
            context_data['title'] = f'Продукты категории - {category.name}'
            #print(context_data)
        for product in context_data['object_list']:
            version = product.version_set.filter(is_active=True).first()
            if version:
                product.number = version.number
            else:
                product.number = 'Отсутствует'
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
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
        self.object.owner = self.request.user
        self.object.save()
        #print(self.object.__dict__)
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    #form_class = ProductForm
    #permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        permi = ('catalog.change_product',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permi):
            return True
        return self.handle_no_permission()

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

    def get_form_class(self):
        if self.request.user.groups.filter(name='Moderator'):
            return ModeratorForm
        else:
            return ProductForm


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product

    #permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        permi = ('catalog.delete_product',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permi):
            return True
        return self.handle_no_permission()


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


class VersionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        permi = ('catalog.add_version',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permi):
            return True
        return self.handle_no_permission()


class VersionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        permi = ('catalog.change_version',)
        _user = self.request.user
        _instance = self.get_object()
        if _user == _instance.owner or _user.has_perms(permi):
            return True
        return self.handle_no_permission()
