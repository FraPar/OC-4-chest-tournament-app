from ..players import PlayerCreationController
from .save_tournament import SaveStateTournament
from ..players.player_choice import PlayerChoice


class AddPlayerInTournament:
    """Création d'un nouveau tournoi"""

    def __init__(self, player_list_by_rank, load_state, save_step):
        self.player_list_by_rank = player_list_by_rank

        self.save_step = save_step
        self.load_state = load_state

    def adding_players_in_tournament(self):
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
                        PlayerChoice.player_choice(self)
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
            SaveStateTournament.save_players(self)