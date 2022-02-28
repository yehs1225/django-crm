import random
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizorAndLoginRequiredMixin

class AgentListView(OrganizorAndLoginRequiredMixin,generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"
    def get_queryset(self):
        return Agent.objects.all()

class AgentCreateView(OrganizorAndLoginRequiredMixin,generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_organizor = False
        user.is_agent = True
        user.set_password(f"{random.randint(0,100000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject="You are invited as agent!(YEHCRM)",
            message = "Please go to YEHCRM to comfirm.",
            from_email = 'admin@test.com',
            recipient_list = [user.email]
        )
        return super(AgentCreateView,self).form_valid(form)
    
class AgentDetailView(OrganizorAndLoginRequiredMixin,generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    
    def get_queryset(self):
        return Agent.objects.all()

class AgentUpdateView(OrganizorAndLoginRequiredMixin,generic.UpdateView):
    template_name = "agents/agent_update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse('agents:agent-list')

class AgentDeleteView(OrganizorAndLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("agents:agent-list")
