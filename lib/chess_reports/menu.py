from .. import views

from tinydb import TinyDB, where


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
            pass
            # return HomeController()
        # quitter le programme
        elif next_action == "4":
            pass
            # return EndController()
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
            pass
            # return EndController()
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
            pass
            # return EndController()

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
