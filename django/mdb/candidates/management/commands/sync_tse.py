# coding: utf-8
from sys import stdout
from django.core.management.base import BaseCommand
from multiprocessing.pool import ThreadPool
from candidates.models import Candidate, PoliticalParty

import logging
import requests

logger = logging.getLogger('mdb')


def get(candidate, j):
    response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/2016/71072/2/candidato/{}'.format(candidate.get('id')))
    response_json = response.json()
    stdout.write("\r\t\t\t\t%s " % (response_json.get('descricaoSexo')))
    stdout.flush()
    if 'FEM.' == response_json.get('descricaoSexo'):
        political_party, created = PoliticalParty.objects.get_or_create(initials=candidate.get('partido').get('sigla'))

        candidate_to_save = Candidate()
        candidate_to_save.political_party = political_party
        candidate_to_save.name = candidate.get('nomeCompleto')
        candidate_to_save.save()

    stdout.write("\r\t\t\t%s " % (j))
    stdout.flush()


class Command(BaseCommand):

    def handle(self, *args, **options):
        thread_pool = ThreadPool(processes=30)
        print "FILL\t\t\tConsume"
        i = 0
        response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2016/71072/2/13/candidatos').json()
        for candidate in response.get('candidatos'):  # Remove `[:100]` to import all
            i = i + 1
            stdout.write("\r%s" % i)
            stdout.flush()
            j = int(i)
            thread_pool.apply_async(get, (candidate, j))  # async
            # get(candidate, j)  # sync
        thread_pool.close()
        thread_pool.join()
        print "\nDONE!"
