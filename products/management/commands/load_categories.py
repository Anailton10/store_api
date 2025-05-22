import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from products.models import Categories


# TODO: Alterar a logica para registrar as categorias do arquivo .csv
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo com atores',
        )

    def handle(self, *args, **options):
        # Nome do arquivo que o usuario vai passar no terminal
        file_name = options['file_name']

        # Abrindo o arquivo
        with open(file_name, 'r', encoding='utf-8') as file:
            # Lendo o arquivo
            reader = csv.DictReader(file)
            # percore cada linha do arquivo .csv
            for row in reader:
                name = row['name']  # pegando o nome

                self.stdout.write(self.style.NOTICE(name))

                # Cadastrando os atores na model
                Categories.objects.create(
                    name=name,
                )

        self.stdout.write(self.style.SUCCESS(
            'CATEGORIAS IMPORTADAS COM SUCESSO!!'))
