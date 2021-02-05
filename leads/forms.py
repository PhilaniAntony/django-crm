from django import forms
from django.forms import fields
from .models import Lead, User, Agent
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CreateLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'description',
            'phone_number',
            'email',
            'agent',
            'organization',
            'category',)


class CustomUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', )
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('category',)
