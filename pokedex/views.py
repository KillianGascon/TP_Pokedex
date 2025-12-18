from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Pokemon, Team
import random


def index(request):
    query = request.GET.get('q', '')
    pokemon_list = Pokemon.objects.all().order_by('number')
    
    if query:
        pokemon_list = pokemon_list.filter(
            Q(name__icontains=query) | Q(number__icontains=query)
        )
    
    paginator = Paginator(pokemon_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pokedex/index.html', {
        'page_obj': page_obj,
        'query': query
    })

def pokemon_detail(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, number=pokemon_id)
    return render(request, 'pokedex/pokemon_detail.html', {'pokemon': pokemon})

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'pokedex/team_list.html', {'teams': teams})

def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Team.objects.create(name=name)
            return redirect('pokedex:team_list')
    return render(request, 'pokedex/create_team.html')

def add_pokemon_to_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        pokemon = get_object_or_404(Pokemon, number=pokemon_id)
        if team.pokemons.count() < 5:
            team.pokemons.add(pokemon)
        return redirect('pokedex:team_list')
    
    query = request.GET.get('q', '')
    pokemon_list = Pokemon.objects.all().order_by('number')
    if query:
        pokemon_list = pokemon_list.filter(
            Q(name__icontains=query) | Q(number__icontains=query)
        )
    
    paginator = Paginator(pokemon_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pokedex/add_to_team.html', {
        'team': team,
        'page_obj': page_obj,
        'query': query
    })

def remove_pokemon_from_team(request, team_id, pokemon_id):
    team = get_object_or_404(Team, id=team_id)
    pokemon = get_object_or_404(Pokemon, number=pokemon_id)
    if request.method == 'POST':
        team.pokemons.remove(pokemon)
    return redirect('pokedex:team_list')

def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        team.delete()
    return redirect('pokedex:team_list')

def combat(request):
    """Team selection page for combat"""
    teams = Team.objects.filter(pokemons__isnull=False).distinct()
    return render(request, 'pokedex/combat.html', {'teams': teams})

def team_battle(request, team1_id, team2_id):
    """Turn-based team battle with player interaction"""
    team1 = get_object_or_404(Team, id=team1_id)
    team2 = get_object_or_404(Team, id=team2_id)
    
    battle_key = f'battle_{team1_id}_{team2_id}'
    
    if request.method == 'POST' and 'reset' in request.POST:
        if battle_key in request.session:
            del request.session[battle_key]
        return redirect('pokedex:team_battle', team1_id=team1_id, team2_id=team2_id)
    
    # Initialize battle state
    if battle_key not in request.session:
        t1_list = list(team1.pokemons.values_list('number', flat=True))
        t2_list = list(team2.pokemons.values_list('number', flat=True))
        request.session[battle_key] = {
            'team1_hp': {str(p.number): p.stats.get('hp', 50) * 2 for p in team1.pokemons.all()},
            'team2_hp': {str(p.number): p.stats.get('hp', 50) * 2 for p in team2.pokemons.all()},
            'current_pokemon1': t1_list[0] if t1_list else None,
            'current_pokemon2': t2_list[0] if t2_list else None,
            'log': [],
            'winner': None,
            'turn': 1
        }
    
    battle = request.session[battle_key]
    current_p1 = Pokemon.objects.filter(number=battle['current_pokemon1']).first()
    current_p2 = Pokemon.objects.filter(number=battle['current_pokemon2']).first()
    
    # Process player action
    if request.method == 'POST' and not battle['winner']:
        action = request.POST.get('action')
        
        if action == 'attack' and current_p1 and current_p2:
            # Player attacks
            attack_stat = current_p1.stats.get('attack', 50)
            defense_stat = current_p2.stats.get('defense', 50)
            damage = max(10, int((attack_stat / defense_stat) * 20 + random.randint(-5, 10)))
            
            p2_key = str(battle['current_pokemon2'])
            battle['team2_hp'][p2_key] = max(0, battle['team2_hp'][p2_key] - damage)
            battle['log'].append(f"Tour {battle['turn']}: {current_p1.name} attaque {current_p2.name} pour {damage} dégâts!")
            
            if battle['team2_hp'][p2_key] <= 0:
                battle['log'].append(f"{current_p2.name} est K.O.!")
                next_p2 = None
                for p in team2.pokemons.all():
                    if battle['team2_hp'].get(str(p.number), 0) > 0:
                        next_p2 = p.number
                        break
                battle['current_pokemon2'] = next_p2
                if not next_p2:
                    battle['winner'] = team1.name
                    battle['log'].append(f"🏆 {team1.name} remporte le combat!")
        
        elif action == 'switch':
            switch_to = request.POST.get('switch_to')
            if switch_to:
                switch_to = int(switch_to)
                if battle['team1_hp'].get(str(switch_to), 0) > 0:
                    old_name = current_p1.name if current_p1 else "?"
                    battle['current_pokemon1'] = switch_to
                    new_pokemon = Pokemon.objects.filter(number=switch_to).first()
                    battle['log'].append(f"Tour {battle['turn']}: {old_name} rentre, {new_pokemon.name} entre!")
        
        # AI turn
        if not battle['winner'] and battle['current_pokemon2']:
            current_p2 = Pokemon.objects.filter(number=battle['current_pokemon2']).first()
            current_p1 = Pokemon.objects.filter(number=battle['current_pokemon1']).first()
            
            if current_p1 and current_p2:
                attack_stat = current_p2.stats.get('attack', 50)
                defense_stat = current_p1.stats.get('defense', 50)
                damage = max(10, int((attack_stat / defense_stat) * 20 + random.randint(-5, 10)))
                
                p1_key = str(battle['current_pokemon1'])
                battle['team1_hp'][p1_key] = max(0, battle['team1_hp'][p1_key] - damage)
                battle['log'].append(f"      {current_p2.name} riposte pour {damage} dégâts!")
                
                if battle['team1_hp'][p1_key] <= 0:
                    battle['log'].append(f"{current_p1.name} est K.O.!")
                    next_p1 = None
                    for p in team1.pokemons.all():
                        if battle['team1_hp'].get(str(p.number), 0) > 0:
                            next_p1 = p.number
                            break
                    battle['current_pokemon1'] = next_p1
                    if not next_p1:
                        battle['winner'] = team2.name
                        battle['log'].append(f"🏆 {team2.name} remporte le combat!")
        
        battle['turn'] += 1
        request.session.modified = True
    
    # Prepare template data
    team1_pokemon_hp = []
    for p in team1.pokemons.all():
        hp = battle['team1_hp'].get(str(p.number), 0)
        max_hp = p.stats.get('hp', 50) * 2
        team1_pokemon_hp.append({'pokemon': p, 'hp': hp, 'max_hp': max_hp, 'alive': hp > 0})
    
    team2_pokemon_hp = []
    for p in team2.pokemons.all():
        hp = battle['team2_hp'].get(str(p.number), 0)
        max_hp = p.stats.get('hp', 50) * 2
        team2_pokemon_hp.append({'pokemon': p, 'hp': hp, 'max_hp': max_hp, 'alive': hp > 0})
    
    current_p1 = Pokemon.objects.filter(number=battle['current_pokemon1']).first()
    current_p2 = Pokemon.objects.filter(number=battle['current_pokemon2']).first()
    
    return render(request, 'pokedex/team_battle.html', {
        'team1': team1,
        'team2': team2,
        'current_p1': current_p1,
        'current_p2': current_p2,
        'current_p1_hp': battle['team1_hp'].get(str(battle['current_pokemon1']), 0) if battle['current_pokemon1'] else 0,
        'current_p1_max_hp': current_p1.stats.get('hp', 50) * 2 if current_p1 else 1,
        'current_p2_hp': battle['team2_hp'].get(str(battle['current_pokemon2']), 0) if battle['current_pokemon2'] else 0,
        'current_p2_max_hp': current_p2.stats.get('hp', 50) * 2 if current_p2 else 1,
        'team1_pokemon_hp': team1_pokemon_hp,
        'team2_pokemon_hp': team2_pokemon_hp,
        'battle_log': battle['log'][-10:],
        'winner': battle['winner'],
        'turn': battle['turn']
    })
