from django.urls import path
from . import views

urlpatterns = [
    path("", views.ManuscriptListView.as_view(), name="manuscript-list"),
    path("<int:pk>/", views.ManuscriptDetailView.as_view(), name="manuscript-detail"),
]
