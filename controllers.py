import views

from tournaments import TournamentCreationController, CreateTournament
from players import PlayerMenuController

from tinydb import TinyDB, where, Query


class ApplicationController:
    """Représente l'application elle-même et permet de la démarrer."""

    def __init__(self):
        """Initialise la classe principale de l'application."""
        self.current_controller = HomeController()

    def start(self):
        """Démarre l'application."""
        while self.current_controller is not None:
            next_controller = self.current_controller.run()
            self.current_controller = next_controller


class HomeController:
    """Contrôleur responsable de gérer le menu d'accueil."""

    def __init__(self):
        self.view = views.HomeView()

    def run(self):
        # Menu d'accueil
        self.view.render()
        next_action = self.view.get_user_choice()

        # Créer un nouveau tournoi
        if next_action == "1":
            return CreateTournament()

        # Créer un nouveau joueur
        elif next_action == "2":
            return PlayerMenuController()

        # Créer un nouveau rapport
        elif next_action == "3":
            return ReportMenuController()

        # Reprendre un tournoi
        elif next_action == "4":
            return LoadTournament()
        # Quitter le programme
        elif next_action == "5":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


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
            return HomeController()
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


class PlayerRankController:
    """Contrôleur responsable de gérer le menu de
    modification du rang d'un joueur.
    """

    def __init__(self):
        self.view = views.TournamentReportMenuView()
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')

    def run(self):
        if len(self.player_pool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            self.rank_player()
        return PlayerMenuController()

    def rank_player(self):
        # visualisation des joueurs présent dans la BDD
        player_pool = self.player_pool.all()
        for datas in player_pool:
            self.view.get_player_data(datas)

        wrong_choice = True
        while wrong_choice is True:
            try:
                player_choice = int(input("Séléctionnez le joueur (ID):"))
                # on va chercher l'ID du joueur dans la BDD des joueurs
                user_choice = self.player_pool.search(where("Player_Id") == player_choice)
                wrong_choice = False
                player_rank = str(user_choice[0]["player_rank"])
            except (IndexError, ValueError):
                print("Veuillez entrer un ID correcte")
                wrong_choice = True
                continue

        wrong_choice = True
        while wrong_choice is True:
            try:
                print("Rang actuel du joueur : " + player_rank)
                newRank = abs(int(input("Quel est le nouveau rang du joueur?")))
                wrong_choice = False
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                wrong_choice = True
                continue

        player_data = {"player_rank": newRank}
        # Mise à jour du joueur correspondant dans la BDD des joueurs
        self.player_pool.update(player_data,
                                Query().Player_Id == player_choice)


class ReportMenuController:
    """Contrôleur responsable de gérer le menu de rapports.
    """

    def __init__(self):
        self.view = views.ReportMenuView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        # créer un rapport sur l'ensemble des joueurs
        if next_action == "1":
            return ReportAllPlayerController()
        # créer un rapport sur l'ensemble des tournois
        elif next_action == "2":
            return ReportTournamentController()
        # retour à l'accueil
        elif next_action == "3":
            return HomeController()
        # quitter le programme
        elif next_action == "4":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return ReportMenuController()


class ReportAllPlayerController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec l'ensemble des acteurs.
    """

    def __init__(self):
        self.view = views.PlayerReportMenuView()
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')
        self.player_pool_ddb = self.player_pool.all()

    def run(self):
        self.view.render()
        self.next_action = self.view.get_user_choice()
        if len(self.player_pool_ddb) == 0:
            print("Pas de joueurs crées")
        else:
            self.creation_report()
        return ReportMenuController()

    def creation_report(self):
            user_choice = self.next_action
            # Trier l'ensemble par ordre Alphabétique
            if user_choice == "1":
                self.player_sort_by_name()
            # Trier l'ensemble par Rang
            elif user_choice == "2":
                self.player_sort_by_rank()
            # retour à l'accueil
            elif user_choice == "3":
                return EndController()
            else:
                self.view.notify_invalid_choice()
                return ReportAllPlayerController()

    # Fonction de tri des joueurs par Noms
    def player_sort_by_name(self):
        sorted_list = sorted(self.player_pool_ddb, key=lambda item: item["player_name"])
        for datas in sorted_list:
            self.view.get_player_data(datas)

    # Fonction de tri des joueurs par Rang
    def player_sort_by_rank(self):
        sorted_list = sorted(self.player_pool_ddb, key=lambda item: item["player_rank"])
        for datas in sorted_list:
            self.view.get_player_data(datas)


class ReportTournamentController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec tous les tournois.
    """

    def __init__(self):
        self.view = views.TournamentReportMenuView()
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')
        self.player_in_tournament = []

    def run(self):
        self.view.menu_render()
        self.next_action = self.view.get_user_choice()
        # on vérifie qu'il y a un tournoi dans la BDD
        if len(self.tournament_table.all()) == 0:
            print("Pas de tournois joués")
        else:
            self.creation_report()
        return ReportMenuController()

    def creation_report(self):
        # Listing de tous les tournois dans la BDD des tournois
        for datas in self.tournament_table.all():
            self.view.get_tournament_data(datas)
        user_choice = self.next_action

        # Voir les tours d'un tournoi spécifique
        try:
            tournament_choice = int(input("Séléctionnez le tournoi (ID):"))
            # on va chercher l'ID du tournoi dansl a BDD des tournois
            tournament_user_choice = self.tournament_table.search(where("Tournament_Id") == tournament_choice)[0]
        except (IndexError, ValueError, UnboundLocalError):
            print("Veuillez entrer un ID correcte")

        # Voir les tours d'un tournoi spécifique
        if user_choice == "1":
            self.view.get_tournament_data(tournament_user_choice)
            self.view.get_tournament_rounds(tournament_user_choice)

        # Voir les matchs d'un tournoi spécifique
        elif user_choice == "2":
            self.view.get_tournament_data(tournament_user_choice)
            self.view.get_tournament_players(tournament_user_choice)
            self.view.get_tournament_matchs(tournament_user_choice)

        # Voir les joueurs d'un tournoi spécifique
        elif user_choice == "3":
            self.tournament_player(tournament_user_choice)

        # Retour au menu d'accueil
        elif user_choice == "4":
            return EndController()

        else:
            self.view.notify_invalid_choice()
            return ReportTournamentController()

    def tournament_player(self, tournament_user_choice):
        if tournament_user_choice["save_step"] >= 2:
            for datas in tournament_user_choice["players"]:
                self.player_in_tournament.append(self.player_pool.search(where("Player_Id") == datas[1])[0])
            self.view.sort_menu_render()

            wrong_choice = True
            while wrong_choice is True:
                user_choice = self.view.get_user_id_choice()
                # Trier l'ensemble des joueurs du tournoi par ordre Alphabétiqu
                if user_choice == "1":
                    wrong_choice = False
                    sorted_list = sorted(self.player_in_tournament, key=lambda item: item["player_name"])
                    for datas in sorted_list:
                        self.view.get_player_data(datas)
                # Trier l'ensemble des joueurs du tournoi par rang
                elif user_choice == "2":
                    wrong_choice = False
                    sorted_list = sorted(self.player_in_tournament, key=lambda item: item["player_rank"])
                    for datas in sorted_list:
                        self.view.get_player_data(datas)
                else:
                    wrong_choice = True
                    print("Veuillez saisir une entrée valide")
                continue
        else:
            print("Aucun joueur n'a été inséré dans un match")


class EndController:
    """Contrôleur responsable de gérer la fin du programme."""

    def __init__(self):
        self.view = views.EndView()

    def run(self):
        self.view.render()
        choice = self.view.get_user_choice()
        if choice == "oui":
            return
        elif choice == "non":
            return HomeController()
        else:
            self.view.notify_invalid_choice()
            return EndController()
