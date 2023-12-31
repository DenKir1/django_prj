from django.contrib import admin
from catalog.models import Product, Category, ContactData, Version


# admin.site.register(Product)
# admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    list_filter = ['category']
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ContactData)
class ContactDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'message', 'created_at')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'number', 'name', 'is_active')
    list_filter = ['product', 'is_active']
    search_fields = ('product', 'name')
