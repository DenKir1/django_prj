from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    is_verify = models.BooleanField(default=False, verbose_name='Верифицировано')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Verify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    verify_code = models.CharField(max_length=15, verbose_name='Код верификации', **NULLABLE)
    verify_pass = models.CharField(max_length=15, verbose_name='Проверочный код', **NULLABLE)


    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Верификация'
        verbose_name_plural = 'Верификации'
