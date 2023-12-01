
from catalog.models import Category, Product

Category.objects.create(name='Vegetables')
Category.objects.create(name='Fruits')
veg = Category.objects.get(name='Vegetables')
fru = Category.objects.get(name='Fruits')

Product.objects.create(name='Apple', price=100, category=fru)
Product.objects.create(name='Banana', price=100, category=fru)
Product.objects.create(name='Cucumber', price=100, category=veg)
Product.objects.create(name='Tomato', price=100, category=veg)
Product.objects.create(name='Onion', price=100, category=veg)
