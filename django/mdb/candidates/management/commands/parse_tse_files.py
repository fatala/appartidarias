import os
import glob
import pandas
from datetime import datetime

FOLDER = './Arquivos_originais'
ANO = '2018'
ARQUIVOS_CANDIDATOS = os.path.join(FOLDER, 'consulta_cand_{}/*.csv'.format(ANO))
ARQUIVOS_BENS = os.path.join(FOLDER, 'bem_candidato_{}/*.csv'.format(ANO))
ARQUIVOS_COLIGACAO = os.path.join(FOLDER, 'consulta_coligacao_{}/*.csv'.format(ANO))
ARQUIVOS_VAGAS = os.path.join(FOLDER, 'consulta_vagas_{}/*.csv'.format(ANO))
ARQUIVOS_CASSACAO = os.path.join(FOLDER, 'motivo_cassacao_{}/*.csv'.format(ANO))

def concat(files):
    """
    Concat TSE files into a single pandas.DataFrame
    """
    return pandas.concat([
        pandas.read_csv(
            pandas.compat.StringIO(file_),
            encoding='latin1',
            sep=';',
        )
        for _, file_ in files.items()
    ])


def parse_candidatos(dataframe):
    dataframe['GERACAO'] = dataframe.apply(
        lambda row: datetime.strptime(
            row['DT_GERACAO']+row['HH_GERACAO'],
            '%d/%m/%Y%H:%M:%S'
        ),
        axis = 1
    )
    dataframe['DT_NASCIMENTO'] = dataframe.apply(
        lambda row: datetime.strptime(
            row['DT_NASCIMENTO'],
            '%d/%m/%Y'
        ).date(),
        axis = 1
    )
    colunas = [
        'GERACAO',
        'SQ_CANDIDATO',
        'ANO_ELEICAO',
        'NR_TURNO',
        'SG_UF',
        'DS_CARGO',
        'NR_CANDIDATO',
        'NM_CANDIDATO',
        'NM_URNA_CANDIDATO',
        'NM_SOCIAL_CANDIDATO',
        'NR_CPF_CANDIDATO',
        'NM_EMAIL',
        'DS_SITUACAO_CANDIDATURA',
        'DS_DETALHE_SITUACAO_CAND',
        'TP_AGREMIACAO',
        'SG_PARTIDO',
        'SQ_COLIGACAO',
        'DS_NACIONALIDADE',
        'NM_MUNICIPIO_NASCIMENTO',
        'DT_NASCIMENTO',
        'NR_TITULO_ELEITORAL_CANDIDATO',
        'DS_GENERO',
        'DS_GRAU_INSTRUCAO',
        'DS_ESTADO_CIVIL',
        'DS_COR_RACA',
        'DS_OCUPACAO',
        'ST_REELEICAO',
        'ST_DECLARAR_BENS',
        'NR_PROCESSO'
    ]
    for col in colunas[1:4]:
        dataframe[col] = dataframe[col].astype(int)
    for col in colunas[4:]:
        dataframe[col] = dataframe[col].astype(str)
    return dataframe[colunas]



def parse_bens(dataframe):
    """
    Arruma o arquivo de bens de candidatos
    """
    dataframe['GERACAO'] = dataframe.apply(
        lambda row: datetime.strptime(
            row['DT_GERACAO']+row['HH_GERACAO'],
            '%d/%m/%Y%H:%M:%S'
        ),
        axis = 1
    )
    dataframe['ATUALIZACAO'] = dataframe.apply(
        lambda row: datetime.strptime(
            row['DT_ULTIMA_ATUALIZACAO']+row['HH_ULTIMA_ATUALIZACAO'],
            '%d/%m/%Y%H:%M:%S'
        ),
        axis = 1
    )
    dataframe['ANO_ELEICAO'] = dataframe['ANO_ELEICAO'].astype(int)
    dataframe['SQ_CANDIDATO'] = dataframe['SQ_CANDIDATO'].astype(int)
    dataframe['DS_TIPO_BEM_CANDIDATO'] = dataframe['DS_TIPO_BEM_CANDIDATO'].astype(str)
    dataframe['DS_BEM_CANDIDATO'] = dataframe['DS_BEM_CANDIDATO'].astype(str)
    dataframe['VR_BEM_CANDIDATO'] = dataframe['VR_BEM_CANDIDATO'].apply(
        lambda x: float(x.replace(',','.'))
    ).astype(float)

    colunas = [
        'GERACAO',
        'ATUALIZACAO',
        'SQ_CANDIDATO',
        'ANO_ELEICAO',
        'DS_TIPO_BEM_CANDIDATO',
        'DS_BEM_CANDIDATO',
        'VR_BEM_CANDIDATO'
    ]
    df = dataframe[colunas]
    return df


def compile():

    df = concat(ARQUIVOS_CANDIDATOS)
    # fname = 'dados_candidatos.csv'
    # df.to_csv(fname, encoding='utf-8', index=False)
    # os.system('pigz -1 -k {}'.format(fname))

    # df = concat(ARQUIVOS_BENS)
    # fname = 'Dados_bens.csv'
    # df.to_csv(fname, encoding='utf-8', index=False)
    # os.system('pigz -1 -k {}'.format(fname))

    # df = concat(ARQUIVOS_COLIGACAO)
    # fname = 'Dados_coligacao.csv'
    # df.to_csv(fname, encoding='utf-8', index=False)
    # os.system('pigz -1 -k {}'.format(fname))

    # df = concat(ARQUIVOS_VAGAS)
    # fname = 'Dados_vagas.csv'
    # df.to_csv(fname, encoding='utf-8', index=False)
    # os.system('pigz -1 -k {}'.format(fname))

    # df = concat(ARQUIVOS_CASSACAO)
    # fname = 'Dados_cassacao.csv'
    # df.to_csv(fname, encoding='utf-8', index=False)
    # os.system('pigz -1 -k {}'.format(fname))

if __name__=='__main__':
    compile()
