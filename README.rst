AppartidariAs
==========================

http://www.appartidarias.com.br


Para que serve essa aplicação?
------------------------------

Dentre os nossos projetos está o monitoramento de candidatas à vereadora do município de São Paulo. Por meio desta webpage, cidadãos e cidadãs observarão as candidatas, poderão ver e nos informar sobre (i) quais pautas, desafios e desempenho estão sendo identificados nessas campanhas e (ii) dados sobre o cumprimento da lei de quotas para candidatas mulheres. As candidatas identificadas como figurantes serão informadas ao Ministério Público Eleitoral do Estado de SP, conforme os termos da parceria firmada com o Grupo Mulheres do Brasil.


Requisitos
----------

Python 3
Virtualenv


Configuração
------------

::

    export DJANGO_SETTINGS_MODULE=settings.{env_name}


Criar virtualenv (use ``virtualenvwrapper``): ::

    mkvirtualenv mdb


Install requirements via ``pip``: ::

    pip install django/requirements/development.txt


Criar tabelas do banco de dados: ::

    # no diretório django/mdb
    ./manage.py syncdb --all --settings=settings.development


Rodar o projeto: ::

    # no diretório django/mdb
    ./manage.py runserver --settings=settings.development


Comandos úteis
--------------

Remover todas as candidatas: ::

    # no diretório django/mdb
    ./manage.py clear_models


Importar candidatas do TSE: ::

    # no diretório django/mdb
    ./manage.py sync_tse