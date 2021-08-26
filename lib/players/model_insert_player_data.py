from tinydb import TinyDB


class SavePlayerData:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self, last_index, player_name, player_surname, player_birthday, player_gender, player_rank):
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')
        self.player_name = player_name
        self.player_surname = player_surname
        self.player_birthday = player_birthday
        self.player_gender = player_gender
        self.last_index = last_index
        self.player_rank = player_rank


    def run(self):
        self.creation_player()
        pass
        # return PlayerMenuController()

    def creation_player(self):
        # renseignement des informations concernant le joueur
        player_data = {"Player_Id": self.last_index, "player_name": self.player_name,
                       "player_surname": self.player_surname, "player_birthday": self.player_birthday,
                       "player_gender": self.player_gender, "player_rank": int(self.player_rank)}

        # insertion des données du joueur dans la BDD correspondante
        self.player_pool.insert(player_data)

        print("Le joueur a été crée")
