import views

from tournaments import TournamentCreationController, CreateTournament, LoadTournament
from players import PlayerMenuController
from chess_reports import ReportMenuController

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
