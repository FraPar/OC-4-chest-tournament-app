from tinydb import where


class FirstRound():
    """Jouer le round 1"""

    def __init__(self, load_state, save_step, middle_number_players,
                 first_half_players, second_half_players, total_match):
        # variable de chargement de tournoi
        self.load_state = load_state
        self.save_step = save_step

        # --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')

        # --- DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE --- #
        self.middle_number_players = middle_number_players
        self.first_half_players = first_half_players
        self.second_half_players = second_half_players

        # --- Définition des variables générales--- #
        self.players_to_sort = []
        self.total_match = total_match

    def playing_first_round(self):
        if (self.load_state is True and self.save_step == 2) or self.load_state is False:

            print("\nROUND 1 :")

            # Boucle permettant de matcher les joueurs de la moitié supèrieure
            # avec les joueurs de la moitié infèrieure respéctive
            for i in range(self.middle_number_players):
                wrong_choice = True
                # Boucle permettant d'assurer un choix valide
                while wrong_choice is True:
                    first_player_index = self.tournament_table.search(where("Tournament_Id") ==
                                                                      self.tournament_index)[0]["players"][i][1]
                    second_player_index = self.tournament_table.search(where("Tournament_Id") ==
                                                                       self.tournament_index)[0]["players"][i+4][1]
                    first_player_data = self.player_pool.search(where("Player_Id") ==
                                                                first_player_index)[0]["player_name"]
                    second_player_data = self.player_pool.search(where("Player_Id") ==
                                                                 second_player_index)[0]["player_name"]
                    print("Joueur " + str(i+1) + " " + str(first_player_data) + " (" + str(first_player_index) + ")" +
                          " contre Joueur " + str(i+5) + " " +
                          str(second_player_data) + " (" + str(second_player_index) + ")")
                    match_winner = input("Entrez le numéro du gagnant (0 = égalité) : ")
                    # définition des points alloués aux gagnants et aux perdants
                    score_winner = 1
                    score_loser = 0
                    # ensemble Try Except permettant d'éviter les erreures de saisies
                    try:
                        # teste si le joueur ayant gagné est celui de la moitié supèrieure
                        if int(match_winner) == self.first_half_players[i]:
                            wrong_choice = False
                            match_loser = self.second_half_players[i]
                            print("Gagnant : " + str(match_winner) + " ; Perdant : " + str(match_loser) + "\n")
                        # teste si le joueur ayant gagné est celui de la moitié infèrieure
                        elif int(match_winner) == self.second_half_players[i]:
                            wrong_choice = False
                            match_loser = self.first_half_players[i]
                            print("Gagnant : " + str(match_winner) + " ; Perdant : " + str(match_loser) + "\n")
                        # teste si les joueurs ont fait une égalité
                        elif int(match_winner) == 0:
                            wrong_choice = False
                            score_winner = 0.5
                            score_loser = 0.5
                            match_winner = self.first_half_players[i]
                            match_loser = self.second_half_players[i]
                            print("Égalité entre le Joueur : " + str(self.first_half_players[i]) +
                                  " et le Joueur : " + str(self.second_half_players[i]) + "\n")
                        else:
                            continue

                    except ValueError:
                        continue

                # On ajoute le gagnant et le perdant de la partie avec leurs scores réspectifs
                self.total_match.append(([int(match_winner), score_winner], [int(match_loser), score_loser]))

            # Ajout des joueurs avec leurs points préparant le tri
            for i in range(self.middle_number_players):
                self.players_to_sort.append(self.total_match[i][0])
                self.players_to_sort.append(self.total_match[i][1])

            # Tri des joueurs par rang
            self.players_to_sort.sort()

            # Tri des joueurs par rang et par score
            self.players_to_sort.sort(key=self.get_score, reverse=True)
            self.players_sorted = self.players_to_sort

    # permet le tri par rang et par score
    def get_score(self, elem):
        return elem[1]
