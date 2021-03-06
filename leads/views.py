import datetime
from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from .models  import Lead,Agent,Category,FollowUp
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizorAndLoginRequiredMixin
from django.contrib import messages
from .forms import(
    LeadForm,
    LeadModelForm,
    CustomUserCreationForm,
    AssinAgentForm,
    LeadCategoryUpdateForm,
    CategoryModelForm,
    FollowUpModelForm
) 


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")    

class LandingPageView(TemplateView):
    template_name="landing.html"

    def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                # if already login , redirect to dashboard.html
                return redirect("dashboard")
            return super().dispatch(request, *args, **kwargs)  

class DashboardView(OrganizorAndLoginRequiredMixin,TemplateView):
    template_name="dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView,self).get_context_data(**kwargs)
        user = self.request.user
        #How many leads we have in total
        total_lead_count = Lead.objects.filter(organization = user.userprofile).count()

        #How many new leads in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
        total_in_past30 = Lead.objects.filter(
            organization = user.userprofile,
            #filter field "data_added" data which are Grater Than Eqaul 30days ago
            date_added__gte=thirty_days_ago 
        ).count()

        #How many agents we have in total
        total_agent_count = Agent.objects.filter(organization = user.userprofile).count()
        context.update({
            "total_lead_count":total_lead_count,
            "total_in_past30":total_in_past30,
            "total_agent_count":total_agent_count
        })

        return context

def landing_page(request):
    return render(request,"landing.html")

class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        #initial query of lead in the organization
        if user.is_organizor:
            queryset = Lead.objects.filter(organization = user.userprofile,agent__isnull = False)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization,agent__isnull = False)
            #query for logged agent
            queryset = queryset.filter(agent__user = user)
        return queryset
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView,self).get_context_data(**kwargs)
        if user.is_organizor:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull = True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context

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
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        #TO SEND EMAIL
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request,"You have successfully created a lead!")
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

    def form_valid(self,form):
        form.save()
        messages.info(self.request,"You have successfully updated this lead!")
        return super(LeadUpdateView,self).form_valid(form)

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

class AssignAgentView(OrganizorAndLoginRequiredMixin,FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssinAgentForm

    #pass extra arguments into the form
    def get_form_kwargs(self,**kwargs):
        kwargs=super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self,form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)

class CategoryListView(OrganizorAndLoginRequiredMixin,ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self,**kwargs):
        context = super(CategoryListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizor:
            queryset = Lead.objects.filter(
                organization = user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization = user.agent.organization
            )
        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull=True).count(),
        })
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(
            organization = user.userprofile
        )
        return queryset

class CategoryDetailView(OrganizorAndLoginRequiredMixin,DetailView):
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user
        #initial query of lead in the organization
        if user.is_organizor:
            queryset = Category.objects.filter(
                organization = user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization = user.agent.organization
            )
        return queryset

class CategoryCreateView(OrganizorAndLoginRequiredMixin,CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm
    
    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self,form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView,self).form_valid(form)

class CategoryUpdateView(OrganizorAndLoginRequiredMixin,UpdateView):
    template_name = "leads/category_update.html"
    queryset = Category.objects.all()
    form_class = CategoryModelForm
    
    def get_success_url(self):
        return reverse("leads:category-list")

class CategoryDeleteView(OrganizorAndLoginRequiredMixin,DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organizor:
            queryset = Category.objects.filter(
                organization = user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization = user.agent.organization
            )
        return queryset
class LeadCategoryUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "leads/lead_catogory_update.html"
    form_class = LeadCategoryUpdateForm
    
    def get_queryset(self):
        user = self.request.user
        #initial query of lead in the organization
        if user.is_organizor:
            queryset = Lead.objects.filter(
                organization = user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization = user.agent.organization
            )
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")

class FollowUpCreateView(LoginRequiredMixin,CreateView):
    template_name = "leads/followup_create.html"
    form_class = FollowUpModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk":self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView,self).get_context_data(**kwargs)
        context.update({
            "lead":Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self,form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView,self).form_valid(form)

class FollowUpUpdateView(OrganizorAndLoginRequiredMixin,UpdateView):
    template_name = "leads/followup_update.html"
    form_class = FollowUpModelForm
    
    def get_queryset(self):
        user = self.request.user
        #query followUp of the lead
        if user.is_organizor:
            queryset = FollowUp.objects.filter(
                lead__organization = user.userprofile
            )
        else:
            queryset = FollowUp.objects.filter(
                lead__organization = user.agent.organization
            )
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk":self.get_object().lead.id})
   
class FollowUpDeleteView(OrganizorAndLoginRequiredMixin,DeleteView):
    template_name = "leads/followup_delete.html"

    def get_queryset(self):
        user = self.request.user
        #query followUp of the lead
        if user.is_organizor:
            queryset = FollowUp.objects.filter(
                lead__organization = user.userprofile
            )
        else:
            queryset = FollowUp.objects.filter(
                lead__organization = user.agent.organization
            )
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk":self.get_object().lead.id})
