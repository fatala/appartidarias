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
            response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/2016/71072/2/candidato/{}'.format(candidate.get('id')), timeout=3)
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

    stdout.write("\r\t\t\t\t%s " % (response_json.get('descricaoSexo')))
    stdout.flush()

    if 'FEM.' == response_json.get('descricaoSexo'):
        political_party, created = PoliticalParty.objects.get_or_create(
            initials=response_json.get('partido').get('sigla'),
            name=response_json.get('partido').get('nome'),
            number=response_json.get('partido').get('numero')
            )

        job_role, created = JobRole.objects.get_or_create(
            name=response_json.get('cargo').get('nome')
            )

        candidate, created = Candidate.objects.update_or_create(
            id_tse = response_json.get('id'),
            defaults= {
                'name' : response_json.get('nomeCompleto'),
                'name_ballot' : response_json.get('nomeUrna'),
                'number' : response_json.get('numero'),
                'job_role' : job_role,
                'political_party' : political_party,
                'coalition' : response_json.get('nomeColigacao'),
                'picture_url' : response_json.get('fotoUrl'),
                'budget_1t' : response_json.get('gastoCampanha1T'),
                'budget_2t' : response_json.get('gastoCampanha2T'),
                'birth_date' : response_json.get('dataDeNascimento'),
                'marital_status' : response_json.get('descricaoEstadoCivil'),
                'education' : response_json.get('grauInstrucao'),
                'job' : response_json.get('ocupacao'),
                'property_value' : response_json.get('totalDeBens')
            }
            )

    stdout.write("\r\t\t\t%s " % (j))
    stdout.flush()


class Command(BaseCommand):

    def handle(self, *args, **options):
        print ("FILL\t\t\tConsume")
        i = 0
        response = requests.get('http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2016/71072/2/13/candidatos').json()
        for candidate in response.get('candidatos')[:100]:  # Remove `[:100]` to import all
            i = i + 1
            stdout.write("\r%s" % i)
            stdout.flush()
            j = int(i)
            # thread_pool.apply_async(get, (candidate, j))  # async
            get(candidate, j)  # sync
        print ("\nDONE!")