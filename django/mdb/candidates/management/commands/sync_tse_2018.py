import io
import os
import json
import time
import pandas
import zipfile
import logging
import requests

from datetime import datetime
from utils import estados, store_json

from django.core.management.base import BaseCommand
from candidates.models import Candidate, PoliticalParty, JobRole, Expenses

logger = logging.getLogger('mdb')


def concat(files):
    """
    Concat TSE files into a single pandas.DataFrame
    """
    return pandas.concat([
        pandas.read_csv(
            pandas.compat.BytesIO(file_),
            encoding='latin1',
            sep=';',
        )
        for _, file_ in files.items()
    ])


def url_patterns():
    base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/'
    download = {
        'candidatos_lista': 'consulta_cand/consulta_cand_{ano}.zip',
        # 'candidatos_bens': 'bem_candidato/bem_candidato_{ano}.zip',
        # 'candidatos_coligacoes': 'consulta_coligacao/consulta_coligacao_{ano}.zip',
        # 'candidatos_vagas': 'consulta_vagas/consulta_vagas_{ano}.zip',
        # 'candidatos_cassacoes': 'motivo_cassacao/motivo_cassacao_{ano}.zip',
        # 'eleitorado_perfil': 'perfil_eleitorado/perfil_eleitorado_{ano}.zip',
        # 'eleitorado_deficiencia': 'perfil_eleitor_deficiente/perfil_eleitor_deficiencia_{ano}.zip',
        # 'votacao_zona_nominal': 'votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip',
        # 'votacao_zona_partido': 'votacao_partido_munzona/votacao_partido_munzona_{ano}.zip',
        # 'votacao_detalhe_zona': 'detalhe_votacao_munzona/detalhe_votacao_munzona_{ano}.zip',
        # 'pesquisa_lista': 'pesquisa_eleitoral/pesquisa_eleitoral_{ano}.zip',
        # 'pesquisa_notasfiscais': 'pesquisa_eleitoral/nota_fiscal_{ano}.zip',
        # 'pesquisa_questionarios': 'pesquisa_eleitoral/questionario_pesquisa_{ano}.zip',
        # 'pesquisa_locais': 'pesquisa_eleitoral/bairro_municipio_{ano}.zip',
    }

    return {kind: base + path for kind, path in download.items()}


def list_zip_files(anos=None):
    """
    Lista possiveis zip files para download
    """
    if anos==None:
        anos = [2018 - 2*x for x in range(1)]
    urls = {}
    for label, url in url_patterns().items():
        for ano in anos:
            if "{estado}" in url:
                for estado in estados:
                    params = {
                        'ano': ano,
                        'estado': estado,
                        'label': label,
                    }
                    label_new = '{label}_{ano}_{estado}'.format(**params)
                    url_new = url.format(**params)
                    urls[label_new] = url_new
            else:
                params = {
                    'ano': ano,
                    'label': label,
                }
                label_new = '{label}_{ano}'.format(**params)
                url_new = url.format(**params)
                urls[label_new] = url_new
    return urls


def fetch_2018_candidate_expenses(**kwargs):
    host = 'http://divulgacandcontas.tse.jus.br/divulga/rest/v1/prestador/consulta/2022802018/2018/'
    path = '{estado}/{cargo}/{partido}/{urna}/{candidate}'
    url = host + path.format(**kwargs)
    logger.debug(f'fetch_expenses: {url}')
    return requests.get(url).json()


def fetch_2018_candidate(id_, state, year='2018', election='2022802018'):
    host = 'http://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/'
    path = '{year}/{state}/{election}/candidato/{id_}'
    url = host + path.format(
        id_=id_,
        state=state,
        election=election,
        year=year,
    )
    logger.debug(f'fetch_candidate: {url}')
    return requests.get(url).json()


def download_file(base_folder, label, url):
    """
    Download and save file
    """
    resp = requests.get(url)
    if resp.ok:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zip_ref:
            return {
                name: zip_ref.read(name)
                for name in zip_ref.namelist()
                if name.split('.')[-1] == 'csv'
            }


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ano = 2018
        logger.debug('Downloading TSE {ano}...'.format(ano=ano))
        folder = os.path.abspath('./arquivos')
        files = list_zip_files()
        for a,b in files.items():
            print(a, b)
        for label, url in files.items():
            download = download_file(folder, label, url)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.debug('[{}] Downloaded {}'.format(now, label))

        path = os.path.join(
            folder,
            'candidatos/list/{ano}/*.csv'.format(ano=ano)
        )
        df = concat(download)
        logger.debug('total candidates: {shape}'.format(shape=df.shape))

        current_time = int(time.time())

        for row in df.iterrows():

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

                if 'FEM.' == profile.get('descricaoSexo'):

                    political_party, created = PoliticalParty.objects.get_or_create(
                        initials=profile.get('partido').get('sigla'),
                        name=profile.get('partido').get('nome'),
                        number=profile.get('partido').get('numero')
                    )

                    job_role, created = JobRole.objects.get_or_create(
                        name=profile.get('cargo').get('nome')
                    )

                    candidate_model, created = Candidate.objects.update_or_create(
                        number=profile.get('numero'),
                        defaults= {
                            'id_tse': profile.get('id'),
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
                            'property_value' : profile.get('totalDeBens')
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
                logger.exception('parsing candidate {profile.get("nomeCompleto")}')
