from django.shortcuts import render
from datetime import datetime


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name}({email})-{message}")

    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        date_ = datetime.now()
        print(f"[{date_}]\nName - {name}\nPhone - ({phone})\n{message}\n")
        with open("log.txt", 'a', encoding="utf-8") as log_:
            log_.write(f"[{date_}]\nName - {name}\nPhone - ({phone})\n{message}\n")
    return render(request, 'catalog/contacts.html')
