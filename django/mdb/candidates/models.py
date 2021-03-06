# coding: utf-8
from django.db import models
from django.utils import timezone


class PoliticalParty(models.Model):

    initials = models.CharField(max_length=128, verbose_name='sigla', unique=True)
    name = models.CharField(max_length=128, verbose_name='nome')
    number = models.IntegerField(verbose_name='numero', unique=True)
    directory_national = models.TextField(verbose_name='diretório nacional', null=True, blank=True)
    directory_state = models.TextField(verbose_name='diretório estadual', null=True, blank=True)
    directory_city = models.TextField(verbose_name='diretório municipal', null=True, blank=True)
    about = models.TextField(verbose_name='sobre', null=True)
    obs = models.TextField(null=True, blank=True)

    # meta
    ranking = models.IntegerField(null=True, verbose_name='ranking to partido')
    size = models.IntegerField(null=True, verbose_name='tamanho do partido')
    women_pct = models.FloatField(null=True, verbose_name='porcentagem de mulheres')
    money_women_pct = models.FloatField(null=True, verbose_name='porcentagem de dinheiro destinado a mulheres')

    class Meta:
        verbose_name = 'partido político'
        verbose_name_plural = 'partidos políticos'

    def __str__(self):
        return f'{self.number} - {self.initials}'


class Agenda(models.Model):
    name = models.CharField('Pauta', max_length=128, unique=True)
    icon = models.CharField(max_length=255, verbose_name='ícone', blank=True)
    class Meta:
        verbose_name = 'Pauta'
        verbose_name_plural = 'Pautas'

    def __str__(self):
        return self.name


class State(models.Model):
    uf = models.CharField('UF', max_length=128)
    name = models.CharField('nome', max_length=128)


class JobRole(models.Model):
    name = models.CharField('Cargo', max_length=128, unique=True)
    code = models.CharField('Código', max_length=128, null=True, unique=True)
    initials = models.CharField('Sigla', max_length=128, null=True, blank=True)
    counting = models.IntegerField('Contagem', default=0)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.name


class Candidate(models.Model):
    FEMALE = 'F'
    MALE = 'M'
    GENDER_CHOICES = (
        (FEMALE, 'Feminino'),
        (MALE, 'Masculino')
    )

    PENDING = 'P'
    APPROVED = 'A'
    DENIED = 'D'
    STATUS_CHOICES = (
        (PENDING, 'Pendente'),
        (APPROVED, 'Aprovado'),
        (DENIED, 'Negado')
    )

    id_tse = models.CharField(max_length=100, verbose_name='ID do TSE')
    name = models.CharField(max_length=128, verbose_name='Nome')
    name_ballot = models.CharField(max_length=128, verbose_name='Nome urna')
    number = models.IntegerField(verbose_name='Numero')
    job_role = models.ForeignKey(JobRole, verbose_name='Cargo')
    political_party = models.ForeignKey(PoliticalParty, verbose_name='Partido')
    coalition = models.CharField(max_length=128, verbose_name='Coligação')
    picture_url = models.URLField(verbose_name='URL da foto', null=True, blank=True)
    budget_1t = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Limite de gasto 1.o turno', null=True, blank=True)
    budget_2t = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Limite de gasto 2.o turno', null=True, blank=True)
    agenda = models.ManyToManyField(Agenda, verbose_name='Pauta')
    projects = models.TextField(verbose_name='Projetos', blank=True)
    reelection = models.BooleanField(blank=True, verbose_name='Re-eleição?', default=False)
    elected = models.BooleanField(blank=True, verbose_name='Eleita antes de 2012?', default=False)
    state = models.CharField(default='BR', max_length=100, verbose_name='Estado')

    year = models.CharField(max_length=4, verbose_name='Ano', default='2018')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=FEMALE, verbose_name='Sexo')
    birth_date = models.DateField(verbose_name='Data de nascimento', auto_now=False, auto_now_add=False, blank=True)
    marital_status = models.CharField(max_length=128, verbose_name='Estado civil')
    education = models.CharField(max_length=128, verbose_name='Nível escolaridade')
    job = models.CharField(max_length=128, verbose_name='Ocupação')
    property_value = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Total de bens', default=0)

    email = models.EmailField(verbose_name='Email', blank=True)
    twitter = models.URLField(verbose_name='Twitter', blank=True)
    facebook = models.URLField(verbose_name='Facebook', blank=True)
    instagram = models.URLField(verbose_name='Instagram', blank=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING, verbose_name='Aprovação candidatura MDB')

    class Meta:
        verbose_name = 'candidato'

    def __str__(self):
        return self.name


class Comment(models.Model):
    email = models.EmailField(verbose_name='Email')
    name = models.CharField(verbose_name='Nome', max_length=128)
    comment = models.TextField(verbose_name='Comentário', blank=True)
    candidate = models.ForeignKey(Candidate, verbose_name='Candidata')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Enviado em')
    approved = models.BooleanField('aprovado', default=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return self.name


class Contact(models.Model):
    email = models.EmailField(verbose_name='Email')
    name = models.CharField(verbose_name='Nome', max_length=128)
    message = models.TextField(verbose_name='Comentário', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data')
    reviewed = models.BooleanField(verbose_name='Revisado', default=False)

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return self.name


class Expenses(models.Model):
    candidate = models.ForeignKey(Candidate, verbose_name='Candidata')
    received = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Total recebido')
    paid = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Total Gasto')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data')    


class PartyJobRoleStats(models.Model):

    political_party = models.ForeignKey(PoliticalParty, verbose_name='Partido')
    job_role = models.ForeignKey(JobRole, verbose_name='Cargo')
    size = models.IntegerField(null=True, verbose_name='Número de candidatos nesse cargo por partido')
    women_pct = models.FloatField(null=True, verbose_name='porcentagem de mulheres')
