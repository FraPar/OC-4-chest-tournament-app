from tinydb import TinyDB, where

class SortTournamentData:
    """Tri les données du tournoi pour un
    classement en ordre."""

    def __init__(self, tournament_index, middle_number_players,
                 total_match, players_sorted, match_to_play):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')

        self.match_to_play = match_to_play
        self.players_sorted = players_sorted
        self.total_match = total_match
        self.middle_number_players = middle_number_players
        self.tournament_index = tournament_index

    # on associe les différents joueurs entre eux
    # après le filtrage évitant les doublons
    def sort_player_by_match(self):
        # on boucle sur l'ensemble des joueurs à coupler dans un match
        for players in self.match_to_play:
            # on boucle sur l'ensemble des joueurs présent dans le tri effectué
            for i in range(len(self.player_list)):
                # on récupère les joueurs et leurs scores dans l'ordre
                if players == self.players_sorted[i][0]:
                    self.players_sorted.append(self.players_sorted[i])
                    # on supprime les joueurs déjà trouvés
                    del self.players_sorted[i]

    # permet d'afficher le classement
    def get_tournament_ranking(self):
        for datas in self.players_sorted:
            IdFounded = False
            while IdFounded is False:
                for i in range(len(self.players_sorted)):
                    PlayerIndex = self.tournament_table.search(where("Tournament_Id") ==
                                                               self.tournament_index)[0]["players"][i][0]
                    if datas[0] == PlayerIndex:
                        PlayerIndex = self.tournament_table.search(where("Tournament_Id") ==
                                                                   self.tournament_index)[0]["players"][i][1]
                        IdFounded = True
                        break
                    else:
                        continue

            player_data = self.player_pool.search(where("Player_Id") ==
                                                  PlayerIndex)[0]
            print("Joueur " + str(i+1) + " " + str(player_data["player_name"]) +
                  " (" + str(player_data["Player_Id"]) + ") | Points : " + str(datas[1]))

    # on trie les joueurs par rapport à leur score et leur rang
    def sort_players_by_score(self):
        self.players_to_sort.clear()
        self.match = self.total_match[-4:]

        # on ajoute les tuples à la variable pour pouvoir trier l'ensemble
        for i in range(self.middle_number_players):
            self.players_to_sort.append(self.match[i][0])
            self.players_to_sort.append(self.match[i][1])

        # Tri des joueurs par rang
        self.players_to_sort.sort()

        # Tri des joueurs par rang et par score
        self.players_to_sort.sort(key=self.get_score, reverse=True)
        self.players_sorted = self.players_to_sort

    # permet le tri par rang et par score
    def get_score(self, elem):
        return elem[1]