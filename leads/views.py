from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from .models  import Lead,Agent
from .forms import LeadForm, LeadModelForm,Lead,CustomUserCreationForm
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizorAndLoginRequiredMixin

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")    

class LandingPageView(TemplateView):
    template_name="landing.html"

def landing_page(request):
    return render(request,"landing.html")

class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    
    def get_queryset(self):
        user = self.request.user
        #initial query of lead in the organization
        if user.is_organizor:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            #query for logged agent
            queryset = queryset.filter(agent__user = user)
        return queryset



def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads':leads,
    }
    return render(request,"leads/lead_list.html",context)

class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead':lead
    }
    return render(request,"leads/lead_detail.html",context)

class LeadCreateView(OrganizorAndLoginRequiredMixin,CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        #TO SEND EMAIL
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView,self).form_valid(form)

def lead_create(request):
    form = LeadModelForm()
    if request.method=="POST":
        print('Receiving a post request')
        form = LeadModelForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context={
        "form":form
    }
    return render(request,"leads/lead_create.html",context)

class LeadUpdateView(OrganizorAndLoginRequiredMixin,UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method=="POST":
        form = LeadModelForm(request.POST,instance=lead) 
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form":form,
        'lead':lead
    }
    return render(request,"leads/lead_update.html",context)

class LeadDeleteView(OrganizorAndLoginRequiredMixin,DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')