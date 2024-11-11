# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom models and their data attributes that is used in this project

from django.db import models
from datetime import datetime

# Create your models here.
class Voter(models.Model):
    #identification
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.CharField(max_length=20)
    street_name = models.TextField()
    apartment_number = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=5)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    
    #party affiliation
    party_affiliation = models.CharField(max_length=5)
    precinct_number = models.CharField(max_length=5)

    # Previous election participation
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # Voter score
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    filename = '/Users/ivanyang/desktop/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    
    for line in f:
        fields = line.strip().split(',')

        try:
            # Create a new instance of Voter object with this record from CSV
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10].strip(),
                v20state=(fields[11].strip().upper() == "TRUE"),
                v21town=(fields[12].strip().upper() == "TRUE"),
                v21primary=(fields[13].strip().upper() == "TRUE"),
                v22general=(fields[14].strip().upper() == "TRUE"),
                v23town=(fields[15].strip().upper() == "TRUE"),
                voter_score=int(fields[16].strip())
            )
            voter.save() # commit to database
            print(f'Created result: {voter}')
            
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} voters.')