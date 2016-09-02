# coding: utf-8

from __future__ import print_function

from sys import stdout
from django.core.management.base import BaseCommand
from multiprocessing.pool import ThreadPool
from candidates.models import Candidate, PoliticalParty, JobRole

import logging
import requests

logger = logging.getLogger('mdb')


def get(candidate, j):
    while range(6):
        try:
            response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/2016/71072/2/candidato/{}'.format(candidate.get('id')))
        except:
            print('retrying to get details on candidate', candidate.get('id'))
            continue

        try:
            response_json = response.json()
        except:
            print('Failed to decode json. raw response:', response.text)
            continue
        else:
            break

    response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/2016/71072/2/candidato/{}'.format(candidate.get('id')))
    response_json = response.json()
    stdout.write("\r\t\t\t\t%s " % (response_json.get('descricaoSexo')))
    stdout.flush()

    if 'FEM.' == response_json.get('descricaoSexo'):
        political_party, created = PoliticalParty.objects.get_or_create(
            initials=response_json.get('partido').get('sigla'),
            name=response_json.get('partido').get('nome'),
            number=response_json.get('partido').get('numero'),
            )

        job_role = JobRole.objects.get(pk=3)

        candidate_to_save = Candidate()

        candidate_to_save.id_tse = response_json.get('id')
        candidate_to_save.name = response_json.get('nomeCompleto')
        candidate_to_save.name_ballot = response_json.get('nomeUrna')
        candidate_to_save.number = response_json.get('numero')
        candidate_to_save.job_role = job_role
        candidate_to_save.political_party = political_party
        candidate_to_save.coalition = response_json.get('nomeColigacao')
        candidate_to_save.picture_url = response_json.get('fotoUrl')
        candidate_to_save.budget_1t = response_json.get('gastoCampanha1T')
        candidate_to_save.budget_2t = response_json.get('gastoCampanha2T')
        candidate_to_save.birth_date = response_json.get('dataDeNascimento')
        candidate_to_save.marital_status = response_json.get('descricaoEstadoCivil')
        candidate_to_save.education = response_json.get('grauInstrucao')
        candidate_to_save.job = response_json.get('ocupacao')
        candidate_to_save.property_value = response_json.get('totalDeBens')

        candidate_to_save.save()

    stdout.write("\r\t\t\t%s " % (j))
    stdout.flush()


class Command(BaseCommand):
    Candidate.objects.all().delete()

    def handle(self, *args, **options):
        thread_pool = ThreadPool(processes=30)
        print ("FILL\t\t\tConsume")
        i = 0
        response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2016/71072/2/13/candidatos').json()
        for candidate in response.get('candidatos'):  # Remove `[:100]` to import all
            i = i + 1
            stdout.write("\r%s" % i)
            stdout.flush()
            j = int(i)
            # thread_pool.apply_async(get, (candidate, j))  # async
            get(candidate, j)  # sync
        thread_pool.close()
        thread_pool.join()
        print ("\nDONE!")