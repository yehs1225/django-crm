from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'agents'

urlpatterns = [
    path('',AgentListView.as_view(),name='agent-list'),
    path('create/',AgentCreateView.as_view(),name='agent-create'),
    path('<int:pk>/',AgentDetailView.as_view(),name='agent-detail'),
    # path('',LeadVistView.as_view(),name='lead-list'),
    # path('<int:pk>/',LeadDetailView.as_view(),name='lead-detail'),
    path('<int:pk>/update/',AgentUpdateView.as_view(),name='agent-update'),
    path('<int:pk>/delete/',AgentDeleteView.as_view(),name='agent-delete'),
    # path('create/',LeadCreateView.as_view(),name='lead-create'),
]