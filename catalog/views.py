from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from catalog.models import Category, Product, ContactData


def home(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Продукты',
    }
    print('\n', Product.objects.all()[:5], '\n')
    
    return render(request, 'catalog/home.html', context=context)


def base_page(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Продукты',
    }

    return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        date_ = datetime.now()
        contact = ContactData.objects.create(name=name, phone=phone, message=message, date_of=date_).save()
        print(contact)
        with open("log.txt", 'a', encoding="utf-8") as log_:
            log_.write(f"[{date_}]\nName - {name}\nPhone - ({phone})\n{message}\n")

    context = {
        'object_list': ContactData.objects.all(),
        'title': 'Контакты',
    }
    return render(request, 'catalog/contacts.html', context=context)


def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Категории',
    }
    return render(request, 'catalog/category.html', context=context)


def category_product(request, pk):
    cat_prod = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category=pk),
        'title': f'Продукты категории {cat_prod.name}',
    }
    return render(request, 'catalog/home.html', context=context)


def product_to_view(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {
        'object': prod,
        'title': f'Продукт {prod.name}',
    }
    return render(request, 'catalog/includes/inc_product.html', context=context)


def create_prod(request):
    if request.method == 'POST':
        category = Category.objects.get(pk=request.POST.get('category'))

        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.POST.get('image')
        price = request.POST.get('price')

        product = Product.objects.create(name=name, description=description, image=image, price=price, category=category).save()
    context = {
        'object_list': Product.objects.all(),
        'title': 'Продукт',
    }
    return render(request, 'catalog/create_prod.html')

