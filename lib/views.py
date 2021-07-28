class HomeView:
    """Vue responsable d'afficher le menu d'accueil."""
    
    @staticmethod
    def render():
        print(
            "Menu d'accueil\n"
            "==============\n"
            "1. Créer un nouveau tournoi (automatique)\n"
            "2. Créer un nouveau tournoi (manuel)\n"
            "3. Créer un nouveau joueur (manuel)\n"
            "4. Reprendre un tournoi (manuel)\n"
            "5. Quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class TournamentCreationView:
    """Vue responsable de l'affichage du menu de création de tournoi."""

    def render(self):
        print(
            "Menu de création d'un nouveau tournoi (manuel)\n"
            "==============================\n"
            "1. retour à l'accueil\n"
            "2. quitter le programme\n"
        )

    def get_user_choice(self):
        return input("Que voulez-vous faire ? ").lower()

    def notify_invalid_choice(self):
        print("Choix non valable !\n\n")


class PlayerCreationView:
    """Vue responsable de l'affichage du menu de creation de joueurs."""

    def render(self):
        print(
            "Menu de création d'un joueur (manuel)\n"
            "==============================\n"
            "1. retour à l'accueil\n"
            "2. quitter le programme\n"
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