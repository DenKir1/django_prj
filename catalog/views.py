from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

from catalog.models import Category, Product, ContactData


def home(request):
    context = {
        'value_one': Product.objects.all()[:5]
    }
    print('\n', Product.objects.all()[:5], '\n')
    
    return render(request, 'catalog/home.html', context=context)


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
        'value_one': ContactData.objects.all()
    }
    return render(request, 'catalog/contacts.html', context=context)


def categories(request):
    context = {
        'value_one': Category.objects.all()
    }
    return render(request, 'catalog/category.html', context=context)
