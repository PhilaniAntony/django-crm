from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorRequiredMixixn
from .models import Lead, Category
from .forms import CreateLeadForm, CustomUserCreateForm, AssignAgentForm, LeadCategoryUpdateForm

# Create your views here.


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreateForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'home-page.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=False)

        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, agent__isnull=False)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads":  queryset,
            })
        return context


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'lead-detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)

        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset


class LeadCreatelView(OrganisorRequiredMixixn, CreateView):
    template_name = 'lead-create.html'
    form_class = CreateLeadForm

    def get_success_url(self):
        return reverse("leads:homepage")

    def form_valid(self, form):
        # send_mail(
        #subject='Lead has been created',
        #message='Go to site and view the new lead',
        # from_email='test@test.com',
        # recipient_list=['iamturnaog@gmail.com']
        # )
        return super(LeadCreatelView, self).form_valid(form)


class LeadUpdateView(OrganisorRequiredMixixn, UpdateView):
    template_name = 'lead-update.html'
    form_class = CreateLeadForm

    def get_success_url(self):
        return reverse("leads:homepage")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)


class LeadDeleteView(OrganisorRequiredMixixn, DeleteView):
    template_name = 'lead-delete.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:homepage")


class AssignAgentView(OrganisorRequiredMixixn, FormView):
    template_name = 'assign-agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentForm, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        return reverse('leads:homepage')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentForm, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category-list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)

        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization)

        context.update({
            'unassigned_lead_count': queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.userprofile)

        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization)

        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'category-details.html'
    context_object_name = 'category'

    """ def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        leads = self.get_object().leads.all()
        context.update({
            'leads': leads
        })

        return context """

    def get_queryset(self):
        user = self.request.user

        if user.is_organisor:
            queryset = Category.objects.filter(organization=user.userprofile)

        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization)

        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'lead-category-update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)

        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_success_url(self):
        return reverse('leads:lead-detail', kwargs={"pk": self.get_object().id})
