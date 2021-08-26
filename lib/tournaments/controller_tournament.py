import random
from tinydb import TinyDB, where

from .. import views

from .model_save_tournament import SaveStateTournament
from ..rounds.first_round import FirstRound
from .adding_players_in_tournament import AddPlayerInTournament
from ..rounds.other_rounds import OtherRounds
from .sort_tournament_data import SortTournamentData


class TournamentCreationController:
    """Création d'un nouveau tournoi"""

    def __init__(self, load_state, save_step,
                 tournament_index, middle_number_players,
                 first_half_players, second_half_players,
                 total_match, players_sorted, match, player_list):

        self.view = views.TournamentMenuView()
        self.db = TinyDB('db.json')

        # variable de chargement de tournoi
        self.load_state = load_state
        self.save_step = save_step

        # --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')

        # --- CREATION DE LA LISTE DES JOUEURS --- #
        self.player_list = player_list
        self.player_list_to_sort = []
        self.player_list_by_rank = []

        # --- DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE --- #
        self.middle_number_players = middle_number_players
        self.first_half_players = first_half_players
        self.second_half_players = second_half_players

        # --- Définition des variables générales--- #
        self.tournament_index = tournament_index
        self.number_of_players = 0
        self.last_index = 0
        self.player_rank = 0
        self.player_match = []
        self.total_match = total_match
        self.players_to_sort = []
        self.players_sorted = players_sorted
        self.match = match
        self.match_to_play = []
        self.player_order = []

    def run(self):

        # --- ETAPE 0 DE SAUVEGARDE --- #
        SaveStateTournament.starting_tournament(self)

        # --- ETAPE 1 DE SAUVEGARDE --- #
        AddPlayerInTournament.adding_players_in_tournament(self)

        # --- ETAPE 2 DE SAUVEGARDE --- #
        FirstRound.playing_first_round(self)

        # impression des scores des joueurs du tournoi
        SortTournamentData.get_tournament_ranking(self)

        # Définition de l'étape de sauvegarde à 3, après le Round 1
        if (self.load_state is True and self.save_step == 2) or self.load_state is False:
            SaveStateTournament.save_round_one(self)

        # --- ETAPE 3 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 3) or self.load_state is False:

            print("\n ROUND 2 :")

            # Lancement de la fonction permettant de jouer un round complet
            OtherRounds.get_player_match(self)

            # impression des scores des joueurs du tournoi
            SortTournamentData.get_tournament_ranking(self)

            # Définition de l'étape de sauvegarde à 4, après le Round 2
            SaveStateTournament.save_round_two(self)

            # --- ETAPE 4 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 4) or self.load_state is False:

            print("\n ROUND 3 : ")

            OtherRounds.get_player_match(self)
            SortTournamentData.get_tournament_ranking(self)

            # Définition de l'étape de sauvegarde à 5, après le Round 3
            SaveStateTournament.save_round_three(self)


            # --- ETAPE 5 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 5) or self.load_state is False:

            print("\n ROUND 4 :")

            OtherRounds.get_player_match(self)
            SortTournamentData.get_tournament_ranking(self)

            # Définition de l'étape de sauvegarde à 6, après le Round 4
            SaveStateTournament.save_round_four(self)

    # permet le tri par rang et par score
    def get_score(self, elem):
        return elem[1]
