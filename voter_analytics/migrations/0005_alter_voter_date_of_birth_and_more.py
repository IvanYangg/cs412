# Generated by Django 5.1.2 on 2024-11-11 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0004_alter_voter_apartment_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='date_of_birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='date_of_registration',
            field=models.DateField(),
        ),
    ]
