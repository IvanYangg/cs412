# Generated by Django 5.1.2 on 2024-11-11 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0005_alter_voter_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='apartment_number',
            field=models.CharField(max_length=50),
        ),
    ]