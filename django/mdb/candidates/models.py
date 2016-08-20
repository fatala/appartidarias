from django.db import models


class PoliticalParty(models.Model):
    initials = models.CharField(max_length=128, verbose_name='sigla')
    name = models.CharField(max_length=128, verbose_name='nome')
    directory_national = models.TextField(verbose_name='diretório nacional')
    directory_state = models.TextField(verbose_name='diretório estadual')
    directory_city = models.TextField(verbose_name='diretório municipal')
    obs = models.TextField()

    class Meta:
        verbose_name = 'partido político'
        verbose_name_plural = 'partidos políticos'

    def __str__(self):
        return self.name


class Agenda(models.Model):
    name = models.CharField('Pauta', max_length=128)

    class Meta:
        verbose_name = 'Pauta'
        verbose_name_plural = 'Pautas'

    def __str__(self):
        return self.name


class Candidate(models.Model):
    political_party = models.ForeignKey(PoliticalParty, verbose_name='partido')
    name = models.CharField(max_length=128, verbose_name='Nome')
    number = models.IntegerField(verbose_name='numero')
    agenda = models.ForeignKey(Agenda, verbose_name='Pauta')
    projects = models.TextField(verbose_name='Projetos')

    class Meta:
        verbose_name = 'candidato'

    def __str__(self):
        return self.name
