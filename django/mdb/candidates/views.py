# coding: utf-8
import json
import logging
import requests

from datetime import date, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

from utils import fetch_2018_candidate_expenses
from .forms import CommentForm, ContactForm
from .models import (
    Candidate,
    PoliticalParty,
    Agenda,
    Comment,
    JobRole,
    PartyJobRoleStats,
)
from .serializers import (
    CandidateSerializer,
    JobRoleSerializer,
    PartySerializer,
    StateSerializer,
    StatsSerializer,
)

logger = logging.getLogger('mdb')


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
        parties = PoliticalParty.objects.all().order_by('ranking')
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
        if 'ano' in query:
            candidates = candidates.filter(year=query['ano'])
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

        try:
            context['budget'] = fetch_2018_candidate_expenses(
                urna=context['candidate'].number,
                partido=context['candidate'].political_party.number,
                estado=context['candidate'].state,
                cargo=context['candidate'].job_role.code,
                candidate=context['candidate'].id_tse,
            )
            logger.debug(f'budget: {context["budget"]}')

        except Exception:
            logger.exception('Failed to fetch expenses')

        context['comments'] = Comment.objects.filter(
            candidate_id=candidate_id,
            approved=True,
        )
        context['form'] = CommentForm()

        context['similar_candidates'] = Candidate.objects.filter(
            gender='F'
        ).filter(
            political_party=context['candidate'].political_party
        ).exclude(
            id_tse=context['candidate'].id_tse
        )[:6]

        try:
            birth_date = context['candidate'].birth_date
            year = timedelta(days=365.2425)
            context['age'] = (date.today() - birth_date) // year

        except Exception:
            logger.exception('error calculating age')

        context['pautas'] = context['candidate'].agenda.all()

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

        # paginate
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

    
class PoliticalPartyTemplate(TemplateView):
    template_name = 'candidates/political_party_detail.html'

    def get_object(self):
        return PoliticalParty.objects.get(initials=self.kwargs['party_initials'])

    def get_context_data(self, **kwargs):
        context = super(PoliticalPartyTemplate, self).get_context_data(**kwargs)
        party = self.get_object()

        stats = PartyJobRoleStats.objects.filter(political_party=party)
        charts = StatsSerializer(stats, many=True).data
        charts.append(PartySerializer(party).data)

        context['party'] = party
        context['party_img'] = party.initials.lower()
        context['charts'] = json.dumps(charts)

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
        logger.debug(f'PoliticalPartyMeta: {data}')
        parties = []

        for d in data:

            party = PoliticalParty.objects.get(
                number=d['party_nb'],
                initials=d['party_accr']
            )

            party.ranking = d['ranking']
            party.size = d['party_size']
            party.women_pct = d['pct_women']
            party.money_women_pct = d['pct_money_women']

            party.save()
            parties.append(party)

        serializer = PartySerializer(parties, many=True)
        return JsonResponse(serializer.data, safe=False)


class Stats(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        logger.debug(f'Stats: {data}')

        stats_array = []
        for d in data:

            logger.debug(f'stats data{d}')

            try:
                party = PoliticalParty.objects.get(
                    number=d['party_nb'],
                )

                job_role = JobRole.objects.get(
                    code=d['job_role_nb'],
                )

                stats, _ = PartyJobRoleStats.objects.get_or_create(
                    job_role=job_role,
                    political_party=party,
                )

                stats.size = d['nb_candidates']
                stats.women_pct = d['pct_women']
                # stats.money_women_pct = d['pct_money_women']

                stats.save()
                stats_array.append(stats)

            except Exception:
                logger.exception('Parsing stats')

        serializer = StatsSerializer(stats_array, many=True)
        return JsonResponse(serializer.data, safe=False)
