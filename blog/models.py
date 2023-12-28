from django.db import models

from catalog.models import NULLABLE
from users.models import User


class Blog(models.Model):
    topic = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=50, verbose_name='Адрес', **NULLABLE)
    message = models.TextField(verbose_name='Cодержимое', **NULLABLE)
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Статус', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры', **NULLABLE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Дата создания', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Создатель', **NULLABLE)
    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        #permissions = [('set_published', 'Меняет статус')]



