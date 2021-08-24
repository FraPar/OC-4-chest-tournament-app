import views

from tinydb import TinyDB, where, Query
import random


class ApplicationController:
    """Représente l'application elle-même et permet de la démarrer."""

    def __init__(self):
        """Initialise la classe principale de l'application."""
        self.current_controller = HomeController()

    def start(self):
        """Démarre l'application."""
        while self.current_controller is not None:
            next_controller = self.current_controller.run()
            self.current_controller = next_controller


class HomeController:
    """Contrôleur responsable de gérer le menu d'accueil."""

    def __init__(self):
        self.view = views.HomeView()

    def run(self):
        # Menu d'accueil
        self.view.render()
        next_action = self.view.get_user_choice()

        # Créer un nouveau tournoi
        if next_action == "1":
            return CreateTournament()

        # Créer un nouveau joueur
        elif next_action == "2":
            return PlayerMenuController()

        # Créer un nouveau rapport
        elif next_action == "3":
            return ReportMenuController()

        # Reprendre un tournoi
        elif next_action == "4":
            return LoadTournament()
        # Quitter le programme
        elif next_action == "5":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


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
        # test de l'étape de sauvegarde en cas de reprise de tournoi
        if self.load_state is False:
            # renseignement des informations concernant le tournoi
            tournament_name = input("Entrez le nom du tournoi : ")
            tournament_location = input("Entrez le lieu du tournoi : ")
            tournament_date = input("Entrez la date du tournoi : ")
            tournament_round = int(4)
            tournament_time = input("Entrez le temps du tournoi : ")
            tournament_description = input("Entrez la description du tournoi : ")

            # définition de l'étape de sauvegarde au niveau 1
            self.save_step = 1
            tournament_data = {"Tournament_Id": self.tournament_index, "Name": tournament_name,
                               "Location": tournament_location, "Date": tournament_date,
                               "Round": tournament_round, "Time": tournament_time,
                               "Description": tournament_description, "save_step": self.save_step}
            # sauvegarde des données renseignées dans la BDD
            self.tournament_table.insert(tournament_data)

        # --- ETAPE 1 DE SAUVEGARDE --- #
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
                        self.creation_player()
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

            # --- ETAPE 2 DE SAUVEGARDE --- #
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
            self.save_step = 3
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                         Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 3 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 3) or self.load_state is False:

            print("\n ROUND 2 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.get_player_match()

            # impression des scores des joueurs du tournoi
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 4, après le Round 2
            self.save_step = 4
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                         Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 4 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 4) or self.load_state is False:

            print("\n ROUND 3 : ")

            self.get_player_match()
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 5, après le Round 3
            self.save_step = 5
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                         Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 5 DE SAUVEGARDE --- #
        if (self.load_state is True and self.save_step == 5) or self.load_state is False:

            print("\n ROUND 4 :")

            self.get_player_match()
            self.get_tournament_ranking()

            # Définition de l'étape de sauvegarde à 6, après le Round 4
            self.save_step = 6
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
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

    def creation_player(self):
        # renseignement des informations concernant le joueur
        player_name = input("Entrez le nom du joueur : ")
        player_surname = input("Entrez le prénom du joueur : ")
        player_birthday = input("Entrez la date de naissance du joueur : ")
        player_gender = input("Entrez le genre du joueur : ")
        wrong_choice = True

        # on évite les erreurs de saisie dans le rang du joueur
        while wrong_choice is True:
            try:
                player_rank = abs(int(input("Entrez le rang du joueur : ")))
                wrong_choice = False
                continue
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                continue

        # définition de l'index du joueur a créer
        # on vérifie si la base de donnée n'a pas encore de joueurs
        if len(self.player_pool.all()) == 0:
            last_index = 0
        else:
            # on regarde quel est le prochain index disponible dans la BDD des joueurs
            player_pool = self.player_pool.all()
            sorted_list = sorted(player_pool, key=lambda item: item["Player_Id"])
            last_index = list(sorted_list)[-1]["Player_Id"] + 1

        player_data = {"Player_Id": last_index, "player_name": player_name,
                       "player_surname": player_surname, "player_birthday": player_birthday,
                       "player_gender": player_gender, "player_rank": int(player_rank)}

        # insertion des données du joueur dans la BDD correspondante
        self.player_pool.insert(player_data)

        print("Le joueur a été crée")


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


class CreateTournament:
    """Contrôleur reponsable de la création d'un nouveau tournoi"""

    def __init__(self):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.view = views.HomeView()

    def run(self):
        # mise en place des variables nécessaires au fonctionnement
        # de la fonction de reprise de tournoi
        load_state = False
        save_step = 0
        middle_number_players = 0
        first_half_players = []
        second_half_players = []
        total_match = []
        players_sorted = []
        match = []
        player_list = []

        # teste de présence de données dans la BDD des tournois
        if len(self.tournament_table.all()) == 0:
            last_index = 0
        else:
            # on définie le prochain ID utilisable de la table des tournois
            tournament_table = self.tournament_table.all()
            sorted_list = sorted(tournament_table, key=lambda
                                 item: item["Tournament_Id"])
            last_index = list(sorted_list)[-1]["Tournament_Id"] + 1

        tournament_index = last_index

        # lancement de la class permettant de créer un tournoi
        return TournamentCreationController(
                load_state, save_step, tournament_index,
                middle_number_players, first_half_players, second_half_players,
                total_match, players_sorted, match, player_list)


class LoadTournament:
    """Contrôleur reponsable du chargement d'un tournoi déjà commencé"""

    def __init__(self):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.view = views.HomeView()

    def run(self):
        # on vérifie qu'il y a un tournoi dans la BDD
        if len(self.tournament_table.all()) == 0:
            print("Pas de tournois joués")
        else:
            # activation de la variable permettant le chargement de tournoi
            load_state = True
            # listing de l'ensemble des tournois renseignés dans la BDD
            for datas in self.tournament_table.all():
                print("Tournoi : " + str(datas.get('Tournament_Id')) + " | Nom : " + str(datas.get('Name')))
            # demande à l'utilisateur du choix de l'ID de son tournoi
            tournament_choice = input("Séléctionnez le tournoi (ID):")

            tournament_index = int(tournament_choice)
            # recherche du tournoi choisi par l'utilisateur
            this_tournament = self.tournament_table.search(where
                                                           ("Tournament_Id") == tournament_index)[0]
            # mise en mémoire de l'étape de la sauvegarde du tournoi
            save_step = this_tournament["save_step"]
            # mise en place des variables nécessaires au fonctionnement
            # de la fonction de reprise de tournoi
            middle_number_players = 0
            first_half_players = []
            second_half_players = []
            total_match = []
            players_sorted = []
            match = []
            player_list = []
            # si les joueurs ont déjà été choisi, il faut renseigner certaines variables
            if save_step >= 2:
                player_list = [1, 2, 3, 4, 5, 6, 7, 8]
                middle_number_players = int(len(self.tournament_table.search
                                                (where("Tournament_Id") == tournament_index)[0]["players"])/2)
                first_half_players = player_list[:middle_number_players]
                second_half_players = player_list[middle_number_players:]
            # si un match a déjà été joué, il faut renseigner des variables supplémentaires
            if save_step >= 3:
                total_match = this_tournament["matchs"]
                # on charge le dernier round joué
                match = this_tournament["matchs"][-4:]
                players_to_sort = []
                for datas in match:
                    players_to_sort.append(datas[0])
                    players_to_sort.append(datas[1])
                # Tri des joueurs par rang
                players_to_sort.sort()
                # Tri des joueurs par rang et par score
                players_to_sort.sort(key=self.get_score, reverse=True)
                players_sorted = players_to_sort

            return TournamentCreationController(
                load_state, save_step, tournament_index,
                middle_number_players, first_half_players,
                second_half_players, total_match, players_sorted,
                match, player_list)

    # permet le tri par rang et par score
    def get_score(self, elem):
        return elem[1]


class PlayerMenuController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self):
        self.view = views.PlayerMenuView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        # Création d'un joueur
        if next_action == "1":
            return PlayerCreationController()
        # Retour au menu
        elif next_action == "2":
            return PlayerRankController()
        # Retour au menu
        elif next_action == "3":
            return HomeController()
        # Quitter le programme
        elif next_action == "4":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerMenuController()


class PlayerCreationController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')

    def run(self):
        self.creation_player()
        return PlayerMenuController()

    def creation_player(self):
        # renseignement des informations concernant le joueur
        player_name = input("Entrez le nom du joueur : ")
        player_surname = input("Entrez le prénom du joueur : ")
        player_birthday = input("Entrez la date de naissance du joueur : ")
        player_gender = input("Entrez le genre du joueur : ")
        wrong_choice = True

        # on évite les erreurs de saisie dans le rang du joueur
        while wrong_choice is True:
            try:
                player_rank = abs(int(input("Entrez le rang du joueur : ")))
                wrong_choice = False
                continue
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                continue

        # définition de l'index du joueur a créer
        # on vérifie si la base de donnée n'a pas encore de joueurs
        if len(self.player_pool.all()) == 0:
            last_index = 0
        else:
            # on regarde quel est le prochain index disponible dans la BDD des joueurs
            player_pool = self.player_pool.all()
            sorted_list = sorted(player_pool, key=lambda item: item["Player_Id"])
            last_index = list(sorted_list)[-1]["Player_Id"] + 1

        player_data = {"Player_Id": last_index, "player_name": player_name,
                       "player_surname": player_surname, "player_birthday": player_birthday,
                       "player_gender": player_gender, "player_rank": int(player_rank)}

        # insertion des données du joueur dans la BDD correspondante
        self.player_pool.insert(player_data)

        print("Le joueur a été crée")


class PlayerRankController:
    """Contrôleur responsable de gérer le menu de
    modification du rang d'un joueur.
    """

    def __init__(self):
        self.view = views.TournamentReportMenuView()
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')

    def run(self):
        if len(self.player_pool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            self.rank_player()
        return PlayerMenuController()

    def rank_player(self):
        # visualisation des joueurs présent dans la BDD
        player_pool = self.player_pool.all()
        for datas in player_pool:
            self.view.get_player_data(datas)

        wrong_choice = True
        while wrong_choice is True:
            try:
                player_choice = int(input("Séléctionnez le joueur (ID):"))
                # on va chercher l'ID du joueur dans la BDD des joueurs
                user_choice = self.player_pool.search(where("Player_Id") == player_choice)
                wrong_choice = False
                player_rank = str(user_choice[0]["player_rank"])
            except (IndexError, ValueError):
                print("Veuillez entrer un ID correcte")
                wrong_choice = True
                continue

        wrong_choice = True
        while wrong_choice is True:
            try:
                print("Rang actuel du joueur : " + player_rank)
                newRank = abs(int(input("Quel est le nouveau rang du joueur?")))
                wrong_choice = False
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                wrong_choice = True
                continue

        player_data = {"player_rank": newRank}
        # Mise à jour du joueur correspondant dans la BDD des joueurs
        self.player_pool.update(player_data,
                                Query().Player_Id == player_choice)


class ReportMenuController:
    """Contrôleur responsable de gérer le menu de rapports.
    """

    def __init__(self):
        self.view = views.ReportMenuView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        # créer un rapport sur l'ensemble des joueurs
        if next_action == "1":
            return ReportAllPlayerController()
        # créer un rapport sur l'ensemble des tournois
        elif next_action == "2":
            return ReportTournamentController()
        # retour à l'accueil
        elif next_action == "3":
            return HomeController()
        # quitter le programme
        elif next_action == "4":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return ReportMenuController()


class ReportAllPlayerController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec l'ensemble des acteurs.
    """

    def __init__(self):
        self.view = views.PlayerReportMenuView()
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')
        self.player_pool_ddb = self.player_pool.all()

    def run(self):
        self.view.render()
        self.next_action = self.view.get_user_choice()
        if len(self.player_pool_ddb) == 0:
            print("Pas de joueurs crées")
        else:
            self.creation_report()
        return ReportMenuController()

    def creation_report(self):
            user_choice = self.next_action
            # Trier l'ensemble par ordre Alphabétique
            if user_choice == "1":
                self.player_sort_by_name()
            # Trier l'ensemble par Rang
            elif user_choice == "2":
                self.player_sort_by_rank()
            # retour à l'accueil
            elif user_choice == "3":
                return EndController()
            else:
                self.view.notify_invalid_choice()
                return ReportAllPlayerController()

    # Fonction de tri des joueurs par Noms
    def player_sort_by_name(self):
        sorted_list = sorted(self.player_pool_ddb, key=lambda item: item["player_name"])
        for datas in sorted_list:
            self.view.get_player_data(datas)

    # Fonction de tri des joueurs par Rang
    def player_sort_by_rank(self):
        sorted_list = sorted(self.player_pool_ddb, key=lambda item: item["player_rank"])
        for datas in sorted_list:
            self.view.get_player_data(datas)


class ReportTournamentController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec tous les tournois.
    """

    def __init__(self):
        self.view = views.TournamentReportMenuView()
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')
        self.player_in_tournament = []

    def run(self):
        self.view.menu_render()
        self.next_action = self.view.get_user_choice()
        # on vérifie qu'il y a un tournoi dans la BDD
        if len(self.tournament_table.all()) == 0:
            print("Pas de tournois joués")
        else:
            self.creation_report()
        return ReportMenuController()

    def creation_report(self):
        # Listing de tous les tournois dans la BDD des tournois
        for datas in self.tournament_table.all():
            self.view.get_tournament_data(datas)
        user_choice = self.next_action

        # Voir les tours d'un tournoi spécifique
        try:
            tournament_choice = int(input("Séléctionnez le tournoi (ID):"))
            # on va chercher l'ID du tournoi dansl a BDD des tournois
            tournament_user_choice = self.tournament_table.search(where("Tournament_Id") == tournament_choice)[0]
        except (IndexError, ValueError, UnboundLocalError):
            print("Veuillez entrer un ID correcte")

        # Voir les tours d'un tournoi spécifique
        if user_choice == "1":
            self.view.get_tournament_data(tournament_user_choice)
            self.view.get_tournament_rounds(tournament_user_choice)

        # Voir les matchs d'un tournoi spécifique
        elif user_choice == "2":
            self.view.get_tournament_data(tournament_user_choice)
            self.view.get_tournament_players(tournament_user_choice)
            self.view.get_tournament_matchs(tournament_user_choice)

        # Voir les joueurs d'un tournoi spécifique
        elif user_choice == "3":
            self.tournament_player(tournament_user_choice)

        # Retour au menu d'accueil
        elif user_choice == "4":
            return EndController()

        else:
            self.view.notify_invalid_choice()
            return ReportTournamentController()

    def tournament_player(self, tournament_user_choice):
        if tournament_user_choice["save_step"] >= 2:
            for datas in tournament_user_choice["players"]:
                self.player_in_tournament.append(self.player_pool.search(where("Player_Id") == datas[1])[0])
            self.view.sort_menu_render()

            wrong_choice = True
            while wrong_choice is True:
                user_choice = self.view.get_user_id_choice()
                # Trier l'ensemble des joueurs du tournoi par ordre Alphabétiqu
                if user_choice == "1":
                    wrong_choice = False
                    sorted_list = sorted(self.player_in_tournament, key=lambda item: item["player_name"])
                    for datas in sorted_list:
                        self.view.get_player_data(datas)
                # Trier l'ensemble des joueurs du tournoi par rang
                elif user_choice == "2":
                    wrong_choice = False
                    sorted_list = sorted(self.player_in_tournament, key=lambda item: item["player_rank"])
                    for datas in sorted_list:
                        self.view.get_player_data(datas)
                else:
                    wrong_choice = True
                    print("Veuillez saisir une entrée valide")
                continue
        else:
            print("Aucun joueur n'a été inséré dans un match")


class EndController:
    """Contrôleur responsable de gérer la fin du programme."""

    def __init__(self):
        self.view = views.EndView()

    def run(self):
        self.view.render()
        choice = self.view.get_user_choice()
        if choice == "oui":
            return
        elif choice == "non":
            return HomeController()
        else:
            self.view.notify_invalid_choice()
            return EndController()
