import csv

from django.core.management.base import BaseCommand

from products.models import Categories, Products


# TODO: Alterar a logica para registrar os productos do arquivo .csv
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo com atores',
        )

    def handle(self, *args, **options):
        # Nome do arquivo que o usuario vai passar
        file_name = options['file_name']

        # Abrindo o arquivo
        with open(file_name, 'r', encoding='utf-8') as file:
            # Lendo o arquivo
            reader = csv.DictReader(file)
            # percore cada linha do arquivo .csv
            for row in reader:
                name = row['name']  # pegando o nome
                category_name = row['category']
                price = float(row['price'])
                stock = int(row['stock'])
                description = row['description']

                self.stdout.write(self.style.NOTICE(name))

                try:
                    # Primeiro, obtém ou cria a categoria
                    category = Categories.objects.filter(name=category_name).first()

                    # Depois, filtra o produto usando o objeto de categoria
                    product = Products.objects.filter(name=name, category=category).first()

                    if not category:
                        category = Categories.objects.create(name=category_name)
                    if product is None:
                        Products.objects.create(
                            name=name,
                            category=category,
                            price=price,
                            stock=stock,
                            description=description
                        )
                    else:
                        product.stock += stock
                        product.save()
                except Exception as e:
                    self.stderr.write(f'Erro ao importar produto: {e}')
            self.stdout.write(self.style.SUCCESS(
                'PRODUTOS IMPORTADOS COM SUCESSO!!'))
