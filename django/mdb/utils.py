import json, boto3

from django.conf import settings

estados = [
    'AP', 'AM', 'RR', 'PA', 'AP', 'RO', 'TO',
    'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA',
    'MG', 'ES', 'RJ', 'SP',
    'MT', 'MS', 'GO', 'DF',
    'PR', 'SC', 'RS',
    'BR', 'ZZ', 'VT',
]


s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
)

def store_json(key, data, bucket='appartidarias'):
    assert type(data) == dict
    s3.put_object(Body=json.dumps(data), Bucket=bucket, Key=key)
