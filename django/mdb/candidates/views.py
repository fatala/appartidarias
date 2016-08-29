from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, PoliticalParty
from .serializers import CandidateSerializer
from django.http import HttpResponse


class CandidateList(APIView):

    def get(self, request):
        candidate = Candidate.objects.all()
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data)


class PoliticalPartyCandidates(TemplateView):
    template_name = 'candidates/list.html'

    def get_context_data(self, **kwargs):
        context = super(PoliticalPartyCandidates, self).get_context_data(**kwargs)
        context['candidates_list'] = Candidate.objects.filter(political_party__id=kwargs['political_party_id'])

        #return context
        return HttpResponse(kwargs['political_party_id'])

def hello(request):
    return HttpResponse("Hello world")