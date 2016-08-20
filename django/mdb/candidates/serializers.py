from rest_framework import serializers
from .models import Candidate


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
        	'name', 'political_party_initials', 'political_party_name', 'directory_national', 'directory_state',
        	'directory_city', 'obs', 'number', 'agenda', 'projects',
        	)
