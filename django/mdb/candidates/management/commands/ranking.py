# coding: utf-8
import os
import glob
import json
import boto3
import logging

import pandas as pd
from django.core.management.base import BaseCommand
from utils import s3_resource, concat, download_file

logger = logging.getLogger('mdb')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        base = 'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip'

        download = download_file(base.format(ano=2018))
        df_cand = concat(download)

        bucket = s3_resource.Bucket('appartidarias')

        df_cand['timestamp'] = 0
        df_cand['received_party'] = None
        df_cand['received_total'] = None

        logger.debug('fetching candidates expenses')
        fetch_dict = {}
        for obj in bucket.objects.all():
            keys = obj.key.split('_')
            if keys[1] not in fetch_dict or keys[-1] > fetch_dict[keys[1]].key.split('_')[-1]:
                fetch_dict[keys[1]] = obj

        for _, obj in fetch_dict.items():
            keys = obj.key.split('_')
            data = json.loads(obj.get()['Body'].read())
            sq_candidato = int(keys[1])
            timestamp = int(keys[-1])
            print(keys)
            assert sum(df_cand.SQ_CANDIDATO == int(sq_candidato)) <= 1
            consolidado = data.get('dadosConsolidados')
            df_cand.loc[
                df_cand.SQ_CANDIDATO == sq_candidato,
                'received_party'
            ] = consolidado['totalPartidos'] if consolidado else None
            df_cand.loc[
                df_cand.SQ_CANDIDATO == sq_candidato,
                'received_total'
            ] = consolidado['totalRecebido'] if consolidado else None        


        # CALCULATE RANKING
        logger.debug('calculating stats')
        df_cargo_genero = df_cand.groupby(['NR_PARTIDO', 'DS_CARGO', 'CD_CARGO', 'DS_GENERO']).agg({'SQ_CANDIDATO': 'count'})
        df_cargo_genero = df_cargo_genero.reset_index().merge(
            df_cargo_genero.groupby(['NR_PARTIDO', 'DS_CARGO', 'CD_CARGO']).sum().reset_index(),
            how='left', on=(['NR_PARTIDO', 'DS_CARGO', 'CD_CARGO'])
        )
        df_cargo_genero['pct_women'] = df_cargo_genero['SQ_CANDIDATO_x'] / df_cargo_genero['SQ_CANDIDATO_y']
        df_cargo_genero = df_cargo_genero.loc[
            df_cargo_genero['DS_GENERO'] == 'FEMININO',
            ['NR_PARTIDO', 'DS_CARGO', 'CD_CARGO', 'SQ_CANDIDATO_y', 'pct_women']
        ]
        df_cargo_genero.columns = ['party_nb', 'job_role', 'job_role_nb', 'nb_candidates', 'pct_women']
        data = df_cargo_genero.to_json(orient='records')
        logger.debug(f'stats data: {data}')
        resp = requests.post(f'{settings.HOST}/api/meta/stats/', data=data)
        logger.debug(f' => status_code: {resp.status_code} response: {resp.text}')


        # CALCULATE RANKING
        logger.debug('calculating party ranking')
        partidos = df_cand.groupby('NR_PARTIDO').agg({'SG_PARTIDO': 'max', 'NM_PARTIDO': 'min', 'SQ_CANDIDATO': 'count'})
        # women pct
        cand_sex_percent = (
            df_cand.groupby(('NR_PARTIDO', 'DS_GENERO')).agg({'SQ_CANDIDATO': 'count'}) / 
            df_cand.groupby(('NR_PARTIDO')).agg({'SQ_CANDIDATO': 'count'})
        ).reset_index()
        women = cand_sex_percent[cand_sex_percent['DS_GENERO'] == 'FEMININO'].reset_index(drop=True)
        # money pct
        cand_money_percent = (
            df_cand.groupby(('NR_PARTIDO', 'DS_GENERO')).agg({'received_party': 'sum'}) / 
            df_cand.groupby('NR_PARTIDO').agg({'received_party': 'sum'})
        ).reset_index()
        money = cand_money_percent[cand_money_percent['DS_GENERO'] == 'FEMININO']
        # merge dfs
        woman_money = pd.merge(women, money, how='inner', on=('NR_PARTIDO', 'DS_GENERO'))
        ranking = pd.merge(woman_money, partidos, on='NR_PARTIDO', how='inner')
        # ranking
        ranking['ranking'] = ranking['SQ_CANDIDATO_x'] / ranking['SQ_CANDIDATO_x'].max() * ranking['received_party'] / ranking['received_party'].max()
        ranking.sort_values('ranking', ascending=False, inplace=True)
        ranking['index'] = range(1, len(ranking) + 1)
        ranking = ranking.loc[:, ('index', 'NR_PARTIDO', 'SQ_CANDIDATO_x', 'received_party', 'SG_PARTIDO', 'SQ_CANDIDATO_y')]
        ranking.columns = ['ranking', 'party_nb', 'pct_women', 'pct_money_women', 'party_accr', 'party_size']

        logger.debug('send data to app')
        data = ranking.to_json(orient='records', index=True)
        logger.debug(f'ranking data: {data}')
        resp = requests.post(f'{settings.HOST}/api/meta/parties/', data=data)
        logger.debug(f'ranking => status_code: {resp.status_code} response: {resp.text}')
