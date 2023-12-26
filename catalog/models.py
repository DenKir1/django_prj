from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    activity = [(True, 'Опубликовано'),
                (False, 'Неопубликовано')]

    name = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена', **NULLABLE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Дата изменения', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Создатель', **NULLABLE)
    is_published = models.BooleanField(choices=activity, default=False, verbose_name='Статус')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

        permissions = [('set_published', 'Меняет статус продукта')]


class ContactData(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    message = models.TextField(verbose_name='Сообщение', **NULLABLE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='дата', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Version(models.Model):
    activity = [(True, 'Активно'),
                (False, 'Неактивно')]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.FloatField(**NULLABLE, verbose_name='Номер версии')
    name = models.CharField(max_length=50, verbose_name='Название версии')
    is_active = models.BooleanField(choices=activity, default=False, verbose_name='Активно')


    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'





