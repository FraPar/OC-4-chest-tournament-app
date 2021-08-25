import random
from tinydb import TinyDB, where

from .. import views

from ..players import PlayerCreationController


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
        self.adding_players_in_tournament()

        # --- ETAPE 2 DE SAUVEGARDE --- #
        self.playing_first_round()

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

            # impression des scores des joueurs du tournoi
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 3, après le Round 1
            SaveStateTournament.save_round_one(self)

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
        self.play_match()
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
            SaveStateTournament.save_players(self)
