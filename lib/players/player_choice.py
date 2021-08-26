from tinydb import TinyDB, where


class PlayerChoice:
    """Joueur choisi dans l'insertion en tournoi"""

    def __init__(self, player_list_to_sort):
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')
        self.player_list_to_sort = player_list_to_sort

    # fonction de séléction des joueurs
    def player_choice(self):
        # listing de l'ensemble des joueurs présents dans la BDD
        for datas in self.player_pool.all():
            print("ID :" + str(datas.get('Player_Id')) + " , Joueur : " + str(datas.get('player_name')))
        if len(self.player_pool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            wrong_choice = True
            # boucle permettant d'éviter un choix éronné
            while wrong_choice is True:
                player_choice = input("Séléctionnez l'ID du joueur :")
                try:
                    # recherche dans la BDD des joueurs l'ID demandé
                    player_id = self.player_pool.search(where("Player_Id") == int(player_choice))[0]

                    # test permettant de savoir si des joueurs ont déjà été inséré
                    if len(self.player_list_to_sort) != 0:
                        wrong_choice = False
                        # boucle sur l'ensemble des joueurs inséré pour vérifier s'il y a un doublon
                        for i in range(len(self.player_list_to_sort)):
                            if self.player_list_to_sort[i][0] == player_id["Player_Id"]:
                                print("Veuillez entrer un nouveau joueur (ID déjà rentré)")
                                wrong_choice = True
                                break
                        # ajout des informations nécessaire à l'insertion d'un joueur dans un tournoi
                        self.player_rank = player_id["player_rank"]
                        self.last_index = player_id["Player_Id"]
                        continue
                    else:
                        # ajout des informations nécessaire à l'insertion d'un joueur dans un tournoi
                        # si aucun joueur n'avait été inséré auparavant
                        self.player_rank = player_id["player_rank"]
                        self.last_index = player_id["Player_Id"]
                        wrong_choice = False
                except (IndexError, ValueError):
                    print("Veuillez entrer une ID correcte")
                continue
