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
        self.tournamentTable = self.db.table('tournament_table')
        self.view = views.HomeView()

    def run(self):
        # Menu d'accueil
        self.view.render()
        next_action = self.view.get_user_choice()

        # Créer un nouveau tournoi
        if next_action == "1":
            # mise en place des variables nécessaires au fonctionnement
            # de la fonction de reprise de tournoi
            Load_state = False
            Save_step = 0
            middleNumberPlayers = 0
            first_halfPlayers = []
            second_halfPlayers = []
            totalMatch = []
            playersSorted = []
            match = []
            playerList = []

            # teste de présence de données dans la BDD des tournois
            if len(self.tournamentTable.all()) == 0:
                last_index = 0
            else:
                # on définie le prochain ID utilisable de la table des tournois
                tournamentTable = self.tournamentTable.all()
                sorted_list = sorted(tournamentTable, key=lambda
                                     item: item["Tournament_Id"])
                last_index = list(sorted_list)[-1]["Tournament_Id"] + 1

            tournament_index = last_index

            # lancement de la class permettant de créer un tournoi
            return ManualRoundCreationController(
                    Load_state, Save_step, tournament_index,
                    middleNumberPlayers, first_halfPlayers, second_halfPlayers,
                    totalMatch, playersSorted, match, playerList)

        # Créer un nouveau joueur
        elif next_action == "2":
            return PlayerMenuController()

        # Créer un nouveau rapport
        elif next_action == "3":
            return ReportMenuController()

        # Reprendre un tournoi
        elif next_action == "4":
            # on vérifie qu'il y a un tournoi dans la BDD
            if len(self.tournamentTable.all()) == 0:
                print("Pas de tournois joués")
            else:
                # activation de la variable permettant le chargement de tournoi
                Load_state = True
                # listing de l'ensemble des tournois renseignés dans la BDD
                for datas in self.tournamentTable.all():
                    print("Tournoi : " + str(datas.get('Tournament_Id')) + " | Nom : " + str(datas.get('Name')))
                # demande à l'utilisateur du choix de l'ID de son tournoi
                tournamentChoice = input("Séléctionnez le tournoi (ID):")

                tournament_index = int(tournamentChoice)
                # recherche du tournoi choisi par l'utilisateur
                this_tournament = self.tournamentTable.search(where
                                                              ("Tournament_Id") == tournament_index)[0]
                # mise en mémoire de l'étape de la sauvegarde du tournoi
                Save_step = this_tournament["Save_step"]
                # mise en place des variables nécessaires au fonctionnement
                # de la fonction de reprise de tournoi
                middleNumberPlayers = 0
                first_halfPlayers = []
                second_halfPlayers = []
                totalMatch = []
                playersSorted = []
                match = []
                playerList = []
                # si les joueurs ont déjà été choisi, il faut renseigner certaines variables
                if Save_step >= 2:
                    playerList = [1, 2, 3, 4, 5, 6, 7, 8]
                    middleNumberPlayers = int(len(self.tournamentTable.search
                                                  (where("Tournament_Id") == tournament_index)[0]["players"])/2)
                    first_halfPlayers = playerList[:middleNumberPlayers]
                    second_halfPlayers = playerList[middleNumberPlayers:]
                # si un match a déjà été joué, il faut renseigner des variables supplémentaires
                if Save_step >= 3:
                    totalMatch = this_tournament["matchs"]
                    # on charge le dernier round joué
                    match = this_tournament["matchs"][-4:]
                    playersToSort = []
                    for datas in match:
                        playersToSort.append(datas[0])
                        playersToSort.append(datas[1])
                    # Tri des joueurs par rang
                    playersToSort.sort()
                    # Tri des joueurs par rang et par score
                    playersToSort.sort(key=self.getScore, reverse=True)
                    playersSorted = playersToSort

                return ManualRoundCreationController(
                    Load_state, Save_step, tournament_index,
                    middleNumberPlayers, first_halfPlayers,
                    second_halfPlayers, totalMatch, playersSorted,
                    match, playerList)
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

    def __init__(self, Load_state, Save_step,
                 tournament_index, middleNumberPlayers,
                 first_halfPlayers, second_halfPlayers,
                 totalMatch, playersSorted, match, playerList):
        self.db = TinyDB('db.json')

        # variable de chargement de tournoi
        self.Load_state = Load_state
        self.Save_step = Save_step

        # --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
        self.tournamentTable = self.db.table('tournament_table')
        self.playerPool = self.db.table('player_pool')
        self.playerTable = self.db.table('player_table')

        # --- CREATION DE LA LISTE DES JOUEURS --- #
        self.playerList = playerList
        self.playerListToSort = []
        self.playerListByRank = []

        # --- DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE --- #
        self.middleNumberPlayers = middleNumberPlayers
        self.first_halfPlayers = first_halfPlayers
        self.second_halfPlayers = second_halfPlayers

        # --- Définition des variables générales--- #
        self.tournament_index = tournament_index
        self.nbPlayers = 0
        self.last_index = 0
        self.playerRank = 0
        self.playerMatch = []
        self.totalMatch = totalMatch
        self.playersToSort = []
        self.playersSorted = playersSorted
        self.match = match
        self.matchToPlay = []
        self.playerOrder = []

    def run(self):

        # --- ETAPE 0 DE SAUVEGARDE --- #
        if self.Load_state is False:
            # renseignement des informations concernant le tournoi
            tournamentName = input("Entrez le nom du tournoi : ")
            tournamentLocation = input("Entrez le lieu du tournoi : ")
            tournamentDate = input("Entrez la date du tournoi : ")
            tournamentRound = int(4)
            tournamentTime = input("Entrez le temps du tournoi : ")
            tournamentDescription = input("Entrez la description du tournoi : ")

            # définition de l'étape de sauvegarde au niveau 1
            self.Save_step = 1
            tournamentData = {"Tournament_Id": self.tournament_index, "Name": tournamentName,
                              "Location": tournamentLocation, "Date": tournamentDate,
                              "Round": tournamentRound, "Time": tournamentTime,
                              "Description": tournamentDescription, "Save_step": self.Save_step}
            # sauvegarde des données renseignées dans la BDD
            self.tournamentTable.insert(tournamentData)

        # --- ETAPE 1 DE SAUVEGARDE --- #
        # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.Load_state is True and self.Save_step == 1) or self.Load_state is False:

            # --- INSERTION DES DONNEES JOUEURS --- #
            # Index permettant de créer un joueur automatiquement
            i = 0
            # Boucle permettant d'ajouter 8 joueurs ont bien été renseigné dans le tournoi
            while len(self.playerListToSort) < 8:
                i += 1
                # Menu de choix de la manière d'insérer un joueur das le tournoi
                print("Voulez-vous :")
                print("==============================")
                print("1. Ajouter un joueur déjà éxistant")
                print("2. Créer un nouveau joueur (Manuel)")
                print("3. Créer un nouveau joueur (Automatique)")

                wrongChoice = True
                # permet de boucler tant qu'un choix invalide est détécté
                while wrongChoice is True:
                    userChoice = input("Que voulez-vous faire? ")
                    # Ajouter un joueur déjà éxistant
                    if userChoice == "1":
                        wrongChoice = False
                        self.playerChoice()
                    # Créer un nouveau joueur (Manuel)
                    elif userChoice == "2":
                        wrongChoice = False
                        self.creationPlayer()
                    # Créer un nouveau joueur (Automatique)
                    elif userChoice == "3":
                        wrongChoice = False
                        playerName = "Name" + str(i)
                        playerSurname = "Surname" + str(i)
                        playerBirthdate = "BDate" + str(i)
                        playerGender = "Gender" + str(i)

                        # Test de la présence de donnée dans la BDD
                        if len(self.playerPool.all()) == 0:
                            self.last_index = 0
                        else:
                            # Définition du prochain ID valide dans la BDD
                            playerPool = self.playerPool.all()
                            sorted_list = sorted(playerPool, key=lambda
                                                 item: item["Player_Id"])
                            print("Joueur automatique crée \n")
                            self.last_index = list(sorted_list)[-1]["Player_Id"] + 1

                        # choix aléatoire d'une côte
                        self.playerRank = random.randint(0, 1500)
                        playerData = {"Player_Id": self.last_index, "playerName": playerName,
                                      "playerSurname": playerSurname, "playerBirthdate": playerBirthdate,
                                      "playerGender": playerGender, "playerRank": self.playerRank}
                        # Insertion des données dans la BDD de joueurs
                        self.playerPool.insert(playerData)
                    else:
                        wrongChoice = True
                        print("Veuillez saisir un entrée valide")

                # Ajout des joueurs et de leur rang avant tri
                self.playerListToSort.append([(self.last_index), self.playerRank])
                self.playerList.append(i)
                continue

            # Tri des joueurs par Rang
            playerListSorted = sorted(self.playerListToSort, key=lambda
                                      item: item[1], reverse=True)

            # Ajout d'un index aux joueurs pour connaître leur classement
            i = 0
            # Boucle sur l'ensemble des données triés pour pouvoir les insérer en BDD après
            for datas in playerListSorted:
                i += 1
                self.playerListByRank.append((i, datas[0], datas[1]))

            # Définition des 4 premiers joueurs et des 4 derniers joueurs
            self.nbPlayers = len(self.playerList)
            self.middleNumberPlayers = int(self.nbPlayers/2)
            self.first_halfPlayers = self.playerList[:self.middleNumberPlayers]
            self.second_halfPlayers = self.playerList[self.middleNumberPlayers:]

            # Définition de l'étape de sauvegarde à 2, après le classement des joueurs
            self.Save_step = 2
            tournamentData = {"players": self.playerListByRank,
                              "Save_step": self.Save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournamentTable.update(tournamentData,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 2 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.Load_state is True and self.Save_step == 2) or self.Load_state is False:

            # --- ROUND 1 --- #
            print()
            print("ROUND 1 :")

            # Boucle permettant de matcher les joueurs de la moitié supèrieure
            # avec les joueurs de la moitié infèrieure respéctive
            for i in range(self.middleNumberPlayers):
                wrongChoice = True
                # Boucle permettant d'assurer un choix valide
                while wrongChoice is True:
                    firstPlayerIndex = self.tournamentTable.search(where("Tournament_Id") ==
                                                                   self.tournament_index)[0]["players"][i][1]
                    secondPlayerIndex = self.tournamentTable.search(where("Tournament_Id") ==
                                                                    self.tournament_index)[0]["players"][i+4][1]
                    firstPlayerData = self.playerPool.search(where("Player_Id") ==
                                                             firstPlayerIndex)[0]["playerName"]
                    secondPlayerData = self.playerPool.search(where("Player_Id") ==
                                                              secondPlayerIndex)[0]["playerName"]
                    print("Joueur " + str(i+1) + " " + str(firstPlayerData) + " (" + str(firstPlayerIndex) + ")" +
                          " contre Joueur " + str(i+5) + " " +
                          str(secondPlayerData) + " (" + str(secondPlayerIndex) + ")")
                    matchWinner = input("Entrez le numéro du gagnant (0 = égalité) : ")
                    # définition des points alloués aux gagnants et aux perdants
                    scoreW = 1
                    scoreL = 0
                    # ensemble Try Except permettant d'éviter les erreures de saisies
                    try:
                        # teste si le joueur ayant gagné est celui de la moitié supèrieure
                        if int(matchWinner) == self.first_halfPlayers[i]:
                            wrongChoice = False
                            matchLoser = self.second_halfPlayers[i]
                            print("Gagnant : " + str(matchWinner) + " ; Perdant : " + str(matchLoser) + "\n")
                        # teste si le joueur ayant gagné est celui de la moitié infèrieure
                        elif int(matchWinner) == self.second_halfPlayers[i]:
                            wrongChoice = False
                            matchLoser = self.first_halfPlayers[i]
                            print("Gagnant : " + str(matchWinner) + " ; Perdant : " + str(matchLoser) + "\n")
                        # teste si les joueurs ont fait une égalité
                        elif int(matchWinner) == 0:
                            wrongChoice = False
                            scoreW = 0.5
                            scoreL = 0.5
                            matchWinner = self.first_halfPlayers[i]
                            matchLoser = self.second_halfPlayers[i]
                            print("Égalité entre le Joueur : " + str(self.first_halfPlayers[i]) +
                                  " et le Joueur : " + str(self.second_halfPlayers[i]) + "\n")
                        else:
                            continue

                    except ValueError:
                        continue

                # On ajoute le gagnant et le perdant de la partie avec leurs scores réspectifs
                self.totalMatch.append(([int(matchWinner), scoreW], [int(matchLoser), scoreL]))

            # Ajout des joueurs avec leurs points préparant le tri
            for i in range(self.middleNumberPlayers):
                self.playersToSort.append(self.totalMatch[i][0])
                self.playersToSort.append(self.totalMatch[i][1])

            # Tri des joueurs par rang
            self.playersToSort.sort()

            # Tri des joueurs par rang et par score
            self.playersToSort.sort(key=self.getScore, reverse=True)
            self.playersSorted = self.playersToSort

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 3, après le Round 1
            self.Save_step = 3
            tournamentData = {"matchs": self.totalMatch, "Save_step": self.Save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournamentTable.update(tournamentData,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 3 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.Load_state is True and self.Save_step == 3) or self.Load_state is False:

            # --- ROUND 2 --- #
            print()
            print("ROUND 2 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.getPlayerMatchs()

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 4, après le Round 2
            self.Save_step = 4
            tournamentData = {"matchs": self.totalMatch, "Save_step": self.Save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournamentTable.update(tournamentData,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 4 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.Load_state is True and self.Save_step == 4) or self.Load_state is False:

            # --- ROUND 3 --- #
            print()
            print("ROUND 3 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.getPlayerMatchs()

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 5, après le Round 3
            self.Save_step = 5
            tournamentData = {"matchs": self.totalMatch, "Save_step": self.Save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournamentTable.update(tournamentData,
                                        Query().Tournament_Id == self.tournament_index)

            # --- ETAPE 5 DE SAUVEGARDE --- #
            # test de l'étape de sauvegarde en cas de reprise de tournoi
        if (self.Load_state is True and self.Save_step == 5) or self.Load_state is False:

            # --- ROUND 4 --- #
            print()
            print("ROUND 4 :")

            # Lancement de la fonction permettant de jouer un round complet
            self.getPlayerMatchs()

            # impression des scores des joueurs du tournoi
            self.getTournamentRanking()

            # Définition de l'étape de sauvegarde à 6, après le Round 4
            self.Save_step = 6
            tournamentData = {"matchs": self.totalMatch, "Save_step": self.Save_step}
            # Mise à jour du tournoi correspondant dans la BDD des tournois
            self.tournamentTable.update(tournamentData,
                                        Query().Tournament_Id == self.tournament_index)

    # fonction de séléction des joueurs
    def playerChoice(self):
        # listing de l'ensemble des joueurs présents dans la BDD
        for datas in self.playerPool.all():
            print("ID :" + str(datas.get('Player_Id')) + " , Joueur : " + str(datas.get('playerName')))
        if len(self.playerPool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            wrongChoice = True
            # boucle permettant d'éviter un choix éronné
            while wrongChoice is True:
                playerChoice = input("Séléctionnez l'ID du joueur :")
                try:
                    # recherche dans la BDD des joueurs l'ID demandé
                    playerId = self.playerPool.search(where("Player_Id") == int(playerChoice))[0]

                    # test permettant de savoir si des joueurs ont déjà été inséré
                    if len(self.playerListToSort) != 0:
                        wrongChoice = False
                        # boucle sur l'ensemble des joueurs inséré pour vérifier s'il y a un doublon
                        for i in range(len(self.playerListToSort)):
                            if self.playerListToSort[i][0] == playerId["Player_Id"]:
                                print("Veuillez entrer un nouveau joueur (ID déjà rentré)")
                                wrongChoice = True
                                break
                        # ajout des informations nécessaire à l'insertion d'un joueur dans un tournoi
                        self.playerRank = playerId["playerRank"]
                        self.last_index = playerId["Player_Id"]
                        continue
                    else:
                        # ajout des informations nécessaire à l'insertion d'un joueur dans un tournoi
                        # si aucun joueur n'avait été inséré auparavant
                        self.playerRank = playerId["playerRank"]
                        self.last_index = playerId["Player_Id"]
                        wrongChoice = False
                except (IndexError, ValueError):
                    print("Veuillez entrer une ID correcte")
                continue

    # création des joueurs
    def creationPlayer(self):
        # renseignement des informations nécéssaires à l'insertion d'un nouveau joueur
        playerName = input("Entrez le nom du joueur : ")
        playerSurname = input("Entrez le prénom du joueur : ")
        playerBirthdate = input("Entrez la date de naissance du joueur : ")
        playerGender = input("Entrez le genre du joueur : ")
        wrongChoice = True

        # on évite les erreurs de saisie dans le rang du joueur
        while wrongChoice is True:
            try:
                self.playerRank = abs(int(input("Entrez le rang du joueur : ")))
                wrongChoice = False
                continue
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                continue

        # Teste s'il y a des joueurs dans la BDD correspondante
        if len(self.playerPool.all()) == 0:
            self.last_index = 0
        # Définie le prochain ID disponible pour l'ajout de joueurs
        else:
            playerPool = self.playerPool.all()
            sorted_list = sorted(playerPool, key=lambda item: item["Player_Id"])
            self.last_index = list(sorted_list)[-1]["Player_Id"] + 1

        playerData = {"Player_Id": self.last_index, "playerName": playerName,
                      "playerSurname": playerSurname, "playerBirthdate": playerBirthdate,
                      "playerGender": playerGender, "playerRank": self.playerRank}

        # insert dans la BDD des joueurs le nouveau joueur
        self.playerPool.insert(playerData)

    # fonction globale permettant d'assurer les rounds 2 à 4
    def getPlayerMatchs(self):
        self.playerMatch.clear()
        self.playerOrder.clear()
        # on prépare les données de joueurs pour mettre en
        # place les paires du round
        # on insert l'ensemble des matchs dans une liste
        # pour ne pas avoir de matchs doublons
        for matchs in self.totalMatch:
            self.playerMatch.append(matchs)
        # on insert les joueurs par rapport à leur score
        # et leur rang dans une variable
        for player in self.playersSorted:
            self.playerOrder.append(player[0])
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
        self.matchToPlay.clear()
        # on boucle sur les joueurs du tournoi, du 1er au dernier
        for players in self.playerOrder:
            playedMatchs = []
            # on boucle sur les matchs déjà joué lors du tournoi
            for plays in self.totalMatch:
                player1 = plays[0][0]
                player2 = plays[1][0]
                # on teste si le joueur 1 est le joueur sur lequel
                # on boucle pour connaître son adversaire
                if player1 == players:
                    playedMatchs.append(player2)
                # on teste si le joueur 2 est le joueur sur lequel
                # on boucle pour connaître son adversaire
                elif player2 == players:
                    playedMatchs.append(player1)
            # on appelle la fonction permettant de mettre
            # un adversaire face à un autre
            self.sortMatch(playedMatchs, players)
        pass

    # fonction permettant de mettre un joueur face à un
    # autre sans doublon de match
    def sortMatch(self, playedMatchs, players):
        for i in range(len(self.playerOrder)):
            # on teste si le joueur n'a pas déjà été aloué
            # a un autre match dans ce round, s'il n'a pas
            # déjà été joué ou si on ne met pas un joueur
            # face à lui même
            if players != self.playerOrder[i] and \
                         (self.playerOrder[i] in playedMatchs) is False and \
                         ((players in self.matchToPlay) is False and
                          (self.playerOrder[i] in self.matchToPlay) is False):
                self.matchToPlay.append(players)
                self.matchToPlay.append(self.playerOrder[i])
                break

    # fonction permettant de gérer le cas particulier des 2
    # derniers joueurs ayant déjà joué ensemble
    def matchToAdd(self):
        # on met i à 3 pour garder les 4 derniers joueurs dans
        # notre piscine de joueurs à mettre en face
        i = 3
        # on teste si tous les matchs ont été alloué ou non.
        while len(self.matchToPlay) < len(self.playerList) \
                and i <= len(self.playerList):
            i += 1
            # on récupère les 4+ derniers joueurs pour trouver un match à jouer
            newPlayerOrder = self.playerOrder[-i:]
            # on mélange les joueurs pour trouver un match à jouer
            random.shuffle(newPlayerOrder)
            self.playerOrder = self.playerOrder[:4]
            # on ajoute les joueurs ayant été mis face à face pour
            # tester s'ils ont déjà joués ensemble
            for players in newPlayerOrder:
                self.playerOrder.append(players)
            # on appelle la fonction permettant de connaître quels
            # match ont été joué par nos joueurs
            self.matchPlayed()
            # si le nombre de joueurs présents dans le tournoi n'est
            # pas équivalent à celui de joueurs a qui on a trouvé un
            # match, on continue la boucle
            if len(self.matchToPlay) < len(self.playerList):
                continue

    # on associe les différents joueurs entre eux
    # après le filtrage évitant les doublons
    def sortPlayersByMatch(self):
        # on boucle sur l'ensemble des joueurs à coupler dans un match
        for players in self.matchToPlay:
            # on boucle sur l'ensemble des joueurs présent dans le tri effectué
            for i in range(len(self.playerList)):
                # on récupère les joueurs et leurs scores dans l'ordre
                if players == self.playersSorted[i][0]:
                    self.playersSorted.append(self.playersSorted[i])
                    # on supprime les joueurs déjà trouvés
                    del self.playersSorted[i]

    # on joue les matchs crées auparavant
    def playMatch(self):
        self.match.clear()

        # on boucle sur les joueurs avec un pas de 2 pour ne pas rejouer des matchs
        for i in range(0, len(self.playerList), 2):

            wrongChoice = True
            # Boucle évitant les erreurs de saisie
            while wrongChoice is True:
                firstPlayerIndex = self.tournamentTable.search(where("Tournament_Id") ==
                                                               self.tournament_index)[0]["players"][i][1]
                secondPlayerIndex = self.tournamentTable.search(where("Tournament_Id") ==
                                                                self.tournament_index)[0]["players"][i+1][1]
                firstPlayerData = self.playerPool.search(where("Player_Id") ==
                                                         firstPlayerIndex)[0]["playerName"]
                secondPlayerData = self.playerPool.search(where("Player_Id") ==
                                                          secondPlayerIndex)[0]["playerName"]
                print("Joueur " + str(self.playersSorted[i][0]) + " " +
                      str(firstPlayerData) + " (" + str(firstPlayerIndex) + ")" +
                      " contre Joueur " + str(self.playersSorted[i+1][0]) + " " +
                      str(secondPlayerData) + " (" + str(secondPlayerIndex) + ")")
                matchWinner = input("Entrez le numéro du Joueur gagnant (0 = égalité) : ")

                try:
                    # on teste si le 1er joueur des 2 est le gagnant
                    if int(matchWinner) == self.playersSorted[i][0]:
                        wrongChoice = False
                        # le 2ème joueur est alors perdant
                        matchLoser = self.playersSorted[i+1][0]
                        # on reprend les scores de chaques joueurs et on met à jour
                        scoreW = self.playersSorted[i][1] + 1
                        scoreL = self.playersSorted[i+1][1]
                        print("Gagnant : " + str(matchWinner) + " ; Perdant : " + str(matchLoser))
                    # on teste si le 2ème joueur des 2 est le gagnant
                    elif int(matchWinner) == self.playersSorted[i+1][0]:
                        wrongChoice = False
                        # le 1er joueur est alors perdant
                        matchLoser = self.playersSorted[i][0]
                        # on reprend les scores de chaques joueurs et on met à jour
                        scoreW = self.playersSorted[i+1][1] + 1
                        scoreL = self.playersSorted[i][1]
                        print("Gagnant : " + str(matchWinner) + " ; Perdant : " + str(matchLoser))
                    # on teste s'il y a eu égalité entre les joueurs
                    elif int(matchWinner) == 0:
                        wrongChoice = False
                        # on reprend les scores de chaques joueurs et on met à jour
                        scoreW = self.playersSorted[i][1] + 0.5
                        scoreL = self.playersSorted[i+1][1] + 0.5
                        matchWinner = self.playersSorted[i][0]
                        matchLoser = self.playersSorted[i+1][0]
                        print("Égalité entre le Joueur : " + str(self.playersSorted[i][0]) +
                              " et le Joueur : " + str(self.playersSorted[i+1][0]))
                    else:
                        continue

                except ValueError:
                    continue

            print("")
            # on ajoute les résultats aux variables
            self.match.append(([int(matchWinner), scoreW], [int(matchLoser), scoreL]))
            self.totalMatch.append(([int(matchWinner), scoreW], [int(matchLoser), scoreL]))

    # permet le tri par rang et par score
    def getScore(self, elem):
        return elem[1]

    # permet d'afficher le classement
    def getTournamentRanking(self):
        for datas in self.playersSorted:
            IdFounded = False
            while IdFounded is False:
                for i in range(len(self.playersSorted)):
                    PlayerIndex = self.tournamentTable.search(where("Tournament_Id") ==
                                                              self.tournament_index)[0]["players"][i][0]
                    if datas[0] == PlayerIndex:
                        PlayerIndex = self.tournamentTable.search(where("Tournament_Id") ==
                                                                  self.tournament_index)[0]["players"][i][1]
                        IdFounded = True
                        break
                    else:
                        continue

            PlayerData = self.playerPool.search(where("Player_Id") ==
                                                PlayerIndex)[0]
            print("Joueur " + str(i+1) + " " + str(PlayerData["playerName"]) +
                  " (" + str(PlayerData["Player_Id"]) + ") | Points : " + str(datas[1]))

    # on trie les joueurs par rapport à leur score et leur rang
    def sortPlayersByScore(self):
        self.playersToSort.clear()
        self.match = self.totalMatch[-4:]

        # on ajoute les tuples à la variable pour pouvoir trier l'ensemble
        for i in range(self.middleNumberPlayers):
            self.playersToSort.append(self.match[i][0])
            self.playersToSort.append(self.match[i][1])

        # Tri des joueurs par rang
        self.playersToSort.sort()

        # Tri des joueurs par rang et par score
        self.playersToSort.sort(key=self.getScore, reverse=True)
        self.playersSorted = self.playersToSort


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
        self.playerPool = self.db.table('player_pool')

    def run(self):
        self.creationPlayer()
        return PlayerMenuController()

    def creationPlayer(self):
        # renseignement des informations concernant le joueur
        playerName = input("Entrez le nom du joueur : ")
        playerSurname = input("Entrez le prénom du joueur : ")
        playerBirthdate = input("Entrez la date de naissance du joueur : ")
        playerGender = input("Entrez le genre du joueur : ")
        wrongChoice = True

        # on évite les erreurs de saisie dans le rang du joueur
        while wrongChoice is True:
            try:
                playerRank = abs(int(input("Entrez le rang du joueur : ")))
                wrongChoice = False
                continue
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                continue

        # définition de l'index du joueur a créer
        # on vérifie si la base de donnée n'a pas encore de joueurs
        if len(self.playerPool.all()) == 0:
            last_index = 0
        else:
            # on regarde quel est le prochain index disponible dans la BDD des joueurs
            playerPool = self.playerPool.all()
            sorted_list = sorted(playerPool, key=lambda item: item["Player_Id"])
            last_index = list(sorted_list)[-1]["Player_Id"] + 1

        playerData = {"Player_Id": last_index, "playerName": playerName,
                      "playerSurname": playerSurname, "playerBirthdate": playerBirthdate,
                      "playerGender": playerGender, "playerRank": int(playerRank)}

        # insertion des données du joueur dans la BDD correspondante
        self.playerPool.insert(playerData)

        print("Le joueur a été crée")


class PlayerRankController:
    """Contrôleur responsable de gérer le menu de
    modification du rang d'un joueur.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.playerPool = self.db.table('player_pool')

    def run(self):
        if len(self.playerPool.all()) == 0:
            print("Pas de joueurs crées")
        else:
            self.rankPlayer()
        return PlayerMenuController()

    def rankPlayer(self):
        # visualisation des joueurs présent dans la BDD
        playerPool = self.playerPool.all()
        for datas in playerPool:
            print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"])
                  + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                  + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"])
                  + ", Classement : " + str(datas["playerRank"]))

        wrongChoice = True
        while wrongChoice is True:
            try:
                playerChoice = int(input("Séléctionnez le joueur (ID):"))
                # on va chercher l'ID du joueur dans la BDD des joueurs
                user_Choice = self.playerPool.search(where("Player_Id") == playerChoice)
                wrongChoice = False
                playerRank = str(user_Choice[0]["playerRank"])
            except (IndexError, ValueError):
                print("Veuillez entrer un ID correcte")
                wrongChoice = True
                continue

        wrongChoice = True
        while wrongChoice is True:
            try:
                print("Rang actuel du joueur : " + playerRank)
                newRank = abs(int(input("Quel est le nouveau rang du joueur?")))
                wrongChoice = False
            except (IndexError, ValueError):
                print("Veuillez entrer un rang correcte")
                wrongChoice = True
                continue

        playerData = {"playerRank": newRank}
        # Mise à jour du joueur correspondant dans la BDD des joueurs
        self.playerPool.update(playerData,
                               Query().Player_Id == playerChoice)


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
        self.playerPool = self.db.table('player_pool')

    def run(self):
        if len(self.playerPool.all()) == 0:
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

        wrongChoice = True
        while wrongChoice is True:
            userChoice = input("Que voulez-vous faire? ")
            # Trier l'ensemble par ordre Alphabétique
            if userChoice == "1":
                wrongChoice = False
                self.player_SortName()
            # Trier l'ensemble par Rang
            elif userChoice == "2":
                wrongChoice = False
                self.player_SortRank()
            # retour à l'accueil
            elif userChoice == "3":
                wrongChoice = False
                return EndController()
            else:
                wrongChoice = True
                print("Veuillez saisir un entrée valide")
            continue

    # Fonction de tri des joueurs par Noms
    def player_SortName(self):
        playerPool = self.playerPool.all()
        sorted_list = sorted(playerPool, key=lambda item: item["playerName"])
        for datas in sorted_list:
            print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"])
                  + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                  + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"])
                  + ", Classement : " + str(datas["playerRank"]))

    # Fonction de tri des joueurs par Rang
    def player_SortRank(self):
        playerPool = self.playerPool.all()
        sorted_list = sorted(playerPool, key=lambda item: item["playerRank"])
        for datas in sorted_list:
            print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"])
                  + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                  + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"])
                  + ", Classement : " + str(datas["playerRank"]))


class ReportTournamentController:
    """Contrôleur responsable de gérer la création d'un nouveau
    rapport avec tous les tournois.
    """

    def __init__(self):
        self.db = TinyDB('db.json')
        self.tournamentTable = self.db.table('tournament_table')
        self.playerPool = self.db.table('player_pool')
        self.playerInTournament = []

    def run(self):
        self.creationReport()
        return ReportMenuController()

    def creationReport(self):
        # Listing de tous les tournois dans la BDD des tournois
        for datas in self.tournamentTable.all():
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

        wrongChoice = True
        while wrongChoice is True:
            # on vérifie qu'il y a un tournoi dans la BDD
            if len(self.tournamentTable.all()) == 0:
                print("Pas de tournois joués")
                break
            userChoice = input("Que voulez-vous faire? ")
            # Voir les tours d'un tournoi spécifique
            try:
                tournamentChoice = int(input("Séléctionnez le tournoi (ID):"))
                # on va chercher l'ID du tournoi dansl a BDD des tournois
                user_Choice = self.tournamentTable.search(where("Tournament_Id") == tournamentChoice)
                wrongChoice = False
                userTest = str(user_Choice[0]["Tournament_Id"])
            except (IndexError, ValueError):
                print("Veuillez entrer un ID correcte")
                wrongChoice = True
                continue
            if userChoice == "1" and wrongChoice is False:
                wrongChoice = False

                print("")
                print("ID : " + userTest + ", Nom : " + str(user_Choice[0]["Name"])
                      + ", Lieu : " + str(user_Choice[0]["Location"]) + ", Date : " + str(user_Choice[0]["Date"])
                      + ", Nombre de rounds : " + str(user_Choice[0]["Round"]) + ", Type de temps : "
                      + str(user_Choice[0]["Time"]) + ", Description : " + str(user_Choice[0]["Description"]))
                # on charge le 1er Round si une sauvegarde a été faites après celui-ci
                if user_Choice[0]["Save_step"] >= 3:
                    print("Joueurs : " + str(user_Choice[0]["players"]))
                    print("")
                    print("Matchs joués :")
                    print("Round 1 :")
                    print(str(user_Choice[0]["matchs"][:4]))
                # on charge le 2eme Round si une sauvegarde a été faites après celui-ci
                if user_Choice[0]["Save_step"] >= 4:
                    print("Round 2 :")
                    print(str(user_Choice[0]["matchs"][4:8]))
                # on charge le 3eme Round si une sauvegarde a été faites après celui-ci
                if user_Choice[0]["Save_step"] >= 5:
                    print("Round 3 :")
                    print(str(user_Choice[0]["matchs"][8:-4]))
                # on charge le dernier Round si une sauvegarde a été faites après celui-ci
                if user_Choice[0]["Save_step"] >= 6:
                    print("Round 4 :")
                    print(str(user_Choice[0]["matchs"][-4:]))
                print("")

            # Voir les matchs d'un tournoi spécifique
            elif userChoice == "2" and wrongChoice is False:

                print("")
                print("ID : " + str(user_Choice[0]["Tournament_Id"]) + ", Nom : " + str(user_Choice[0]["Name"])
                      + ", Lieu : " + str(user_Choice[0]["Location"]) + ", Date : " + str(user_Choice[0]["Date"])
                      + ", Nombre de rounds : " + str(user_Choice[0]["Round"]) + ", Type de temps : "
                      + str(user_Choice[0]["Time"]) + ", Description : " + str(user_Choice[0]["Description"]))
                print("Joueurs : " + str(user_Choice[0]["players"]))
                print("")
                print("Matchs joués :")
                print(str(user_Choice[0]["matchs"]))

            # Voir les joueurs d'un tournoi spécifique
            elif userChoice == "3" and wrongChoice is False:
                if user_Choice[0]["Save_step"] >= 2:
                    for datas in user_Choice[0]["players"]:
                        self.playerInTournament.append(self.playerPool.search(where("Player_Id") == datas[1])[0])

                    print("\n Voulez-vous :")
                    print("==============================")
                    print("1. Trier l'ensemble par ordre Alphabétique")
                    print("2. Trier l'ensemble par Rang")

                    wrongChoice = True
                    while wrongChoice is True:
                        userChoice = input("Que voulez-vous faire? ")
                        # Trier l'ensemble des joueurs du tournoi par ordre Alphabétiqu
                        if userChoice == "1":
                            wrongChoice = False
                            sorted_list = sorted(self.playerInTournament, key=lambda item: item["playerName"])
                            for datas in sorted_list:
                                print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"])
                                      + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                                      + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"])
                                      + ", Classement : " + str(datas["playerRank"]))
                        # Trier l'ensemble des joueurs du tournoi par rang
                        elif userChoice == "2":
                            wrongChoice = False
                            sorted_list = sorted(self.playerInTournament, key=lambda item: item["playerRank"])
                            for datas in sorted_list:
                                print("ID : " + str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"])
                                      + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                                      + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"])
                                      + ", Classement : " + str(datas["playerRank"]))
                        else:
                            wrongChoice = True
                            print("Veuillez saisir un entrée valide")
                        continue
                else:
                    print("Aucun joueur n'a été inséré dans un match")

            # Retour au menu d'accueil
            elif userChoice == "4" and wrongChoice is False:
                return EndController()

            else:
                print("Veuillez saisir un entrée valide")

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
