from django.urls import path
from . import views

urlpatterns = [
    path("this/", views.this, name="this"),
    path("trigger-workflow/", views.trigger_workflow, name="trigger_workflow"),
    path("google_auth/", views.google_auth, name="google_auth"),
]