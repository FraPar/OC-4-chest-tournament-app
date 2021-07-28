from . import views


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
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            #mettre la version création automatique de tournoi
            pass
        elif next_action == "2":
            return TournamentCreationController()
        elif next_action == "3":
            return PlayerCreationController()
        elif next_action == "4":
            #mettre la reprise de tournoi en cours (pas encore mise en place)
            pass
        else:
            self.view.notify_invalid_choice()
            return HomeController()


class TournamentCreationController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    tournoi.
    """

    def __init__(self):
        self.view = views.TournamentCreationView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return HomeController()
        elif next_action == "2":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return TournamentCreationController()


class PlayerCreationController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self):
        self.view = views.PlayerCreationView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return HomeController()
        elif next_action == "2":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerCreationController()


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
