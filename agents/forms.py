from django import forms
from leads.models import Agent
from django.contrib.auth import get_user_model

User = get_user_model()

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'    
        )