import views

from tinydb import TinyDB, where, Query
from random import randint, random
import random 

# VOIR POUR LA REPRISE D'UN MATCH EN COURS (State depuis une class, puis reprise des données de la bdd)

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
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            # mettre la version création automatique de tournoi
            return AutomaticTournamentCreationController()
        elif next_action == "2":
            Load_state = False
            # return ManualTournamentCreationController()
            Save_step = 0
            return ManualRoundCreationController(Load_state, Save_step)
        elif next_action == "3":
            return PlayerMenuController()
        elif next_action == "4":
            return ReportMenuController()
        elif next_action == "5":
            Load_state = True
            # return ManualTournamentCreationController()

            for datas in self.tournamentTable.all():
                print("Tournoi : " + datas.get('Name'))
            tournamentChoice = input("Séléctionnez le tournoi :")
            Save_step = self.tournamentTable.search(where("Name") == tournamentChoice)[0]["Save_step"]
            # print(Save_step[0]["Save_step"])
            
            return ManualRoundCreationController(Load_state, Save_step)

        elif next_action == "6":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


class AutomaticTournamentCreationController:
    """Contrôleur responsable de gérer le menu de création d'un
    tournoi automatique."""

    def __init__(self):
        self.view = views.AutomaticTournamentCreationView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return AutomaticRoundCreationController()
        elif next_action == "2":
            return HomeController()
        elif next_action == "3":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return AutomaticTournamentCreationController()


class AutomaticRoundCreationController:
    """Mettre mes fonctions du main.py
    """

    def __init__(self):
        self.db = TinyDB('db.json')

        # mettre les variables avec .self et les fonctions en self.

        """CREATION DE LA LISTE DES JOUEURS"""
        self.playerList = [1, 2, 3, 4, 5, 6, 7, 8]

        """NOMBRE DE JOUEURS DANS LA PARTIE"""
        self.nbPlayers = len(self.playerList)

        """DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE"""
        self.middleNumberPlayers = int(self.nbPlayers/2)
        self.first_halfPlayers = self.playerList[:self.middleNumberPlayers]
        self.second_halfPlayers = self.playerList[self.middleNumberPlayers:]

        """Définition des variables"""
        self.playerMatch = []
        self.totalMatch = []

        # Tri des joueurs
        self.playersToSort = []

        self.match = []

        self.matchToPlay = []

        self.playerOrder = []

    def run(self):

        """Définition des variables"""
        round1 = []
        # round2 = []
        # round3 = []
        # round4 = []

        """ROUND 1"""
        print()
        print("ROUND 1 :")

        for i in range(self.middleNumberPlayers):
            randomScore = [0, 0.5, 1]
            x = randomScore[randint(0, 2)]
            if x == 0:
                y = 1
            elif x == 0.5:
                y = 0.5
            else:
                y = 0
            round1.append(([self.first_halfPlayers[i], x],
                           [self.second_halfPlayers[i], y]))
            self.totalMatch.append(([self.first_halfPlayers[i], x],
                                    [self.second_halfPlayers[i], y]))

        """TRI DES JOUEURS PAR RANG ET PAR POINTS"""
        for i in range(self.middleNumberPlayers):
            self.playersToSort.append(round1[i][0])
            self.playersToSort.append(round1[i][1])

        # Tri des joueurs par rang
        self.playersToSort.sort()

        # Tri des joueurs par rang et par score
        self.playersToSort.sort(key=self.getScore, reverse=True)
        self.playersSorted = self.playersToSort

        print(self.playersSorted)

        """ROUND 2"""
        print()
        print("ROUND 2 :")

        self.getPlayerMatchs()

        print(self.playersSorted)

        """ROUND 3"""
        print()
        print("ROUND 3 :")

        self.getPlayerMatchs()

        print(self.playersSorted)

        """ROUND 4"""
        print()
        print("ROUND 4 :")

        self.getPlayerMatchs()

        print()
        print("Score final :")
        print(self.playersSorted)

    # fonction globale permettant d'assurer les rounds 2 à 4
    def getPlayerMatchs(self):
        self.playerMatch = []
        self.playerOrder = []
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
        # on appelle la fonction permettant de connaître
        # quels match ont été joué par nos joueurs
        self.matchPlayed()

        self.matchToAdd()
        self.sortPlayersByMatch()
        self.playMatch()
        self.sortPlayersByScore(self.match)

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
            print("Match joués par le Joueur " + str(players)
                  + " : " + str(playedMatchs))
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
                         (self.playerOrder[i] in playedMatchs) == False and \
                         ((players in self.matchToPlay) == False and
                          (self.playerOrder[i] in self.matchToPlay) == False):
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

        # génération aléatoire de victoire / égalité / défaite sur les matchs
        for i in range(0, len(self.playerList), 2):
            randomScore = [0, 0.5, 1]
            x = randomScore[randint(0, 2)]
            # si le score de X est 0, le joueur Y gagne 1. (perdu pour X)
            if x == 0:
                x = self.playersSorted[i][1]
                y = self.playersSorted[i+1][1] + 1
            # si le score de X est 0,5, le joueur Y gagne 0,5. (égalité)
            elif x == 0.5:
                y = self.playersSorted[i+1][1] + 0.5
                x = self.playersSorted[i][1] + 0.5
            # si le score de X est 1, le joueur Y gagne 0. (perdu pour Y)
            else:
                x = self.playersSorted[i][1] + 1
                y = self.playersSorted[i+1][1]
            # on ajoute le tuple joueur / score au round actuel
            # puis au total des matchs
            self.match.append(([self.playersSorted[i][0], x],
                               [self.playersSorted[i+1][0], y]))
            self.totalMatch.append(([self.playersSorted[i][0], x],
                                    [self.playersSorted[i+1][0], y]))

    # permet le tri par rang et par score
    def getScore(self, elem):
        return elem[1]

    # on trie les joueurs par rapport à leur score et leur rang
    def sortPlayersByScore(self, match):
        self.playersToSort.clear()
        # on ajoute les tuples à la variable pour pouvoir trier l'ensemble
        for i in range(self.middleNumberPlayers):
            self.playersToSort.append(match[i][0])
            self.playersToSort.append(match[i][1])

        # Tri des joueurs par rang
        self.playersToSort.sort()

        # Tri des joueurs par rang et par score
        self.playersToSort.sort(key=self.getScore, reverse=True)
        self.playersSorted = self.playersToSort


class ManualRoundCreationController:
    """Mode Manuel à mettre en place
    """

    def __init__(self, Load_state, Save_step):
        self.db = TinyDB('db.json')

        # variable de chargement de tournoi
        self.Load_state = Load_state
        self.Save_step = Save_step

        # --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
        self.tournamentTable = self.db.table('tournament_table')
        self.playerPool = self.db.table('player_pool')
        self.playerTable = self.db.table('player_table')

        """CREATION DE LA LISTE DES JOUEURS"""
        self.playerList = []
        self.playerListToSort = []
        self.playerListByRank = []

        """NOMBRE DE JOUEURS DANS LA PARTIE"""
        self.nbPlayers = 0

        """DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE"""
        self.middleNumberPlayers = 0
        self.first_halfPlayers = 0
        self.second_halfPlayers = 0

        """Définition des variables"""
        self.tournament_index = 0
        self.last_index = 0
        self.playerRank = 0
        self.playerMatch = []
        self.totalMatch = []
        self.playersToSort = []
        self.match = []
        self.matchToPlay = []
        self.playerOrder = []

    def run(self):

        """ETAPE 0 DE SAUVEGARDE"""
        print(self.Load_state)
        print(self.Save_step)
        if (self.Load_state == True and self.Save_step == 0) or self.Load_state == False:
            tournamentName = input("Entrez le nom du tournoi : ")
            tournamentLocation = input("Entrez le lieu du tournoi : ")
            tournamentDate = input("Entrez la date du tournoi : ")
            tournamentRound = input("Entrez le nombre de round du tournoi : ")
            #tournamentAllRound = input("Entrez le nom du tournoi : ")
            #tournamentPlayers = input("Entrez le nom des joueurs : ")
            tournamentTime = input("Entrez le temps du tournoi : ")
            tournamentDescription = input("Entrez la description du tournoi : ")
            #tournamentData = {"Name":tournamentName, "Location":tournamentLocation, "Date":tournamentDate, "Round":tournamentRound, "Players":{'Player1':[], 'Player2':{}, 'Player3':{}, 'Player4':{}, 'Player5':{}, 'Player6':{}, 'Player7':{}, 'Player8':{}}, "Time":tournamentTime, "Description":tournamentDescription}
            
            # AJOUTER UNE FONCTION PERMETTANT D'INCREMENTER L'ID

            if len(self.tournamentTable.all()) == 0:
                self.last_index = 0
            else:
                tournamentTable = self.tournamentTable.all()
                sorted_list = sorted(tournamentTable, key=lambda item:item["Tournament_Id"])
                print(list(sorted_list)[-1]["Tournament_Id"])
                self.last_index = list(sorted_list)[-1]["Tournament_Id"] + 1

            tournamentData = {"Tournament_Id":self.last_index ,"Name":tournamentName, "Location":tournamentLocation, "Date":tournamentDate, "Round":tournamentRound, "Time":tournamentTime, "Description":tournamentDescription, "Save_step":1}
            self.tournamentTable.insert(tournamentData)
            self.tournament_index = self.last_index

            """ETAPE 1 DE SAUVEGARDE"""
            print(self.Load_state)
            print(self.Save_step)
        
        if (self.Load_state == True and self.Save_step == 1) or self.Load_state == False:
            
            """DONNEES JOUEURS"""
            # index = self.playerPool.all()[0] pour index?
            i = 0
            # self.playerList
            while len(self.playerListToSort) < 8:
                i += 1
                print("Voulez-vous :")
                print("==============================")
                print("1. Ajouter un joueur déjà éxistant")
                print("2. Créer un nouveau joueur (Manuel)")
                print("3. Créer un nouveau joueur (Automatique)")
                
                wrongChoice = True
                while wrongChoice == True:
                    userChoice = input("Que voulez-vous faire? ")
                    if userChoice == "1":
                        wrongChoice = False
                        self.playerChoice()
                    elif userChoice == "2":
                        wrongChoice = False
                        self.creationPlayer()
                    elif userChoice == "3":
                        wrongChoice = False
                        playerName = "Name" + str(i)
                        playerSurname = "Surname" + str(i)
                        playerBirthdate = "BDate" + str(i)
                        playerGender = "Gender" + str(i)

                        if len(self.playerPool.all()) == 0:
                            self.last_index = 0
                        else:
                            playerPool = self.playerPool.all()
                            sorted_list = sorted(playerPool, key=lambda item:item["Player_Id"])
                            print(list(sorted_list)[-1]["Player_Id"])
                            self.last_index = list(sorted_list)[-1]["Player_Id"] + 1

                        self.playerRank = random.randint(0, 1000)
                        playerData = {"Player_Id": self.last_index, "playerName":playerName, "playerSurname":playerSurname, "playerBirthdate":playerBirthdate, "playerGender":playerGender, "playerRank":self.playerRank}
                        self.playerPool.insert(playerData)
                    else:
                        wrongChoice = True
                        print("Veuillez saisir un entrée valide")

                self.playerListToSort.append([(self.last_index),self.playerRank])
                self.playerList.append(i)
                continue

            playerListSorted = sorted(self.playerListToSort, key=lambda item:item[1], reverse = True)

            i = 0
            for datas in playerListSorted:
                i += 1
                self.playerListByRank.append((i, datas[0],datas[1]))

            self.nbPlayers = len(self.playerList)
            self.middleNumberPlayers = int(self.nbPlayers/2)
            self.first_halfPlayers = self.playerList[:self.middleNumberPlayers]
            self.second_halfPlayers = self.playerList[self.middleNumberPlayers:]

            tournamentData = {"players": self.playerListByRank, "Save_step":2}
            self.tournamentTable.update(tournamentData, Query().Tournament_Id == self.tournament_index)

            """ETAPE 2 DE SAUVEGARDE"""
        if (self.Load_state == True and self.Save_step == 2) or self.Load_state == False:

            """ROUND 1"""
            print()
            print("ROUND 1 :")

            for i in range(self.middleNumberPlayers):
                randomScore = [0, 0.5, 1]
                x = randomScore[randint(0, 2)]
                if x == 0:
                    y = 1
                elif x == 0.5:
                    y = 0.5
                else:
                    y = 0
                self.totalMatch.append(([self.first_halfPlayers[i], x],
                                        [self.second_halfPlayers[i], y]))

            """TRI DES JOUEURS PAR RANG ET PAR POINTS"""
            for i in range(self.middleNumberPlayers):
                self.playersToSort.append(self.totalMatch[i][0])
                self.playersToSort.append(self.totalMatch[i][1])

            # Tri des joueurs par rang
            self.playersToSort.sort()

            # Tri des joueurs par rang et par score
            self.playersToSort.sort(key=self.getScore, reverse=True)
            self.playersSorted = self.playersToSort

            print(self.playersSorted)

            tournamentData = {"matchs": self.totalMatch, "Save_step":3}
            self.tournamentTable.update(tournamentData, Query().Tournament_Id == self.tournament_index)

            """ETAPE 3 DE SAUVEGARDE"""
        if (self.Load_state == True and self.Save_step == 3) or self.Load_state == False:

            """ROUND 2"""
            print()
            print("ROUND 2 :")

            self.getPlayerMatchs()

            print(self.playersSorted)

            tournamentData = {"matchs":self.totalMatch, "Save_step":4}
            self.tournamentTable.update(tournamentData, Query().Tournament_Id == self.tournament_index)



            """ETAPE 4 DE SAUVEGARDE"""
        if (self.Load_state == True and self.Save_step == 4) or self.Load_state == False:

            """ROUND 3"""
            print()
            print("ROUND 3 :")

            self.getPlayerMatchs()

            print(self.playersSorted)

            tournamentData = {"matchs":self.totalMatch, "Save_step":5}
            self.tournamentTable.update(tournamentData, Query().Tournament_Id == self.tournament_index)

            """ETAPE 5 DE SAUVEGARDE"""
        if (self.Load_state == True and self.Save_step == 5) or self.Load_state == False:

            """ROUND 4"""
            print()
            print("ROUND 4 :")

            self.getPlayerMatchs()

            print(self.playersSorted)

            tournamentData = {"matchs":self.totalMatch, "Save_step":6}
            self.tournamentTable.update(tournamentData, Query().Tournament_Id == self.tournament_index)

    # séléction des joueurs
    def playerChoice(self):
        for datas in self.playerPool.all():
            print("ID :" + str(datas.get('Player_Id')) + " , Joueur : " + str(datas.get('playerName')))
        playerChoice = input("Séléctionnez l'ID du joueur :")
        playerId = self.playerPool.search(where("Player_Id") == int(playerChoice))[0]
        self.playerRank = playerId["playerRank"]
        self.last_index = playerId["Player_Id"]

    # création des joueurs
    def creationPlayer(self):
        playerName = input("Entrez le nom du joueur : ")
        playerSurname = input("Entrez le prénom du joueur : ")
        playerBirthdate = input("Entrez la date de naissance du joueur : ")
        playerGender = input("Entrez le genre du joueur : ")
        self.playerRank = int(input("Entrez le rang du joueur : "))

        if len(self.playerPool.all()) == 0:
            self.last_index = 0
        else:
            playerPool = self.playerPool.all()
            sorted_list = sorted(playerPool, key=lambda item:item["Player_Id"])
            print(list(sorted_list)[-1]["Player_Id"])
            self.last_index = list(sorted_list)[-1]["Player_Id"] + 1

        playerData = {"Player_Id":self.last_index, "playerName":playerName, "playerSurname":playerSurname, "playerBirthdate":playerBirthdate, "playerGender":playerGender, "playerRank":self.playerRank}

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
        # on appelle la fonction permettant de connaître
        # quels match ont été joué par nos joueurs
        self.matchPlayed()

        self.matchToAdd()
        self.sortPlayersByMatch()
        self.playMatch()
        self.sortPlayersByScore(self.match)

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
                         (self.playerOrder[i] in playedMatchs) == False and \
                         ((players in self.matchToPlay) == False and
                          (self.playerOrder[i] in self.matchToPlay) == False):
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

        # génération aléatoire de victoire / égalité / défaite sur les matchs
        for i in range(0, len(self.playerList), 2):
            randomScore = [0, 0.5, 1]
            x = randomScore[randint(0, 2)]
            # si le score de X est 0, le joueur Y gagne 1. (perdu pour X)
            if x == 0:
                x = self.playersSorted[i][1]
                y = self.playersSorted[i+1][1] + 1
            # si le score de X est 0,5, le joueur Y gagne 0,5. (égalité)
            elif x == 0.5:
                y = self.playersSorted[i+1][1] + 0.5
                x = self.playersSorted[i][1] + 0.5
            # si le score de X est 1, le joueur Y gagne 0. (perdu pour Y)
            else:
                x = self.playersSorted[i][1] + 1
                y = self.playersSorted[i+1][1]
            # on ajoute le tuple joueur / score au round actuel
            # puis au total des matchs
            self.match.append(([self.playersSorted[i][0], x],
                               [self.playersSorted[i+1][0], y]))
            self.totalMatch.append(([self.playersSorted[i][0], x],
                                    [self.playersSorted[i+1][0], y]))

    # permet le tri par rang et par score
    def getScore(self, elem):
        return elem[1]

    # on trie les joueurs par rapport à leur score et leur rang
    def sortPlayersByScore(self, match):
        self.playersToSort.clear()
        # on ajoute les tuples à la variable pour pouvoir trier l'ensemble
        for i in range(self.middleNumberPlayers):
            self.playersToSort.append(match[i][0])
            self.playersToSort.append(match[i][1])

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
        if next_action == "1":
            return PlayerCreationController()
        elif next_action == "2":
            return HomeController()
        elif next_action == "3":
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
        playerName = input("Entrez le nom du joueur : ")
        playerSurname = input("Entrez le prénom du joueur : ")
        playerBirthdate = input("Entrez la date de naissance du joueur : ")
        playerGender = input("Entrez le genre du joueur : ")
        playerRank = input("Entrez le rang du joueur : ")

        if len(self.playerPool.all()) == 0:
            last_index = 0
        else:
            playerPool = self.playerPool.all()
            sorted_list = sorted(playerPool, key=lambda item:item["Player_Id"])
            print(list(sorted_list)[-1]["Player_Id"])
            last_index = list(sorted_list)[-1]["Player_Id"] + 1

        playerData = {"Player_Id": last_index, "playerName":playerName, "playerSurname":playerSurname, "playerBirthdate":playerBirthdate, "playerGender":playerGender, "playerRank":int(playerRank)}

        self.playerPool.insert(playerData)

        for datas in self.playerPool.all():
            print(datas)


class ReportMenuController:
    """Contrôleur responsable de gérer le menu de rapports.
    """

    def __init__(self):
        self.view = views.ReportMenuView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return ReportAllPlayerController()
        elif next_action == "2":
            return ReportTournamentController()
        elif next_action == "3":
            return HomeController()
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
        self.creationReport()
        return ReportMenuController()

    def creationReport(self):
        print("Voulez-vous :")
        print("==============================")
        print("1. Trier l'ensemble par ordre Alphabétique")
        print("2. Trier l'ensemble par Rang")
        print("3. Retourner au menu")
        
        wrongChoice = True
        while wrongChoice == True:
            userChoice = input("Que voulez-vous faire? ")
            if userChoice == "1":
                wrongChoice = False
                self.player_SortName()
            elif userChoice == "2":
                wrongChoice = False
                self.player_SortRank()
            elif userChoice == "3":
                wrongChoice = False
                return EndController()
            else:
                wrongChoice = True
                print("Veuillez saisir un entrée valide")
            continue

    def player_SortName(self):
        playerPool = self.playerPool.all()
        sorted_list = sorted(playerPool, key=lambda item:item["playerName"])
        for datas in sorted_list:
            print("ID : " +  str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"]) + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                  + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"]) + ", Classement : "
                  + str(datas["playerRank"]))

    def player_SortRank(self):
        playerPool = self.playerPool.all()
        sorted_list = sorted(playerPool, key=lambda item:item["playerRank"])
        for datas in sorted_list:
            print("ID : " +  str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"]) + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                  + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"]) + ", Classement : "
                  + str(datas["playerRank"]))


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

        for datas in self.tournamentTable.all():
            print("ID : " +  str(datas["Tournament_Id"]) + ", Nom : " + str(datas["Name"]) + ", Lieu : " + str(datas["Location"]) + ", Date : "
                  + str(datas["Date"]) + ", Nombre de rounds : " + str(datas["Round"]) + ", Type de temps : "
                  + str(datas["Time"]) + ", Description : " + str(datas["Description"]))

        print("Voulez-vous :")
        print("==============================")
        print("1. Voir les tours d'un tournoi spécifique")
        print("2. Voir les matchs d'un tournoi spécifique")
        print("3. Voir les joueurs d'un tournoi spécifique")
        print("4. Retourner au menu")
        
        wrongChoice = True
        while wrongChoice == True:
            userChoice = input("Que voulez-vous faire? ")
            if userChoice == "1":
                wrongChoice = False
                tournamentChoice = int(input("Séléctionnez le tournoi (ID):"))
                user_Choice = self.tournamentTable.search(where("Tournament_Id") == tournamentChoice)
                print("")
                print("ID : " +  str(user_Choice[0]["Tournament_Id"]) + ", Nom : " + str(user_Choice[0]["Name"]) + ", Lieu : " + str(user_Choice[0]["Location"]) + ", Date : "
                    + str(user_Choice[0]["Date"]) + ", Nombre de rounds : " + str(user_Choice[0]["Round"]) + ", Type de temps : "
                    + str(user_Choice[0]["Time"]) + ", Description : " + str(user_Choice[0]["Description"]))
                if user_Choice[0]["Save_step"] >= 3: 
                    print("Joueurs : " + str(user_Choice[0]["players"]))
                    print("")
                    print("Matchs joués :")
                    print("Round 1 :")
                    print(str(user_Choice[0]["matchs"][:4]))
                if user_Choice[0]["Save_step"] >= 4: 
                    print("Round 2 :")
                    print(str(user_Choice[0]["matchs"][4:8]))
                if user_Choice[0]["Save_step"] >= 5: 
                    print("Round 3 :")
                    print(str(user_Choice[0]["matchs"][8:-4]))
                if user_Choice[0]["Save_step"] >= 6: 
                    print("Round 4 :")
                    print(str(user_Choice[0]["matchs"][-4:]))
                print("")
                
            elif userChoice == "2":
                wrongChoice = False
                tournamentChoice = int(input("Séléctionnez le tournoi (ID) :"))
                user_Choice = self.tournamentTable.search(where("Tournament_Id") == tournamentChoice)
                print("")
                print("ID : " +  str(user_Choice[0]["Tournament_Id"]) + ", Nom : " + str(user_Choice[0]["Name"]) + ", Lieu : " + str(user_Choice[0]["Location"]) + ", Date : "
                    + str(user_Choice[0]["Date"]) + ", Nombre de rounds : " + str(user_Choice[0]["Round"]) + ", Type de temps : "
                    + str(user_Choice[0]["Time"]) + ", Description : " + str(user_Choice[0]["Description"]))
                print("Joueurs : " + str(user_Choice[0]["players"]))
                print("")
                print("Matchs joués :")
                print(str(user_Choice[0]["matchs"]))

            elif userChoice == "3":
                wrongChoice = False
                tournamentChoice = int(input("Séléctionnez le tournoi (ID) :"))
                user_Choice = self.tournamentTable.search(where("Tournament_Id") == tournamentChoice)
                for datas in user_Choice[0]["players"]:
                    self.playerInTournament.append(self.playerPool.search(where("Player_Id") == datas[1])[0])

                print("Voulez-vous :")
                print("==============================")
                print("1. Trier l'ensemble par ordre Alphabétique")
                print("2. Trier l'ensemble par Rang")

                wrongChoice = True
                while wrongChoice == True:
                    userChoice = input("Que voulez-vous faire? ")
                    if userChoice == "1":
                        wrongChoice = False
                        sorted_list = sorted(self.playerInTournament, key=lambda item:item["playerName"])
                        for datas in sorted_list:
                            print("ID : " +  str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"]) + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                                + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"]) + ", Classement : "
                                + str(datas["playerRank"]))
                    elif userChoice == "2":
                        wrongChoice = False
                        sorted_list = sorted(self.playerInTournament, key=lambda item:item["playerRank"])
                        for datas in sorted_list:
                            print("ID : " +  str(datas["Player_Id"]) + ", Nom : " + str(datas["playerName"]) + ", Prénom : " + str(datas["playerSurname"]) + ", Date de naissance : "
                                + str(datas["playerBirthdate"]) + ", Genre : " + str(datas["playerGender"]) + ", Classement : "
                                + str(datas["playerRank"]))
                    else:
                        wrongChoice = True
                        print("Veuillez saisir un entrée valide")
                    continue

            elif userChoice == "4":
                wrongChoice = False
                return EndController()
            else:
                wrongChoice = True
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
