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
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()
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
