# coding: utf-8
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import CommentForm, ContactForm
from .models import Candidate, PoliticalParty, Agenda, Comment, JobRole
from .serializers import CandidateSerializer, JobRoleSerializer, PartySerializer, StateSerializer

import json
import requests

class StateList(APIView):
    def get(self, request):
        states = []
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)


class JobRoleList(APIView):
    def get(self, request):
        job_roles = JobRole.objects.all()
        serializer = JobRoleSerializer(job_roles, many=True)
        return Response(serializer.data)


class PartiesList(APIView):
    def get(self, request):
        parties = PoliticalParty.objects.all()
        serializer = PartySerializer(parties, many=True)
        return Response(serializer.data)


class CandidateList(APIView):

    def get(self, request):
        query = request.query_params

        # pagination
        page_size = int(query.get('page_size') or settings.PAGE_SIZE)
        page = int(query.get('page') or 1)

        candidates = Candidate.objects.all()

        # filter candiadates
        if 'sexo' in query:
            candidates = candidates.filter(gender=query['sexo'])
        if 'estado' in query:
            candidates = candidates.filter(state=query['estado'])
        if 'partido' in query:
            candidates = candidates.filter(political_party__initials=query['partido'])
        if 'cargo' in query:
            candidates = candidates.filter(job_role__name=query['cargo'])

        paginated_candidates = candidates[(page-1)*page_size:page*page_size]
        serializer = CandidateSerializer(paginated_candidates, many=True)
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

    def get_object(self):
        return Candidate.objects.get(pk=self.kwargs['candidate_id'])

    def get_context_data(self, **kwargs):
        context = super(CandidateDetail, self).get_context_data(**kwargs)

        candidate_id = kwargs['candidate_id']
        context['candidate'] = self.get_object()

        attempt = 1
        while range(6):
            try:
                url = 'http://divulgacandcontas.tse.jus.br/divulga/rest/v1/prestador/consulta/2/2016/71072/13/{}/{}/{}'.format(context['candidate'].political_party.number, context['candidate'].number, context['candidate'].id_tse)
                print('Getting {} attempt #{}'.format(url, attempt))
                context['budget'] = requests.get(url).json()
                print('Response: {}'.format(context['budget']))
            except Exception as e:
                print('Failed to fetch or decode budget: {}'.format(str(e)))
                attempt += 1
                continue
            else:
                break

        context['comments'] = Comment.objects.filter(
            candidate_id=candidate_id,
            approved=True,
        )
        context['form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = CommentForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.candidate = self.get_object()
            instance.save()

            context['success'] = True
        else:
            context['success'] = False
            context['errors'] = form.errors

        return self.render_to_response(context)


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


class PoliticalPartyDetail(TemplateView):
    template_name = 'candidates/political_party_detail.html'

    def get_object(self):
        return PoliticalParty.objects.get(initials=self.kwargs['party_initials'])

    def get_context_data(self, **kwargs):
        context = super(PoliticalPartyDetail, self).get_context_data(**kwargs)

        party = self.get_object()
        context['party'] = party
        context['party_img'] = party.initials.lower()

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


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
                candidate_list = Candidate.objects.filter(name_ballot__icontains=query)
            context['candidates_list'] = candidate_list
            context['query'] = query

        return context


class IndexView(TemplateView):
    template_name = 'candidates/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['host'] = settings.HOST
        return context


class AboutView(TemplateView):
    template_name = 'candidates/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)

        return context


class Elections2012View(TemplateView):
    template_name = 'candidates/elections2012.html'

    def get_context_data(self, **kwargs):
        context = super(Elections2012View, self).get_context_data(**kwargs)

        return context


class ContactView(TemplateView):
    template_name = 'candidates/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)

        return context


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContactForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            context['success'] = True
        else:
            context['success'] = False
            context['errors'] = form.errors

        return self.render_to_response(context)


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


class PoliticalPartyMeta(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        parties = []

        for d in data:

            party = PoliticalParty.objects.filter(
                number=d['party_nb'],
                initials=d['party_accr']
            )[0]

            party.ranking = d['ranking']
            party.size = d['party_size']
            party.women_ptc = int(d['pct_women']*100)
            party.money_women_pct = int(d['pct_money_women']*100)

            party.save()
            parties.append(party)

        serializer = PartySerializer(parties, many=True)
        return JsonResponse(serializer.data, safe=False)
