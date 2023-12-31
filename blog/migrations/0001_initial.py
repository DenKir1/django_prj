# Generated by Django 4.2.7 on 2023-12-07 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('slug', models.CharField(blank=True, max_length=50, null=True, verbose_name='Адрес')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Cодержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Статус')),
                ('views_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='Просмотры')),
                ('date_of', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
