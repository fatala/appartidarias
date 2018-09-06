from rest_framework import serializers
from .models import Candidate, PoliticalParty, JobRole, State, PartyJobRoleStats


class CandidateSerializer(serializers.ModelSerializer):
    political_party_initials = serializers.ReadOnlyField(source='political_party.initials')
    political_party_name = serializers.ReadOnlyField(source='political_party.name')
    directory_national = serializers.ReadOnlyField(source='political_party.directory_national')
    directory_state = serializers.ReadOnlyField(source='political_party.directory_state')
    directory_city = serializers.ReadOnlyField(source='political_party.directory_ciry')
    obs = serializers.ReadOnlyField(source='political_party.obs')
    agenda = serializers.ReadOnlyField(source='agenda.name')


    class Meta:
        model = Candidate
        fields = (
            'name',
            'political_party_initials',
            'political_party_name',
            'directory_national',
            'directory_state',
            'directory_city',
            'picture_url',
            'status',
            'obs',
            'number',
            'agenda',
            'projects',
        )


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = (
            'initials',
            'name',
            'ranking',
            'size',
            'women_pct',
            'money_women_pct',
        )


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = (
            'name',
            'uf'
        )


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = (
            'name',
            'code'
        )


class StatsSerializer(serializers.ModelSerializer):
    job_role_name = serializers.StringRelatedField(source='job_role', read_only=True)
    class Meta:
        model = PartyJobRoleStats
        fields = (
            'political_party',
            'job_role',
            'job_role_name',
            'size',
            'women_pct',
        )
