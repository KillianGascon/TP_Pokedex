# Documentation du Pokédex

## Introduction
Application Pokédex développée en Python avec le framework **Django**. Elle utilise l'API **PokeAPI** pour récupérer les informations des 251 premiers Pokémon.

## Installation

1. **Prérequis**: Python 3.10+
2. **Installer les dépendances**:
   ```bash
   pip install django requests
   ```
3. **Initialiser la base de données**:
   ```bash
   python manage.py migrate
   ```
4. **Importer les Pokémon** (première utilisation):
   ```bash
   python manage.py import_pokemon
   ```
5. **Lancer le serveur**:
   ```bash
   python manage.py runserver
   ```
6. Ouvrir `http://127.0.0.1:8000/` dans un navigateur.

## Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| **Affichage** | Grille de Pokémon avec images et types |
| **Navigation** | Pagination pour parcourir les 251 Pokémon |
| **Recherche** | Recherche par nom ou numéro |
| **Détails** | Vue détaillée avec statistiques (HP, Attaque, etc.) |
| **Équipes** | Création d'équipes de **5 Pokémon** |
| **Combat** | Combat tour par tour entre 2 équipes |

## Système de Combat

Le système de combat permet d'affronter deux équipes:
- **Équipe 1**: Contrôlée par le joueur
- **Équipe 2**: Contrôlée par l'**IA**

### Actions disponibles:
1. **Attaquer**: Inflige des dégâts basés sur les stats Attaque/Défense
2. **Changer de Pokémon**: Remplacer le Pokémon actif par un autre de l'équipe

### Déroulement:
1. Le joueur choisit une action
2. L'IA riposte automatiquement
3. Quand un Pokémon atteint 0 HP, il est K.O.
4. L'équipe sans Pokémon valide perd

## Choix Techniques

- **Framework**: Django 6.0 pour sa robustesse et son ORM intégré.
- **Base de données**: SQLite (données importées localement pour performance).
- **Design**: CSS vanilla avec thème Pokémon (gradients, animations, badges).
- **API**: PokeAPI v2 pour les données officielles.
- **Combat IA**: L'adversaire attaque automatiquement chaque tour.
