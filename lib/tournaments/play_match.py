from tinydb import TinyDB, where


class PlayMatch:
    """Jouer le match"""

    def __init__(self, tournament_index, total_match, players_sorted):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')
        self.total_match = total_match
        self.tournament_index = tournament_index
        self.players_sorted = players_sorted

    # on joue les matchs crées auparavant
    def play_match(self):
        self.match.clear()

        # on boucle sur les joueurs avec un pas de 2 pour ne pas rejouer des matchs
        for i in range(0, len(self.player_list), 2):

            wrong_choice = True
            # Boucle évitant les erreurs de saisie
            while wrong_choice is True:
                first_player_index = self.tournament_table.search(where("Tournament_Id") ==
                                                                  self.tournament_index)[0]["players"][i][1]
                second_player_index = self.tournament_table.search(where("Tournament_Id") ==
                                                                   self.tournament_index)[0]["players"][i+1][1]
                first_player_data = self.player_pool.search(where("Player_Id") ==
                                                            first_player_index)[0]["player_name"]
                second_player_data = self.player_pool.search(where("Player_Id") ==
                                                             second_player_index)[0]["player_name"]
                print("Joueur " + str(self.players_sorted[i][0]) + " " +
                      str(first_player_data) + " (" + str(first_player_index) + ")" +
                      " contre Joueur " + str(self.players_sorted[i+1][0]) + " " +
                      str(second_player_data) + " (" + str(second_player_index) + ")")
                match_winner = input("Entrez le numéro du Joueur gagnant (0 = égalité) : ")

                try:
                    # on teste si le 1er joueur des 2 est le gagnant
                    if int(match_winner) == self.players_sorted[i][0]:
                        wrong_choice = False
                        # le 2ème joueur est alors perdant
                        match_loser = self.players_sorted[i+1][0]
                        # on reprend les scores de chaques joueurs et on met à jour
                        score_winner = self.players_sorted[i][1] + 1
                        score_loser = self.players_sorted[i+1][1]
                        print("Gagnant : " + str(match_winner) + " ; Perdant : " + str(match_loser))
                    # on teste si le 2ème joueur des 2 est le gagnant
                    elif int(match_winner) == self.players_sorted[i+1][0]:
                        wrong_choice = False
                        # le 1er joueur est alors perdant
                        match_loser = self.players_sorted[i][0]
                        # on reprend les scores de chaques joueurs et on met à jour
                        score_winner = self.players_sorted[i+1][1] + 1
                        score_loser = self.players_sorted[i][1]
                        print("Gagnant : " + str(match_winner) + " ; Perdant : " + str(match_loser))
                    # on teste s'il y a eu égalité entre les joueurs
                    elif int(match_winner) == 0:
                        wrong_choice = False
                        # on reprend les scores de chaques joueurs et on met à jour
                        score_winner = self.players_sorted[i][1] + 0.5
                        score_loser = self.players_sorted[i+1][1] + 0.5
                        match_winner = self.players_sorted[i][0]
                        match_loser = self.players_sorted[i+1][0]
                        print("Égalité entre le Joueur : " + str(self.players_sorted[i][0]) +
                              " et le Joueur : " + str(self.players_sorted[i+1][0]))
                    else:
                        continue

                except ValueError:
                    continue

            print("")
            # on ajoute les résultats aux variables
            self.match.append(([int(match_winner), score_winner], [int(match_loser), score_loser]))
            self.total_match.append(([int(match_winner), score_winner], [int(match_loser), score_loser]))