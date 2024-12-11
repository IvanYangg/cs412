# Generated by Django 5.1.2 on 2024-12-05 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=20)),
                ('minutes_per_game', models.FloatField()),
                ('points_per_game', models.FloatField()),
                ('assists_per_game', models.FloatField()),
                ('rebounds_per_game', models.FloatField()),
                ('three_pointers_made_per_game', models.FloatField()),
                ('steals_per_game', models.FloatField()),
                ('blocks_per_game', models.FloatField()),
                ('turnovers_per_game', models.FloatField()),
                ('fouls_per_game', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=3)),
                ('avg_ppg', models.FloatField()),
                ('avg_ppg_conceded', models.FloatField()),
                ('avg_three_point_attempted', models.FloatField()),
                ('avg_three_point_made', models.FloatField()),
                ('avg_three_point_percentage', models.FloatField()),
                ('avg_free_throw_attempted', models.FloatField()),
                ('avg_rebounds_per_game', models.FloatField()),
                ('avg_assists_per_game', models.FloatField()),
                ('avg_steals_per_game', models.FloatField()),
                ('avg_blocks_per_game', models.FloatField()),
                ('avg_turnovers_per_game', models.FloatField()),
                ('avg_fouls_per_game', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PlayerGameLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('minutes', models.IntegerField()),
                ('points', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('rebounds', models.IntegerField()),
                ('three_pointers_made', models.IntegerField()),
                ('three_pointers_attempted', models.IntegerField()),
                ('steals', models.IntegerField()),
                ('blocks', models.IntegerField()),
                ('turnovers', models.IntegerField()),
                ('fouls', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.team'),
        ),
        migrations.CreateModel(
            name='Matchup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1_image_url', models.CharField(max_length=200)),
                ('team2_image_url', models.CharField(max_length=200)),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matchups_as_team1', to='project.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matchups_as_team2', to='project.team')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserWatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.userprofile')),
            ],
        ),
    ]