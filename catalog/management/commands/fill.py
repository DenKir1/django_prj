
from django.conf import settings
from django.db import ProgrammingError, IntegrityError
from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options) -> None:
        Category.objects.all().delete()
        Product.objects.all().delete()

        fixtures_path = 'data.json'

        try:
            call_command('loaddata', fixtures_path)
        except ProgrammingError:
            pass
        except IntegrityError as e:
            self.stdout.write(f'Красный? - Invalid fixtures: {e}', self.style.NOTICE)
        else:
            self.stdout.write('Зеленый - Successfully', self.style.SUCCESS)
