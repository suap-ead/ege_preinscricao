import datetime
import csv
from django.core.management.base import BaseCommand
# from django.conf import settings
# from sc4py.env import env
from solicitacao.models import Chamada, Selecionado
from solicitacao.importers import selecionado_csv_importer


class Command(BaseCommand):
    help="Importa os selecionados contidos em um arquivo CSV"

    def add_arguments(self, parser):
        parser.add_argument('chamada_id', type=int)

    def handle(self, *args, **options):
        selecionado_csv_importer(options['chamada_id'], 'selecionados.csv')
