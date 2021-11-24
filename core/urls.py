from django.urls import path, include
from .           import views

urlpatterns = [
    path('', views.welcome_view, name="welcome_view"),
    path('checkAvailability/', views.APIScanner, name="api_scanner"),

    # DEBUGGING URLS
    path('return_redirect/', views.RedirectView, name="redirect"),
]