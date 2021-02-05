from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganisorRequiredMixixn
from leads.models import Agent
from .forms import AgentModelForm
import random
# Create your views here.


class AgentListView(OrganisorRequiredMixixn, generic.ListView):
    template_name = 'agents/agents-list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organization=organisation)


class AgentCreateView(OrganisorRequiredMixixn, generic.CreateView):
    template_name = 'agents/agent-create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_orgamisor = False
        user.set_password(f'{ random.randint(0, 1000000) }')
        user.save()
        Agent.objects.create(
            user=user, organization=self.request.user.userprofile)
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorRequiredMixixn, generic.DetailView):
    template_name = 'agents/agent-detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.all()


class AgentUpdateView(OrganisorRequiredMixixn, generic.UpdateView):
    template_name = 'agents/agent-update.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        user = self.request.user
        return Agent.objects.filter(organization=user.userprofile)


class AgentDeleteView(OrganisorRequiredMixixn, generic.DeleteView):
    template_name = 'agents/agent-delete.html'
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        return Agent.objects.all()
