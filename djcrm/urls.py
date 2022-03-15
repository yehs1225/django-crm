from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import(
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)
from django.urls import path,include
from leads.views import landing_page,LandingPageView,SignupView,DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LandingPageView.as_view(),name='landing-page'),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('leads/',include('leads.urls',namespace="leads")),
    path('agents/',include('agents.urls',namespace="agents")),
    path('signup/',SignupView.as_view(),name='signup'),  
    path('login/',LoginView.as_view(),name='login'),   
    path('logout/',LogoutView.as_view(),name='logout'),   
    path('password-reset/',PasswordResetView.as_view(),name='password-reset'),   
    path('password-reset-confirm/<uidb64>/<token>',PasswordResetConfirmView.as_view(),name='password-reset-confirm'),   
    path('password-reset-done/',PasswordResetDoneView.as_view(),name='password_reset_done'),   
    path('password-reset-complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
