from tinydb import TinyDB, where, Query
import views

from players import PlayerCreationController


class AddingPlayers:
    def __init__(self, load_state, save_step, player_list_to_sort, player_list, player_list_by_rank, tournament_index):
        self.view = views.TournamentMenuView()
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')
        self.tournament_table = self.db.table('tournament_table')

        self.load_state = load_state
        self.save_step = save_step
        self.player_list_to_sort = player_list_to_sort
        self.player_list = player_list
        self.player_list_by_rank = player_list_by_rank
        self.tournament_index = tournament_index

    def run(self):
        if (self.load_state is True and self.save_step == 1) or self.load_state is False:

            # --- INSERTION DES DONNEES JOUEURS --- #
            # Index permettant de créer un joueur automatiquement
            player_index = 0
            # Boucle permettant d'ajouter 8 joueurs ont bien été renseigné dans le tournoi
            while len(self.player_list_to_sort) < 8:
                player_index += 1
                # Menu de choix de la manière d'insérer un joueur das le tournoi
                self.view.render()
                wrong_choice = True
                # permet de boucler tant qu'un choix invalide est détécté
                while wrong_choice is True:
                    user_choice = input("Que voulez-vous faire? ")
                    # Ajouter un joueur déjà éxistant
                    if user_choice == "1":
                        wrong_choice = False
                        self.player_choice()
                    # Créer un nouveau joueur
                    elif user_choice == "2":
                        wrong_choice = False
                        PlayerCreationController().creation_player()
                        self.last_index = self.player_pool.all()[-1]["Player_Id"]
                        self.player_rank = self.player_pool.all()[-1]["player_rank"]
                    else:
                        wrong_choice = True
                        print("Veuillez saisir une entrée valide")

                # Ajout des joueurs et de leur rang avant tri
                self.player_list_to_sort.append([(self.last_index), self.player_rank])
                self.player_list.append(player_index)
                continue

            # Tri des joueurs par Rang
            player_list_sorted = sorted(self.player_list_to_sort, key=lambda
                                        item: item[1], reverse=True)

            # Ajout d'un index aux joueurs pour connaître leur classement
            index = 0
            # Boucle sur l'ensemble des données triés pour pouvoir les insérer en BDD après
            for datas in player_list_sorted:
                index += 1
                self.player_list_by_rank.append((index, datas[0], datas[1]))

            # Définition des 4 premiers joueurs et des 4 derniers joueurs
            self.number_of_players = len(self.player_list)
            self.middle_number_players = int(self.number_of_players/2)
            self.first_half_players = self.player_list[:self.middle_number_players]
            self.second_half_players = self.player_list[self.middle_number_players:]

            # Définition de l'étape de sauvegarde à 2, après le classement des joueurs
            self.save_step = 2
            tournament_data = {"players": self.player_list_by_rank,
                               "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                         Query().Tournament_Id == self.tournament_index)

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
