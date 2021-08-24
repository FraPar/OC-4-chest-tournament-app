class HomeView:
    """Vue responsable d'afficher le menu d'accueil."""

    @staticmethod
    def render():
        print(
            "\n"
            "Menu d'accueil\n"
            "==============\n"
            "1. Créer un nouveau tournoi\n"
            "2. Créer un nouveau joueur\n"
            "3. Créer un nouveau rapport\n"
            "4. Reprendre un tournoi\n"
            "5. Quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class TournamentMenuView:
    """Vue responsable de l'affichage de la création d'un
    tournoi."""

    def render(self):
        print(
            "\n"
            "Menu de création d'un joueur\n"
            "==============================\n"
            "1. Ajouter un joueur déjà éxistant\n"
            "2. Créer un nouveau joueur"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class PlayerMenuView:
    """Vue responsable de l'affichage du menu de creation de joueurs."""

    def render(self):
        print(
            "\n"
            "Menu de création d'un joueur\n"
            "==============================\n"
            "1. créer un joueur\n"
            "2. changer le classement d'un joueur\n"
            "3. retour à l'accueil\n"
            "4. quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class ReportMenuView:
    """Vue responsable de l'affichage du menu de creation de rapport."""

    def render(self):
        print(
            "\n"
            "Menu de création d'un rapport\n"
            "==============================\n"
            "1. créer un rapport sur l'ensemble des joueurs\n"
            "2. créer un rapport sur l'ensemble des tournois\n"
            "3. retour à l'accueil\n"
            "4. quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class PlayerReportMenuView:
    """Vue responsable de l'affichage du menu de creation de rapport
    sur les joueurs."""

    def render(self):
        print(
            "\n"
            "Voulez-vous :\n"
            "==============================\n"
            "1. Trier l'ensemble par ordre Alphabétique\n"
            "2. Trier l'ensemble par Rang\n"
            "3. Retourner au menu\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def get_player_data(self, datas):
        return print("ID : " + str(datas["Player_Id"]) +
                     ", Nom : " + str(datas["player_name"]) +
                     ", Prénom : " + str(datas["player_surname"]) +
                     ", Date de naissance : " + str(datas["player_birthday"]) +
                     ", Genre : " + str(datas["player_gender"]) +
                     ", Classement : " + str(datas["player_rank"]))

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class TournamentReportMenuView:
    """Vue responsable de l'affichage du menu de creation de rapport
    sur les joueurs."""

    def menu_render(self):
        print(
            "\n"
            "Voulez-vous :\n"
            "==============================\n"
            "1. Voir les tours d'un tournoi spécifique\n"
            "2. Voir les matchs d'un tournoi spécifique\n"
            "3. Voir les joueurs d'un tournoi spécifique\n"
            "4. Retourner au menu\n"
        )

    def sort_menu_render(self):
        print(
            "\n"
            "Voulez-vous :\n"
            "==============================\n"
            "1. Trier l'ensemble par ordre Alphabétique\n"
            "2. Trier l'ensemble par Rang\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def get_user_id_choice(self):
        return input("Séléctionnez le tournoi (ID): ").lower()

    def get_tournament_data(self, datas):
        return print("ID : " + str(datas["Tournament_Id"]) +
                     ", Nom : " + str(datas["Name"]) +
                     ", Lieu : " + str(datas["Location"]) +
                     ", Date : " + str(datas["Date"]) +
                     ", Nombre de rounds : " + str(datas["Round"]) +
                     ", Type de temps : " + str(datas["Time"]) +
                     ", Description : " + str(datas["Description"]))

    def get_player_data(self, datas):
        return print("ID : " + str(datas["Player_Id"]) +
                     ", Nom : " + str(datas["player_name"]) +
                     ", Prénom : " + str(datas["player_surname"]) +
                     ", Date de naissance : " + str(datas["player_birthday"]) +
                     ", Genre : " + str(datas["player_gender"]) +
                     ", Classement : " + str(datas["player_rank"]))

    def get_tournament_rounds(self, datas):
        # on charge le 1er Round si une sauvegarde a été faites après celui-ci
        if datas["save_step"] >= 3:
            self.get_tournament_players(datas)
            print("")
            print("Matchs joués :")
            print("Round 1 :")
            print(str(datas["matchs"][:4]))
        # on charge le 2eme Round si une sauvegarde a été faites après celui-ci
        if datas["save_step"] >= 4:
            print("Round 2 :")
            print(str(datas["matchs"][4:8]))
        # on charge le 3eme Round si une sauvegarde a été faites après celui-ci
        if datas["save_step"] >= 5:
            print("Round 3 :")
            print(str(datas["matchs"][8:-4]))
        # on charge le dernier Round si une sauvegarde a été faites après celui-ci
        if datas["save_step"] >= 6:
            print("Round 4 :")
            print(str(datas["matchs"][-4:]))

    def get_tournament_matchs(self, datas):
        print("")
        print("Matchs joués :")
        print(str(datas["matchs"]))

    def get_tournament_players(self, datas):
        print("")
        print("Joueurs : " + str(datas["players"]))

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class EndView:
    """Vue responsable de l'affichage de menu de fin d'application."""

    def render(self):
        print("Voulez-vous vraiment quitter l'application ?")

    def get_user_choice(self):
        return input("oui ou non ? ")

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")
