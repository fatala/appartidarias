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


Criar virtualenv (use ``virtualenvwrapper``): ::

    mkvirtualenv mdb


Install requirements via ``pip``: ::

    pip install -r django/requirements/development.txt


Criar tabelas do banco de dados: ::

    $ python django/mdb/manage.py migrate


Rodar o projeto: ::

    $ python django/mdb/manage.py runserver


Comandos úteis
--------------

Remover todas as candidatas: ::

    $ python django/mdb/manage.py clear_models


Importar candidatas do TSE: ::

    $ python django/mdb/manage.py sync_tse_2018


Deploy
------

Instalar o teresa via `homebrew`: ::

  $ brew tap luizalabs/teresa-cli
  $ brew install teresa

Apontar para o endereço do cluster onde deseja fazer o deploy: ::

  $ teresa config set-cluster [nome_cluster] --server [cluster_host] --tls --current

Criar um usuário: ::

  Pedir no canal #firefighting do slack a criação de um usuário

Fazer login no teresa: ::

  $ teresa login --user [email]

Criar applicação se não existir: ::

  $ teresa app create [app] --team [team]

Configurar as env vars disponíveis nesse [link] (https://docs.google.com/document/d/1f4Ajcw0iNdbWnr_pRhpwELOLQqLamytjV3e91lFGA3U/edit?usp=sharing): ::

  $ teresa app env-set --app appartidarias [env vars]

Fazer o deploy da applicação: ::

  $ teresa deploy create . --app [app] --description '[versão] [Descrição]'
