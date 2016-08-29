from django.shortcuts import render
from django.shortcuts import get_object_or_404
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


def hello(request):
    return HttpResponse("Hello world")


class ExampleView(TemplateView):
    template_name = 'candidates/list.html'

    def get_context_data(self, **kwargs):

        context = super(ExampleView, self).get_context_data(**kwargs)
        context['object_list'] = PoliticalParty.objects.all()

        return context