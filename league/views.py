import random
from urllib import request

from django.shortcuts import redirect, render
# Make sure both Team and Match are imported here!
from .models import Team, Match 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




def standings(request):
    teams = list(Team.objects.all())
    
    for team in teams:
        # 1. Decide how many total matches this team has played
        team.played = random.randint(4, 6)  # e.g., 5 games played
        
        # 2. Randomly pick a number of wins (cannot be more than matches played)
        team.wins = random.randint(0, team.played)
        
        # Calculate how many matches are left over after picking wins
        remaining_matches = team.played - team.wins
        
        # 3. Randomly pick a number of draws out of the remaining matches
        team.draws = random.randint(0, remaining_matches)
        
        # 4. Whatever matches are left over must be losses
        team.losses = remaining_matches - team.draws
        
        # 5. Apply the official football scoring rules!
        team.points = (team.wins * 3) + (team.draws * 1) + (team.losses * 0)

    # Sort the teams by points (highest first)
    sorted_teams = sorted(teams, key=lambda x: x.points, reverse=True)

    context = {'teams': sorted_teams}
    
    return render(request, 'league/standings.html', context)
    
    

# Add this brand-new function right below standings!
def match_results(request):
    
    # 1. Fetch all teams from your database
    teams = list(Team.objects.all())
    
    if len(teams) < 20:
        # Safety fallback if you haven't added all 20 teams to the database yet
        return render(request, 'league/matches.html', {'error': 'Please add all 20 teams in the admin panel first.'})
        
    random.shuffle(teams)

    num_teams = len(teams)
    total_rounds = num_teams - 1  # 19 rounds for 20 teams
    matches_per_round = num_teams // 2  # 10 matches per round

    schedule = {}

    # 2. Execute the Circle Method Rotation
    for round_num in range(total_rounds):
        matchday_label = f"Matchday {round_num + 1}"
        schedule[matchday_label] = []
    
        # ⭐ FIXED: This loop is now properly indented INSIDE the round_num loop
        for i in range(matches_per_round):
            home_team = teams[i]
            away_team = teams[num_teams - 1 - i]
            
            # Generate scores for the played match
            home_score = random.randint(0, 4)
            away_score = random.randint(0, 4)
            
            # Decide a random match status
            status = random.choice(['FT', 'FT', 'LIVE', 'HT'])
            
            schedule[matchday_label].append({
                'home_team': home_team.name,
                'away_team': away_team.name,
                'home_score': home_score,
                'away_score': away_score,
                'status': status
            })
            
        # ⭐ FIXED: The rotation step must happen inside the round loop after pairs are made
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        
    return render(request, 'league/matches.html', {'schedule': schedule})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Saves the new user directly to the database
            login(request, user) # Automatically log them in after signing up
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'league/signup.html', {'form': form})

# 2. LOG IN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'league/login.html', {'form': form})

# 3. LOG OUT VIEW
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')
    
def home(request):
    return render(request, 'league/home.html')
