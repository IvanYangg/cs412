# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom views that are used in this project

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

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
    
# Graphs view to create and render the plots
class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        qs = super().get_queryset()

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

        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for election in election_fields:
            if self.request.GET.get(election) == 'on':
                qs = qs.filter(**{election: True})

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Histogram for voter birth years
        years = [voter.date_of_birth.year for voter in self.object_list]
        counts = {year: years.count(year) for year in set(years)}
        # Generate the bar chart
        birth_year_hist = go.Bar(
            x=list(counts.keys()),
            y=list(counts.values()),
            name='Voter Birth Years'
        )
        title_text = f"Voter Distribution by Year of Birth (n=58769)"
        # obtain the graph as an HTML div
        graph_birthyears = plotly.offline.plot({"data": [birth_year_hist], "layout_title_text": title_text}, auto_open=False, output_type = "div")
        # send div as template context variable
        context['graph_birthyear_hist'] = graph_birthyears
        
        # Pie chart for party affiliation distribution
        party_affiliations = [voter.party_affiliation for voter in self.object_list if voter.party_affiliation]
        party_affiliation_counts = {party: party_affiliations.count(party) for party in set(party_affiliations)}
        # generate the Pie chart
        party_affiliation_pie = go.Pie(
            labels=list(party_affiliation_counts.keys()),
            values=list(party_affiliation_counts.values()),
            name='Party Affiliation'
        )
        title_text = f"Voter Distribution by Party Affiliation (n=58769)"
        # obtain the graph as an HTML div
        graph_party = plotly.offline.plot({"data": [party_affiliation_pie], "layout_title_text": title_text}, auto_open=False, output_type="div")
        
        # send div as template context variable
        context['graph_party_pie'] = graph_party

        # Histogram for voter participation in elections
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_participation = {field: sum(1 for voter in self.object_list if getattr(voter, field, False)) for field in election_fields}
        # generate the histogram
        election_hist = go.Bar(
            x=list(election_participation.keys()),
            y=list(election_participation.values()),
            name='Election Participation'
        )
        title_text = f"Vote Count by Election (n=58769)"
        # obtain the graph as an HTML div
        graph_elections = plotly.offline.plot({"data": [election_hist], "layout_title_text": title_text}, auto_open=False, output_type="div")
        # send div as template context variable
        context['graph_elections_hist'] = graph_elections
        
        context['birth_years'] = range(1920, 2005)
        context['elections'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        return context
