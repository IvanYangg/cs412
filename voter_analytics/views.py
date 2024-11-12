# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom views that are used in this project

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()

        # Filtering logic
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        
        if min_dob:
            qs = qs.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            qs = qs.filter(date_of_birth__year__lte=max_dob)
        if party_affiliation:
            qs = qs.filter(party_affiliation=party_affiliation)
        if voter_score:
            qs = qs.filter(voter_score=voter_score)

        # Election filters
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for election in election_fields:
            if self.request.GET.get(election) == 'on':
                qs = qs.filter(**{election: True})

        return qs

    # function to add additional context data to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birth_years'] = range(1920, 2005)
        context['elections'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        return context

# a custom class based view to display the details of a single voter
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
