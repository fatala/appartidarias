import io
import boto3
import json
import pandas
import logging
import zipfile
import requests

from datetime import datetime
from django.conf import settings

logger = logging.getLogger('mdb')

estados = [
    'AP', 'AM', 'RR', 'PA', 'AP', 'RO', 'TO',
    'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA',
    'MG', 'ES', 'RJ', 'SP',
    'MT', 'MS', 'GO', 'DF',
    'PR', 'SC', 'RS',
    'BR', 'ZZ', 'VT',
]

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)

s3_resource = boto3.resource(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)

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


def store_json(key, data, bucket='appartidarias'):
    assert type(data) == dict
    s3_client.put_object(Body=json.dumps(data), Bucket=bucket, Key=key)
    logger.debug(f'sent to s3: {key}')


def download_file(url):
    """
    Download and save file
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.debug('[{}] Downloaded {}'.format(now, url))
    resp = requests.get(url)
    if resp.ok:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zip_ref:
            return {
                name: zip_ref.read(name)
                for name in zip_ref.namelist()
                if name.split('.')[-1] == 'csv'
            }
