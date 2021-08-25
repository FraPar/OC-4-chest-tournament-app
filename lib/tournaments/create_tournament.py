import random
from tinydb import TinyDB, where, Query

from .. import views

from ..players import PlayerCreationController
from .save_tournament import SaveStateTournament
from .controller_tournament import TournamentCreationController


class CreateTournament:
    """Contrôleur reponsable de la création d'un nouveau tournoi"""

    def __init__(self):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.view = views.HomeView()

    def run(self):
        # mise en place des variables nécessaires au fonctionnement
        # de la fonction de reprise de tournoi
        load_state = False
        save_step = 0
        middle_number_players = 0
        first_half_players = []
        second_half_players = []
        total_match = []
        players_sorted = []
        match = []
        player_list = []

        # teste de présence de données dans la BDD des tournois
        if len(self.tournament_table.all()) == 0:
            last_index = 0
        else:
            # on définie le prochain ID utilisable de la table des tournois
            last_index = self.tournament_table.all()[-1]["Tournament_Id"] + 1

        tournament_index = last_index

        # lancement de la class permettant de créer un tournoi
        return TournamentCreationController(
                load_state, save_step, tournament_index,
                middle_number_players, first_half_players, second_half_players,
                total_match, players_sorted, match, player_list)
