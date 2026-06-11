from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    # This method tells Django how to display the team's name in the Admin panel
    def __str__(self):
        return self.name

class Match(models.Model):
    # ForeignKeys link this Match to specific Teams in the Team database table
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    
    # A boolean to check if the match has happened yet
    is_played = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"