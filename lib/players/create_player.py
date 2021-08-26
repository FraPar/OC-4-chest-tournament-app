from tinydb import TinyDB

from ..models.model_insert_player_data import SavePlayerData


class PlayerCreationController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')

    def run(self):
        self.creation_player()
        pass
        # return PlayerMenuController()

    def creation_player(self):
        # renseignement des informations concernant le joueur
        self.player_name = input("Entrez le nom du joueur : ")
        self.player_surname = input("Entrez le prénom du joueur : ")
        self.player_birthday = input("Entrez la date de naissance du joueur : ")
        self.player_gender = input("Entrez le genre du joueur : ")

        # on évite les erreurs de saisie dans le rang du joueur
        wrong_choice = True
        while wrong_choice is True:
            try:
                self.player_rank = abs(int(input("Entrez le rang du joueur : ")))
                wrong_choice = False
                continue
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                continue

        # définition de l'index du joueur a créer
        # on vérifie si la base de donnée n'a pas encore de joueurs
        if len(self.player_pool.all()) == 0:
            self.last_index = 0
        else:
            # on regarde quel est le prochain index disponible dans la BDD des joueurs
            self.last_index = self.player_pool.all()[-1]["Player_Id"] + 1

        SavePlayerData.creation_player(self)
