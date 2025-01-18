from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Manuscript


class ManuscriptListView(ListView):
    model = Manuscript
    template_name = "manuscripts/manuscript_list.html"


class ManuscriptDetailView(DetailView):
    model = Manuscript
    template_name = "manuscripts/manuscript_detail.html"
