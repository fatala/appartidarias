# coding: utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import CommentForm, ContactForm
from .models import Candidate, PoliticalParty, Agenda, Comment
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

    def get_object(self):
        return Candidate.objects.get(pk=self.kwargs['candidate_id'])

    def get_context_data(self, **kwargs):
        context = super(CandidateDetail, self).get_context_data(**kwargs)
        candidate_id = kwargs['candidate_id']

        context['candidate'] = self.get_object()

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
            subject = 'AppartidariAs - contato'
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']

            recipients = ['contato@grupomulheresdorasil.com.br']

            send_mail(subject, message, sender, recipients)

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
