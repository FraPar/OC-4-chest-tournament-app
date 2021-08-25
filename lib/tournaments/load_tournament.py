from tinydb import TinyDB, where

from .. import views

from .controller_tournament import TournamentCreationController

class LoadTournament:
    """Contrôleur reponsable du chargement d'un tournoi déjà commencé"""

    def __init__(self):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.view = views.HomeView()

    def run(self):
        # on vérifie qu'il y a un tournoi dans la BDD
        if len(self.tournament_table.all()) == 0:
            print("Pas de tournois joués")
            pass
            # return HomeController()
        else:
            # activation de la variable permettant le chargement de tournoi
            load_state = True
            # listing de l'ensemble des tournois renseignés dans la BDD
            for datas in self.tournament_table.all():
                print("Tournoi : " + str(datas.get('Tournament_Id')) + " | Nom : " + str(datas.get('Name')))
            # demande à l'utilisateur du choix de l'ID de son tournoi
            tournament_choice = input("Séléctionnez le tournoi (ID):")

            tournament_index = int(tournament_choice)
            # recherche du tournoi choisi par l'utilisateur
            this_tournament = self.tournament_table.search(where
                                                           ("Tournament_Id") == tournament_index)[0]
            # mise en mémoire de l'étape de la sauvegarde du tournoi
            save_step = this_tournament["save_step"]
            # mise en place des variables nécessaires au fonctionnement
            # de la fonction de reprise de tournoi
            middle_number_players = 0
            first_half_players = []
            second_half_players = []
            total_match = []
            players_sorted = []
            match = []
            player_list = []
            # si les joueurs ont déjà été choisi, il faut renseigner certaines variables
            if save_step >= 2:
                player_list = [1, 2, 3, 4, 5, 6, 7, 8]
                middle_number_players = int(len(self.tournament_table.search
                                                (where("Tournament_Id") == tournament_index)[0]["players"])/2)
                first_half_players = player_list[:middle_number_players]
                second_half_players = player_list[middle_number_players:]
            # si un match a déjà été joué, il faut renseigner des variables supplémentaires
            if save_step >= 3:
                total_match = this_tournament["matchs"]
                # on charge le dernier round joué
                match = this_tournament["matchs"][-4:]
                players_to_sort = []
                for datas in match:
                    players_to_sort.append(datas[0])
                    players_to_sort.append(datas[1])
                # Tri des joueurs par rang
                players_to_sort.sort()
                # Tri des joueurs par rang et par score
                players_to_sort.sort(key=self.get_score, reverse=True)
                players_sorted = players_to_sort

            return TournamentCreationController(
                load_state, save_step, tournament_index,
                middle_number_players, first_half_players,
                second_half_players, total_match, players_sorted,
                match, player_list)

    # permet le tri par rang et par score
    def get_score(self, elem):
        return elem[1]