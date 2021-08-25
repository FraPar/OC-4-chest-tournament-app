from .. import views

from tinydb import TinyDB, where, Query

# from . import PlayerMenuController


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
        # return PlayerMenuController()

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
