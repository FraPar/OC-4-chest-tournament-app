import views

from . import PlayerCreationController
from .change_rank import PlayerRankController
# from controllers import HomeController, EndController


class PlayerMenuController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self):
        self.view = views.PlayerMenuView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        # Création d'un joueur
        if next_action == "1":
            return PlayerCreationController()
        # Changer le classement d'un joueur
        elif next_action == "2":
            return PlayerRankController()
        # Retour au menu
        elif next_action == "3":
            pass
            # return HomeController()
        # Quitter le programme
        elif next_action == "4":
            pass
            # return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerMenuController()
