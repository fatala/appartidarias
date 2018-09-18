import os
import json
import time
import logging
import requests

from utils import (
    store_json,
    concat,
    download_file,
    fetch_2018_candidate_expenses,
    fetch_2018_candidate,
)

from django.conf import settings
from django.core.management.base import BaseCommand
from candidates.models import Candidate, PoliticalParty, JobRole, Expenses

logger = logging.getLogger('mdb')
current_time = int(time.time())


def fetch_serial(df):
    for row in df.iterrows():
        process_candidate(row)


def fetch_parallel(df):

    from multiprocessing.dummy import Pool as ThreadPool
    pool = ThreadPool(settings.THREADS)
    pool.map(process_candidate, df.iterrows())


def process_candidate(row):
    try:

        candidate = row[1]

        profile = fetch_2018_candidate(
            id_=candidate['SQ_CANDIDATO'],
            state=candidate['SG_UF'],
        )

        store_json(
            'profile_{id_}_{partido}_{uf}_{time}'.format(
                id_=candidate['SQ_CANDIDATO'],
                partido=candidate['NR_PARTIDO'],
                uf=candidate['SG_UF'],
                time=current_time,
            ),
            profile,
        )

        expenses = fetch_2018_candidate_expenses(
            estado=candidate['SG_UF'],
            candidate=candidate['SQ_CANDIDATO'],
            urna=candidate['NR_CANDIDATO'],
            cargo=candidate['CD_CARGO'],
            partido=candidate['NR_PARTIDO'],
        )

        store_json(
            'expenses_{id_}_{partido}_{uf}_{time}'.format(
                id_=candidate['SQ_CANDIDATO'],
                partido=candidate['NR_PARTIDO'],
                uf=candidate['SG_UF'],
                time=current_time,
            ),
            expenses,
        )

        gender = 'F' if 'FEM.' == profile.get('descricaoSexo') else 'M'

        political_party, created = PoliticalParty.objects.get_or_create(
            number=profile.get('partido').get('numero'),
            defaults = {
                'initials': profile.get('partido').get('sigla').upper(),
                'name': profile.get('partido').get('nome'),
            }
        )

        job_role, created = JobRole.objects.get_or_create(
            name=profile.get('cargo').get('nome'),
            code=candidate['CD_CARGO'],
        )

        if not created and job_role.code is None:
            job_role.code = candidate['CD_CARGO']
            job_role.save()

        candidate_model, created = Candidate.objects.update_or_create(
            id_tse=profile.get('id'),
            defaults={
                'year': '2018',
                'gender': gender,
                'number': profile.get('numero'),
                'name' : profile.get('nomeCompleto'),
                'name_ballot' : profile.get('nomeUrna'),
                'job_role' : job_role,
                'political_party' : political_party,
                'coalition' : profile.get('nomeColigacao'),
                'picture_url' : profile.get('fotoUrl'),
                'budget_1t' : profile.get('gastoCampanha1T'),
                'budget_2t' : profile.get('gastoCampanha2T'),
                'birth_date' : profile.get('dataDeNascimento'),
                'marital_status' : profile.get('descricaoEstadoCivil'),
                'education' : profile.get('grauInstrucao'),
                'job' : profile.get('ocupacao'),
                'state': profile.get('sgUe') or candidate['SG_UF'],
                'property_value' : profile.get('totalDeBens'),
                'email': candidate['NM_EMAIL'],
            }
        )

        try:
            expenses = Expenses.objects.create(
                candidate=candidate_model,
                received=expenses['dadosConsolidados']['totalRecebido'],
                paid=expenses['despesas']['totalDespesasPagas'],
            )
            logger.debug('got expenses: {}'.format(profile.get('nomeCompleto')))
        except Exception:
            logger.debug('missing expenses: {}'.format(profile.get('nomeCompleto')))

        logger.debug('created: {}'.format(profile.get('nomeCompleto')))

    except Exception:
        logger.exception(f'creating candidate from endpoint')

        try:
            gender = 'F' if 4 == candidate['CD_GENERO'] else 'M'

            political_party, created = PoliticalParty.objects.get_or_create(
                number=candidate['NR_PARTIDO'],
                defaults = {
                    'initials': candidate['SG_PARTIDO'],
                    'name': candidate['NM_PARTIDO'],
                }
            )

            job_role, created = JobRole.objects.get_or_create(
                name=candidate['DS_CARGO'],
                code=candidate['CD_CARGO'],
            )

            birth = '-'.join(reversed(candidate['DT_NASCIMENTO'].split('/')))

            candidate_model, created = Candidate.objects.update_or_create(
                id_tse=candidate['SQ_CANDIDATO'],
                defaults={
                    'year': '2018',
                    'gender': gender,
                    'number': candidate['NR_CANDIDATO'],
                    'name' : candidate['NM_CANDIDATO'],
                    'name_ballot' : candidate['NM_URNA_CANDIDATO'],
                    'job_role' : job_role,
                    'political_party' : political_party,
                    'coalition' : candidate['NM_COLIGACAO'],
                    'birth_date' : birth,
                    'marital_status' : candidate['DS_ESTADO_CIVIL'],
                    'education' : candidate['DS_GRAU_INSTRUCAO'],
                    'job' : candidate['DS_OCUPACAO'],
                    'state': candidate['SG_UF'],
                    'email': candidate['NM_EMAIL'],
                }
            )

        except Exception:
            logger.exception('creating candidates from df')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ano = 2018
        logger.debug('Downloading TSE {ano}...'.format(ano=ano))
        base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip' # noqa
        url = base.format(ano=ano)
        download = download_file(url)
        df = concat(download)
        logger.debug('total candidates: {shape}'.format(shape=df.shape))

        fetch_parallel(df)

        logger.debug(
            f'candidates: {Candidate.objects.count()} expected: {df.shape[0]}'
        )
