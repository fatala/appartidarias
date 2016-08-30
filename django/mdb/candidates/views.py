# coding: utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Candidate, PoliticalParty, Agenda
from .serializers import CandidateSerializer


class CandidateList(APIView):

    def get(self, request):
        candidate = Candidate.objects.all()
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data)


class CandidateListFilter(TemplateView):
    template_name = 'candidates/candidate_list.html'
    page_size = 10

    def get_context_data(self, **kwargs):
        context = super(CandidateListFilter, self).get_context_data(**kwargs)

        if kwargs['type'] == "political_party":
            candidates = Candidate.objects.filter(
                political_party__id=kwargs['id']
            )
            if candidates:
                context['title'] = candidates[0].political_party.name
        else:
            candidates = Candidate.objects.filter(
                agenda__id=kwargs['id']
            )
            if candidates:
                context['title'] = candidates[0].agenda.name

        paginator = Paginator(candidates, self.page_size)

        page = self.request.GET.get('page', 1)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context['candidates_list'] = object_list

        return context


class CandidateDetail(TemplateView):
    template_name = 'candidates/candidate_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CandidateDetail, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(pk=kwargs['candidate_id'])

        return context


class PoliticalPartyListView(TemplateView):
    template_name = 'candidates/political_party_list.html'
    page_size = 20

    def get_context_data(self, **kwargs):
        context = super(PoliticalPartyListView, self).get_context_data(**kwargs)

        political_parties = PoliticalParty.objects.order_by('name')

        paginator = Paginator(political_parties, self.page_size)

        page = self.request.GET.get('page', 1)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        context['object_list'] = object_list

        return context


class CandidateSearchView(TemplateView):
    template_name = 'candidates/candidate_search.html'

    def get_context_data(self, **kwargs):
        context = super(CandidateSearchView, self).get_context_data(**kwargs)

        query = self.request.GET.get('query')
        if query:
            try:
                query = int(query)
                candidate_list = Candidate.objects.filter(number=query)
            except ValueError:
                candidate_list = Candidate.objects.filter(name__icontains=query)
            context['candidates_list'] = candidate_list
            context['query'] = query

        return context


class IndexView(TemplateView):
    template_name = 'candidates/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return context


class AgendaListView(TemplateView):
    template_name = 'candidates/agenda_list.html'

    def get_context_data(self, **kwargs):
        context = super(AgendaListView, self).get_context_data(**kwargs)
        context['agenda_list'] = Agenda.objects.order_by("name")

        return context


class AgendaCandidates(TemplateView):
    template_name = 'candidates/agenda_candidates_list.html'

    def get_context_data(self, **kwargs):
        context = super(AgendaCandidates, self).get_context_data(**kwargs)
        context['candidates_list'] = Candidate.objects.filter(
            agenda__id=kwargs['agenda_id']
        )

        return context
