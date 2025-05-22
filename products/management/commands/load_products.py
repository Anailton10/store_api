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
                category = row['category']
                price = row['price']
                stock = row['stock']
                description = ['description']

                self.stdout.write(self.style.NOTICE(name))

                try:
                    category = Categories.objects.filter(name=category).first()
                    if not category:
                        # Cadastrando os atores na model
                        Categories.objects.create(name=category)
                    Products.objects.create(
                        name=name,
                        category=category,
                        price=price,
                        stock=stock,
                        description=description
                    )
                except Exception as e:
                    self.stderr.write(f'Erro ao importar produto: {e}')
            self.stdout.write(self.style.SUCCESS(
                'PRODUTOS IMPORTADOS COM SUCESSO!!'))
