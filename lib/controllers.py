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
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.view = views.HomeView()

    def run(self):
        # Menu d'accueil
        self.view.render()
        next_action = self.view.get_user_choice()

        # Créer un nouveau tournoi
        if next_action == "1":
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
            return ManualRoundCreationController(
                    load_state, save_step, tournament_index,
                    middle_number_players, first_half_players, second_half_players,
                    total_match, players_sorted, match, player_list)

        # Créer un nouveau joueur
        elif next_action == "2":
            return PlayerMenuController()

        # Créer un nouveau rapport
        elif next_action == "3":
            return ReportMenuController()

        # Reprendre un tournoi
        elif next_action == "4":
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
                    players_to_sort.sort(key=self.getScore, reverse=True)
                    players_sorted = players_to_sort

                return ManualRoundCreationController(
                    load_state, save_step, tournament_index,
                    middle_number_players, first_half_players,
                    second_half_players, total_match, players_sorted,
                    match, player_list)
        # Quitter le programme
        elif next_action == "5":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()

    # permet le tri par rang et par score
    def getScore(self, elem):
        return elem[1]


class ManualRoundCreationController:
    """Création d'un nouveau tournoi"""

    def __init__(self, load_state, save_step,
                 tournament_index, middle_number_players,
                 first_half_players, second_half_players,
                 total_match, players_sorted, match, player_list):
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
        # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.load_state is True and self.save_step == 1) or self.load_state is False:

            # --- INSERTION DES DONNEES JOUEURS --- #
            # Index permettant de créer un joueur automatiquement
            i = 0
            # Boucle permettant d'ajouter 8 joueurs ont bien été renseigné dans le tournoi
            while len(self.player_list_to_sort) < 8:
                i += 1
                # Menu de choix de la manière d'insérer un joueur das le tournoi
                print("Voulez-vous :")
                print("==============================")
                print("1. Ajouter un joueur déjà éxistant")
                print("2. Créer un nouveau joueur (Manuel)")
                print("3. Créer un nouveau joueur (Automatique)")

                wrong_choice = True
                # permet de boucler tant qu'un choix invalide est détécté
                while wrong_choice is True:
                    user_choice = input("Que voulez-vous faire? ")
                    # Ajouter un joueur déjà éxistant
                    if user_choice == "1":
                        wrong_choice = False
                        self.player_choice()
                    # Créer un nouveau joueur (Manuel)
                    elif user_choice == "2":
                        wrong_choice = False
                        self.creationPlayer()
                    # Créer un nouveau joueur (Automatique)
                    elif user_choice == "3":
                        wrong_choice = False
                        player_name = "Name" + str(i)
                        player_surname = "Surname" + str(i)
                        player_birthday = "BDate" + str(i)
                        player_gender = "Gender" + str(i)

                        # Test de la présence de donnée dans la BDD
                        if len(self.player_pool.all()) == 0:
                            self.last_index = 0
                        else:
                            # Définition du prochain ID valide dans la BDD
                            player_pool = self.player_pool.all()
                            sorted_list = sorted(player_pool, key=lambda
                                                 item: item["Player_Id"])
                            print("Joueur automatique crée \n")
                            self.last_index = list(sorted_list)[-1]["Player_Id"] + 1

                        # choix aléatoire d'une côte
                        self.player_rank = random.randint(0, 1500)
                        player_data = {"Player_Id": self.last_index, "player_name": player_name,
                                      "player_surname": player_surname, "player_birthday": player_birthday,
                                      "player_gender": player_gender, "player_rank": self.player_rank}
                        # Insertion des données dans la BDD de joueurs
                        self.player_pool.insert(player_data)
                    else:
                        wrong_choice = True
                        print("Veuillez saisir un entrée valide")

                # Ajout des joueurs et de leur rang avant tri
                self.player_list_to_sort.append([(self.last_index), self.player_rank])
                self.player_list.append(i)
                continue

            # Tri des joueurs par Rang
            player_list_sorted = sorted(self.player_list_to_sort, key=lambda
                                      item: item[1], reverse=True)

            # Ajout d'un index aux joueurs pour connaître leur classement
            i = 0
            # Boucle sur l'ensemble des données triés pour pouvoir les insérer en BDD après
            for datas in player_list_sorted:
                i += 1
                self.player_list_by_rank.append((i, datas[0], datas[1]))

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
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.load_state is True and self.save_step == 2) or self.load_state is False:

            # --- ROUND 1 --- #
            print()
            print("ROUND 1 :")

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
            self.players_to_sort.sort(key=self.getScore, reverse=True)
            self.players_sorted = self.players_to_sort

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 3, après le Round 1
            self.save_step = 3
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 3 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.load_state is True and self.save_step == 3) or self.load_state is False:

            # --- ROUND 2 --- #
            print()
            print("ROUND 2 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.getplayer_matchs()

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 4, après le Round 2
            self.save_step = 4
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 4 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.load_state is True and self.save_step == 4) or self.load_state is False:

            # --- ROUND 3 --- #
            print()
            print("ROUND 3 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.getplayer_matchs()

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 5, après le Round 3
            self.save_step = 5
            tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournament_table.update(tournament_data,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 5 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.load_state is True and self.save_step == 5) or self.load_state is False:

            # --- ROUND 4 --- #
            print()
            print("ROUND 4 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.getplayer_matchs()

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

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

    # création des joueurs
    def creationPlayer(self):
        # renseignement des informations nécéssaires à l'insertion d'un nouveau joueur
        player_name = input("Entrez le nom du joueur : ")
        player_surname = input("Entrez le prénom du joueur : ")
        player_birthday = input("Entrez la date de naissance du joueur : ")
        player_gender = input("Entrez le genre du joueur : ")
        wrong_choice = True

        # on évite les erreurs de saisie dans le rang du joueur
        while wrong_choice is True:
            try:
                self.player_rank = abs(int(input("Entrez le rang du joueur : ")))
                wrong_choice = False
                continue
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                continue

        # Teste s'il y a des joueurs dans la BDD correspondante
        if len(self.player_pool.all()) == 0:
            self.last_index = 0
        # Définie le prochain ID disponible pour l'ajout de joueurs
        else:
            player_pool = self.player_pool.all()
            sorted_list = sorted(player_pool, key=lambda item: item["Player_Id"])
            self.last_index = list(sorted_list)[-1]["Player_Id"] + 1

        player_data = {"Player_Id": self.last_index, "player_name": player_name,
                      "player_surname": player_surname, "player_birthday": player_birthday,
                      "player_gender": player_gender, "player_rank": self.player_rank}

        # insert dans la BDD des joueurs le nouveau joueur
        self.player_pool.insert(player_data)

    # fonction globale permettant d'assurer les rounds 2 à 4
    def getplayer_matchs(self):
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
        self.matchPlayed()
        # fonction permettant de trouver un match dans le cas d'un doublon de match
        self.matchToAdd()
        # fonction permettant d'associer les joueurs entre eux avant de jouer le match
        self.sortPlayersByMatch()
        # fonction permettant de jouer le match
        self.playMatch()
        # fonction permettant de trier les joueurs selon leur rang / nouveau score
        self.sortPlayersByScore()

    # fonction permettant de connaître les matchs joués par notre joueur
    def matchPlayed(self):
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
            self.sortMatch(played_matchs, players)
        pass

    # fonction permettant de mettre un joueur face à un
    # autre sans doublon de match
    def sortMatch(self, played_matchs, players):
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
    def matchToAdd(self):
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
            self.matchPlayed()
            # si le nombre de joueurs présents dans le tournoi n'est
            # pas équivalent à celui de joueurs a qui on a trouvé un
            # match, on continue la boucle
            if len(self.match_to_play) < len(self.player_list):
                continue

    # on associe les différents joueurs entre eux
    # après le filtrage évitant les doublons
    def sortPlayersByMatch(self):
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
    def playMatch(self):
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
    def getScore(self, elem):
        return elem[1]

    # permet d'afficher le classement
    def getTournamentRanking(self):
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
    def sortPlayersByScore(self):
        self.players_to_sort.clear()
        self.match = self.total_match[-4:]

        # on ajoute les tuples à la variable pour pouvoir trier l'ensemble
        for i in range(self.middle_number_players):
            self.players_to_sort.append(self.match[i][0])
            self.players_to_sort.append(self.match[i][1])

        # Tri des joueurs par rang
        self.players_to_sort.sort()

        # Tri des joueurs par rang et par score
        self.players_to_sort.sort(key=self.getScore, reverse=True)
        self.players_sorted = self.players_to_sort


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
            return player_rankController()
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
        self.creationPlayer()
        return PlayerMenuController()

    def creationPlayer(self):
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


class player_rankController:
    """Contrôleur responsable de gérer le menu de
    modification du rang d'un joueur.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')

    def run(self):
        if len(self.player_pool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            self.rankPlayer()
        return PlayerMenuController()

    def rankPlayer(self):
        # visualisation des joueurs présent dans la BDD
        player_pool = self.player_pool.all()
        for datas in player_pool:
            print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["player_name"])
                  + ", Prénom : " + str(datas["player_surname"]) + ", Date de naissance : "
                  + str(datas["player_birthday"]) + ", Genre : " + str(datas["player_gender"])
                  + ", Classement : " + str(datas["player_rank"]))

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
    pass


class ReportAllPlayerController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec l'ensemble des acteurs.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.player_pool = self.db.table('player_pool')

    def run(self):
        if len(self.player_pool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            self.creationReport()
        return ReportMenuController()

    def creationReport(self):
        print("Voulez-vous :")
        print("==============================")
        print("1. Trier l'ensemble par ordre Alphabétique")
        print("2. Trier l'ensemble par Rang")
        print("3. Retourner au menu")

        wrong_choice = True
        while wrong_choice is True:
            user_choice = input("Que voulez-vous faire? ")
            # Trier l'ensemble par ordre Alphabétique
            if user_choice == "1":
                wrong_choice = False
                self.player_SortName()
            # Trier l'ensemble par Rang
            elif user_choice == "2":
                wrong_choice = False
                self.player_SortRank()
            # retour à l'accueil
            elif user_choice == "3":
                wrong_choice = False
                return EndController()
            else:
                wrong_choice = True
                print("Veuillez saisir un entrée valide")
            continue

    # Fonction de tri des joueurs par Noms
    def player_SortName(self):
        player_pool = self.player_pool.all()
        sorted_list = sorted(player_pool, key=lambda item: item["player_name"])
        for datas in sorted_list:
            print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["player_name"])
                  + ", Prénom : " + str(datas["player_surname"]) + ", Date de naissance : "
                  + str(datas["player_birthday"]) + ", Genre : " + str(datas["player_gender"])
                  + ", Classement : " + str(datas["player_rank"]))

    # Fonction de tri des joueurs par Rang
    def player_SortRank(self):
        player_pool = self.player_pool.all()
        sorted_list = sorted(player_pool, key=lambda item: item["player_rank"])
        for datas in sorted_list:
            print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["player_name"])
                  + ", Prénom : " + str(datas["player_surname"]) + ", Date de naissance : "
                  + str(datas["player_birthday"]) + ", Genre : " + str(datas["player_gender"])
                  + ", Classement : " + str(datas["player_rank"]))


class ReportTournamentController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec tous les tournois.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.player_pool = self.db.table('player_pool')
        self.player_in_tournament = []

    def run(self):
        self.creationReport()
        return ReportMenuController()

    def creationReport(self):
        # Listing de tous les tournois dans la BDD des tournois
        for datas in self.tournament_table.all():
            print("ID : " + str(datas["Tournament_Id"]) + ", Nom : " + str(datas["Name"])
                  + ", Lieu : " + str(datas["Location"]) + ", Date : " + str(datas["Date"])
                  + ", Nombre de rounds : " + str(datas["Round"]) + ", Type de temps : "
                  + str(datas["Time"]) + ", Description : " + str(datas["Description"]))

        print("\n Voulez-vous :")
        print("==============================")
        print("1. Voir les tours d'un tournoi spécifique")
        print("2. Voir les matchs d'un tournoi spécifique")
        print("3. Voir les joueurs d'un tournoi spécifique")
        print("4. Retourner au menu")

        wrong_choice = True
        while wrong_choice is True:
            # on vérifie qu'il y a un tournoi dans la BDD
            if len(self.tournament_table.all()) == 0:
                print("Pas de tournois joués")
                break
            user_choice = input("Que voulez-vous faire? ")
            # Voir les tours d'un tournoi spécifique
            try:
                tournament_choice = int(input("Séléctionnez le tournoi (ID):"))
                # on va chercher l'ID du tournoi dansl a BDD des tournois
                tournament_user_choice = self.tournament_table.search(where("Tournament_Id") == tournament_choice)
                wrong_choice = False
                user_test = str(tournament_user_choice[0]["Tournament_Id"])
            except (IndexError, ValueError):
                print("Veuillez entrer un ID correcte")
                wrong_choice = True
                continue
            if user_choice == "1" and wrong_choice is False:
                wrong_choice = False

                print("")
                print("ID : " + user_test + ", Nom : " + str(tournament_user_choice[0]["Name"])
                      + ", Lieu : " + str(tournament_user_choice[0]["Location"]) + ", Date : " + str(tournament_user_choice[0]["Date"])
                      + ", Nombre de rounds : " + str(tournament_user_choice[0]["Round"]) + ", Type de temps : "
                      + str(tournament_user_choice[0]["Time"]) + ", Description : " + str(tournament_user_choice[0]["Description"]))
                # on charge le 1er Round si une sauvegarde a été faites après celui-ci
                if tournament_user_choice[0]["save_step"] >= 3:
                    print("Joueurs : " + str(tournament_user_choice[0]["players"]))
                    print("")
                    print("Matchs joués :")
                    print("Round 1 :")
                    print(str(tournament_user_choice[0]["matchs"][:4]))
                # on charge le 2eme Round si une sauvegarde a été faites après celui-ci
                if tournament_user_choice[0]["save_step"] >= 4:
                    print("Round 2 :")
                    print(str(tournament_user_choice[0]["matchs"][4:8]))
                # on charge le 3eme Round si une sauvegarde a été faites après celui-ci
                if tournament_user_choice[0]["save_step"] >= 5:
                    print("Round 3 :")
                    print(str(tournament_user_choice[0]["matchs"][8:-4]))
                # on charge le dernier Round si une sauvegarde a été faites après celui-ci
                if tournament_user_choice[0]["save_step"] >= 6:
                    print("Round 4 :")
                    print(str(tournament_user_choice[0]["matchs"][-4:]))
                print("")

            # Voir les matchs d'un tournoi spécifique
            elif user_choice == "2" and wrong_choice is False:

                print("")
                print("ID : " + str(tournament_user_choice[0]["Tournament_Id"]) + ", Nom : " + str(tournament_user_choice[0]["Name"])
                      + ", Lieu : " + str(tournament_user_choice[0]["Location"]) + ", Date : " + str(tournament_user_choice[0]["Date"])
                      + ", Nombre de rounds : " + str(tournament_user_choice[0]["Round"]) + ", Type de temps : "
                      + str(tournament_user_choice[0]["Time"]) + ", Description : " + str(tournament_user_choice[0]["Description"]))
                print("Joueurs : " + str(tournament_user_choice[0]["players"]))
                print("")
                print("Matchs joués :")
                print(str(tournament_user_choice[0]["matchs"]))

            # Voir les joueurs d'un tournoi spécifique
            elif user_choice == "3" and wrong_choice is False:
                if tournament_user_choice[0]["save_step"] >= 2:
                    for datas in tournament_user_choice[0]["players"]:
                        self.player_in_tournament.append(self.player_pool.search(where("Player_Id") == datas[1])[0])

                    print("\n Voulez-vous :")
                    print("==============================")
                    print("1. Trier l'ensemble par ordre Alphabétique")
                    print("2. Trier l'ensemble par Rang")

                    wrong_choice = True
                    while wrong_choice is True:
                        user_choice = input("Que voulez-vous faire? ")
                        # Trier l'ensemble des joueurs du tournoi par ordre Alphabétiqu
                        if user_choice == "1":
                            wrong_choice = False
                            sorted_list = sorted(self.player_in_tournament, key=lambda item: item["player_name"])
                            for datas in sorted_list:
                                print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["player_name"])
                                      + ", Prénom : " + str(datas["player_surname"]) + ", Date de naissance : "
                                      + str(datas["player_birthday"]) + ", Genre : " + str(datas["player_gender"])
                                      + ", Classement : " + str(datas["player_rank"]))
                        # Trier l'ensemble des joueurs du tournoi par rang
                        elif user_choice == "2":
                            wrong_choice = False
                            sorted_list = sorted(self.player_in_tournament, key=lambda item: item["player_rank"])
                            for datas in sorted_list:
                                print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["player_name"])
                                      + ", Prénom : " + str(datas["player_surname"]) + ", Date de naissance : "
                                      + str(datas["player_birthday"]) + ", Genre : " + str(datas["player_gender"])
                                      + ", Classement : " + str(datas["player_rank"]))
                        else:
                            wrong_choice = True
                            print("Veuillez saisir un entrée valide (1)")
                        continue
                else:
                    print("Aucun joueur n'a été inséré dans un match")

            # Retour au menu d'accueil
            elif user_choice == "4" and wrong_choice is False:
                return EndController()

            else:
                print("Veuillez saisir un entrée valide (2)")

            continue


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
