from django.db import models


class PoliticalParty(models.Model):
    initials = models.CharField(max_length=128, verbose_name='sigla')
    name = models.CharField(max_length=128, verbose_name='nome')
    number = models.IntegerField(verbose_name='numero')
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


class JobRole(models.Model):
    name = models.CharField('Cargo', max_length=128)

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
    political_party = models.ForeignKey(PoliticalParty, verbose_name='partido')
    name = models.CharField(max_length=128, verbose_name='Nome')
    number = models.IntegerField(verbose_name='numero')
    job_role = models.ForeignKey(JobRole, verbose_name='Cargo')
    picture_url = models.CharField(max_length=256, verbose_name='URL da foto')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=FEMALE, verbose_name='sexo')
    agenda = models.ForeignKey(Agenda, verbose_name='Pauta')
    projects = models.TextField(verbose_name='Projetos')

    class Meta:
        verbose_name = 'candidato'

    def __str__(self):
        return self.name