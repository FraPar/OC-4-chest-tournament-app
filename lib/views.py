class HomeView:
    """Vue responsable d'afficher le menu d'accueil."""

    @staticmethod
    def render():
        print(
            "Menu d'accueil\n"
            "==============\n"
            "1. Créer un nouveau tournoi (manuel)\n"
            "2. Créer un nouveau joueur (manuel)\n"
            "3. Créer un nouveau rapport\n"
            "4. Reprendre un tournoi\n"
            "5. Quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class ManualTournamentCreationView:
    """Vue responsable de l'affichage du menu de création de tournoi."""

    def render(self):
        print(
            "Menu de création d'un nouveau tournoi (manuel)\n"
            "==============================\n"
            "1. créer un tournoi\n"
            "2. retour à l'accueil\n"
            "3. quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class PlayerMenuView:
    """Vue responsable de l'affichage du menu de creation de joueurs."""

    def render(self):
        print(
            "Menu de création d'un joueur (manuel)\n"
            "==============================\n"
            "1. créer un joueur\n"
            "2. retour à l'accueil\n"
            "3. quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class ReportMenuView:
    """Vue responsable de l'affichage du menu de creation de joueurs."""

    def render(self):
        print(
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


class EndView:
    """Vue responsable de l'affichage de menu de fin d'application."""

    def render(self):
        print("Voulez-vous vraiment quitter l'application ?")

    def get_user_choice(self):
        return input("oui ou non ? ")

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")
