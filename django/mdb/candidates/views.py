# coding: utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Candidate, PoliticalParty
from .serializers import CandidateSerializer


class CandidateList(APIView):

    def get(self, request):
        candidate = Candidate.objects.all()
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data)


class PoliticalPartyCandidates(TemplateView):
    template_name = 'candidates/political_party_candidates_list.html'

    def get_context_data(self, **kwargs):
        context = super(PoliticalPartyCandidates, self).get_context_data(**kwargs)
        context['candidates_list'] = Candidate.objects.filter(
            political_party__id=kwargs['political_party_id']
        )

        return context


class CandidateDetail(TemplateView):
    template_name = 'candidates/candidate_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CandidateDetail, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(pk=kwargs['candidate_id'])

        return context


class PoliticalPartyListView(TemplateView):
    template_name = 'candidates/political_party_list.html'
    page_size = 5

    def get_context_data(self, **kwargs):
        context = super(PoliticalPartyListView, self).get_context_data(**kwargs)

        political_parties = PoliticalParty.objects.all()

        paginator = Paginator(political_parties, self.page_size)

        page = self.request.GET.get('page', 1)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context['object_list'] = object_list

        #search
        query = self.request.GET.get('query')
        if query:
            try:
                query = int(query)
                candidate_list = Candidate.objects.filter(number=query)
            except ValueError:
                candidate_list = Candidate.objects.filter(name__icontains=query)
            context['candidate_list'] = candidate_list
            context['query'] = query

        return context


class IndexView(TemplateView):
    template_name = 'candidates/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return context