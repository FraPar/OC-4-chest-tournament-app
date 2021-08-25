import random
from tinydb import TinyDB, where

from .. import views

from .save_tournament import SaveStateTournament
from .first_round import FirstRound
from .adding_players_in_tournament import AddPlayerInTournament
from .play_match import PlayMatch


class TournamentCreationController:
    """Création d'un nouveau tournoi"""

    def __init__(self, load_state, save_step,
                 tournament_index, middle_number_players,
                 first_half_players, second_half_players,
                 total_match, players_sorted, match, player_list):

        self.view = views.TournamentMenuView()
        self.db = TinyDB('db.json')

        # variable de chargement de tournoi
        self.load_state = load_state
        self.save_step = save_step

        # --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')

        # --- CREATION DE LA LISTE DES JOUEURS --- #
        self.player_list = player_list
        self.player_list_to_sort = []
        self.player_list_by_rank = []

        # --- DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE --- #
        self.middle_number_players = middle_number_players
        self.first_half_players = first_half_players
        self.second_half_players = second_half_players

        # --- Définition des variables générales--- #
        self.tournament_index = tournament_index
        self.number_of_players = 0
        self.last_index = 0
        self.player_rank = 0
        self.player_match = []
        self.total_match = total_match
        self.players_to_sort = []
        self.players_sorted = players_sorted
        self.match = match
        self.match_to_play = []
        self.player_order = []

    def run(self):

        # --- ETAPE 0 DE SAUVEGARDE --- #
        SaveStateTournament.starting_tournament(self)

        # --- ETAPE 1 DE SAUVEGARDE --- #
        AddPlayerInTournament.adding_players_in_tournament(self)

        # --- ETAPE 2 DE SAUVEGARDE --- #
        FirstRound.playing_first_round(self)

        # impression des scores des joueurs du tournoi
        self.get_tournament_ranking()

        # Définition de l'étape de sauvegarde à 3, après le Round 1
        SaveStateTournament.save_round_one(self)

        # --- ETAPE 3 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 3) or self.load_state is False:

            print("\n ROUND 2 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.get_player_match()

            # impression des scores des joueurs du tournoi
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 4, après le Round 2
            SaveStateTournament.save_round_two(self)

            # --- ETAPE 4 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 4) or self.load_state is False:

            print("\n ROUND 3 : ")

            self.get_player_match()
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 5, après le Round 3
            SaveStateTournament.save_round_three(self)


            # --- ETAPE 5 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 5) or self.load_state is False:

            print("\n ROUND 4 :")

            self.get_player_match()
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 6, après le Round 4
            SaveStateTournament.save_round_four(self)

    # fonction globale permettant d'assurer les rounds 2 à 4
    def get_player_match(self):
        self.player_match.clear()
        self.player_order.clear()
        # on prépare les données de joueurs pour mettre en
        # place les paires du round
        # on insert l'ensemble des matchs dans une liste
        # pour ne pas avoir de matchs doublons
        for matchs in self.total_match:
            self.player_match.append(matchs)
        # on insert les joueurs par rapport à leur score
        # et leur rang dans une variable
        for player in self.players_sorted:
            self.player_order.append(player[0])
        # fonction permettant de connaître quels match ont été joué par nos joueurs
        self.match_played()
        # fonction permettant de trouver un match dans le cas d'un doublon de match
        self.match_to_add()
        # fonction permettant d'associer les joueurs entre eux avant de jouer le match
        self.sort_player_by_match()
        # fonction permettant de jouer le match
        PlayMatch.play_match(self)
        # fonction permettant de trier les joueurs selon leur rang / nouveau score
        self.sort_players_by_score()

    # fonction permettant de connaître les matchs joués par notre joueur
    def match_played(self):
        self.match_to_play.clear()
        # on boucle sur les joueurs du tournoi, du 1er au dernier
        for players in self.player_order:
            played_matchs = []
            # on boucle sur les matchs déjà joué lors du tournoi
            for plays in self.total_match:
                player1 = plays[0][0]
                player2 = plays[1][0]
                # on teste si le joueur 1 est le joueur sur lequel
                # on boucle pour connaître son adversaire
                if player1 == players:
                    played_matchs.append(player2)
                # on teste si le joueur 2 est le joueur sur lequel
                # on boucle pour connaître son adversaire
                elif player2 == players:
                    played_matchs.append(player1)
            # on appelle la fonction permettant de mettre
            # un adversaire face à un autre
            self.sort_match(played_matchs, players)
        pass

    # fonction permettant de mettre un joueur face à un
    # autre sans doublon de match
    def sort_match(self, played_matchs, players):
        for i in range(len(self.player_order)):
            # on teste si le joueur n'a pas déjà été aloué
            # a un autre match dans ce round, s'il n'a pas
            # déjà été joué ou si on ne met pas un joueur
            # face à lui même
            if players != self.player_order[i] and \
                         (self.player_order[i] in played_matchs) is False and \
                         ((players in self.match_to_play) is False and
                          (self.player_order[i] in self.match_to_play) is False):
                self.match_to_play.append(players)
                self.match_to_play.append(self.player_order[i])
                break

    # fonction permettant de gérer le cas particulier des 2
    # derniers joueurs ayant déjà joué ensemble
    def match_to_add(self):
        # on met i à 3 pour garder les 4 derniers joueurs dans
        # notre piscine de joueurs à mettre en face
        i = 3
        # on teste si tous les matchs ont été alloué ou non.
        while len(self.match_to_play) < len(self.player_list) \
                and i <= len(self.player_list):
            i += 1
            # on récupère les 4+ derniers joueurs pour trouver un match à jouer
            new_player_order = self.player_order[-i:]
            # on mélange les joueurs pour trouver un match à jouer
            random.shuffle(new_player_order)
            self.player_order = self.player_order[:4]
            # on ajoute les joueurs ayant été mis face à face pour
            # tester s'ils ont déjà joués ensemble
            for players in new_player_order:
                self.player_order.append(players)
            # on appelle la fonction permettant de connaître quels
            # match ont été joué par nos joueurs
            self.match_played()
            # si le nombre de joueurs présents dans le tournoi n'est
            # pas équivalent à celui de joueurs a qui on a trouvé un
            # match, on continue la boucle
            if len(self.match_to_play) < len(self.player_list):
                continue

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



    # permet le tri par rang et par score
    def get_score(self, elem):
        return elem[1]

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


