import io
import os
import json
import pandas
import zipfile
import logging
import requests

from datetime import datetime
from utils import estados
from parse_tse_files import concat

from django.core.management.base import BaseCommand
from candidates.models import Candidate, PoliticalParty, JobRole

logger = logging.getLogger('mdb')


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
    print('fetch_candidate:', url)
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

        for row in df.iterrows():
            candidate = row[1]

            profile = fetch_2018_candidate(
                id_=candidate['SQ_CANDIDATO'],
                state=candidate['SG_UF'],
            )

            expenses = fetch_2018_candidate_expenses(
                estado=candidate['SG_UF'],
                candidate=candidate['SQ_CANDIDATO'],
                urna=candidate['NR_CANDIDATO'],
                cargo=candidate['CD_CARGO'],
                partido=candidate['NR_PARTIDO'],
            )

            print(json.dumps(profile, indent=4))

            if 'FEM.' == profile.get('descricaoSexo'):

                political_party, created = PoliticalParty.objects.get_or_create(
                    initials=profile.get('partido').get('sigla'),
                    name=profile.get('partido').get('nome'),
                    number=profile.get('partido').get('numero')
                )

                job_role, created = JobRole.objects.get_or_create(
                    name=profile.get('cargo').get('nome')
                )

                response_candidate, created = Candidate.objects.update_or_create(
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
                        'property_value' : profile.get('totalDeBens')
                    }
                )

                logger.debug('created: {}'.format(profile.get('nomeCompleto')))

                break
