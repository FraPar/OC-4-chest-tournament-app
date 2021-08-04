import views

from tinydb import TinyDB, Query, where
from random import randint, random
import random
import operator


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
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            #mettre la version création automatique de tournoi
            return AutomaticTournamentCreationController()
        elif next_action == "2":
            return TournamentCreationController()
        elif next_action == "3":
            return PlayerCreationController()
        elif next_action == "4":
            #mettre la reprise de tournoi en cours (pas encore mise en place)
            pass
        elif next_action == "5":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return HomeController()


class AutomaticTournamentCreationController:
    """Contrôleur responsable de gérer le menu de création d'un tournoi automatique.
    """

    def __init__(self):
        self.view = views.AutomaticTournamentCreationView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return RoundCreationController()
        elif next_action == "2":
            return HomeController()
        elif next_action == "3":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return AutomaticTournamentCreationController()


class TournamentCreationController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    tournoi.
    """

    def __init__(self):
        self.view = views.TournamentCreationView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return HomeController()
        elif next_action == "2":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return TournamentCreationController()

class RoundCreationController:
    """Mettre mes fonctions du main.py
    """

    def __init__(self):
        self.db= TinyDB('db.json')

        #mettre les variables avec .self et les fonctions en self.

        """CREATION DE LA LISTE DES JOUEURS"""
        self.playerList = [1, 2, 3, 4, 5, 6, 7, 8]

        """NOMBRE DE JOUEURS DANS LA PARTIE"""
        self.nbPlayers = len(self.playerList)

        """DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE"""
        self.middleNumberPlayers = int(self.nbPlayers/2)
        #first_halfPlayers = self.playerList[:middleNumberPlayers]
        #second_halfPlayers = self.playerList[middleNumberPlayers:]

        """Définition des variables"""
        #self.playerMatch = []
        self.totalMatch = []

        #Tri des joueurs
        self.playersToSort = []

        self.match = []  

        self.matchToPlay = []

    def run(self):



        """NOMBRE DE JOUEURS DANS LA PARTIE"""
        #nbPlayers = len(self.playerList)

        """DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE"""
        #middleNumberPlayers = int(nbPlayers/2)
        first_halfPlayers = self.playerList[:self.middleNumberPlayers]
        second_halfPlayers = self.playerList[self.middleNumberPlayers:]

        """Définition des variables"""
        playerMatch = []
        #totalMatch = []
        round1 = []
        round2 = []
        round3 = []
        round4 = []

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
            round1.append(([first_halfPlayers[i], x], [second_halfPlayers[i], y]))
            self.totalMatch.append(([first_halfPlayers[i], x], [second_halfPlayers[i], y]))

        """TRI DES JOUEURS PAR RANG ET PAR POINTS"""
        for i in range(self.middleNumberPlayers):
            self.playersToSort.append(round1[i][0])
            self.playersToSort.append(round1[i][1])

        #Tri des joueurs par rang
        self.playersToSort.sort()

        #Tri des joueurs par rang et par score
        self.playersToSort.sort(key=self.getScore, reverse=True)
        self.playersSorted = self.playersToSort

        playersToMatch = []
        listOfPlayers = []


        print(self.playersSorted)

        """ROUND 2"""
        print()
        print("ROUND 2 :")

        self.getPlayerMatchs(self.totalMatch, playerMatch, self.playersSorted)

        print(self.playersSorted)

        """ROUND 3"""
        print()
        print("ROUND 3 :")

        self.getPlayerMatchs(self.totalMatch, playerMatch, self.playersSorted)

        print(self.playersSorted)

        """ROUND 4"""
        print()
        print("ROUND 4 :")

        self.getPlayerMatchs(self.totalMatch, playerMatch, self.playersSorted)

        print()
        print("Score final :")
        print(self.playersSorted)

    #fonction globale permettant d'assurer les rounds 2 à 4
    def getPlayerMatchs(self, totalMatch, playerMatch, playersSorted):
        playerMatch = []
        playerOrder = []
        #on prépare les données de joueurs pour mettre en place les paires du round
        #on insert l'ensemble des matchs dans une liste pour ne pas avoir de matchs doublons
        for matchs in totalMatch:
            playerMatch.append(matchs)
        #on insert les joueurs par rapport à leur score et leur rang dans une variable
        for player in self.playersSorted:
            playerOrder.append(player[0])
        #on appelle la fonction permettant de connaître quels match ont été joué par nos joueurs
        self.matchPlayed(playerOrder, totalMatch)

        self.matchToAdd(playerOrder, totalMatch)
        self.sortPlayersByMatch()
        self.playMatch()
        self.sortPlayersByScore(self.match)

    #fonction permettant de connaître les matchs joués par notre joueur
    def matchPlayed(self, playerOrder, totalMatch):
        self.matchToPlay.clear()
        #on boucle sur les joueurs du tournoi, du 1er au dernier
        for players in playerOrder:
            playedMatchs = []
            #on boucle sur les matchs déjà joué lors du tournoi
            for plays in totalMatch:
                player1 = plays[0][0]
                player2 = plays[1][0]
                #on teste si le joueur 1 est le joueur sur lequel on boucle pour connaître son adversaire
                if player1 == players:
                    playedMatchs.append(player2)
                #on teste si le joueur 2 est le joueur sur lequel on boucle pour connaître son adversaire
                elif player2 == players:
                    playedMatchs.append(player1)
            print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))
            #on appelle la fonction permettant de mettre un adversaire face à un autre
            self.sortMatch(playedMatchs, players, playerOrder)
        pass

    #fonction permettant de mettre un joueur face à un autre sans doublon de match
    def sortMatch(self, playedMatchs, players, playerOrder):
        for i in range(len(playerOrder)):
            #on teste si le joueur n'a pas déjà été aloué a un autre match dans ce round, s'il n'a pas déjà été joué ou si on ne met pas un joueur face à lui même
            if players != playerOrder[i] and (playerOrder[i] in playedMatchs) == False and ((players in self.matchToPlay) == False and (playerOrder[i] in self.matchToPlay) == False):
                self.matchToPlay.append(players)
                self.matchToPlay.append(playerOrder[i])
                break

    #fonction permettant de gérer le cas particulier des 2 derniers joueurs ayant déjà joué ensemble
    def matchToAdd(self, playerOrder, totalMatch):
        #on met i à 3 pour garder les 4 derniers joueurs dans notre piscine de joueurs à mettre en face
        i = 3
        #on teste si tous les matchs ont été alloué ou non.
        while len(self.matchToPlay) < len(self.playerList) and i <= len(self.playerList):
            i += 1
            print()
            print("Shuffle")
            #on récupère les 4+ derniers joueurs pour trouver un match à jouer
            newPlayerOrder = playerOrder[-i:]
            #on mélange les joueurs pour trouver un match à jouer
            random.shuffle(newPlayerOrder)
            playerOrder = playerOrder[:4]
            #on ajoute les joueurs ayant été mis face à face pour tester s'ils ont déjà joués ensemble
            for players in newPlayerOrder:
                playerOrder.append(players)
            #on appelle la fonction permettant de connaître quels match ont été joué par nos joueurs
            self.matchPlayed(playerOrder, totalMatch)
            #si le nombre de joueurs présents dans le tournoi n'est pas équivalent à celui de joueurs a qui on a trouvé un match, on continue la boucle
            if len(self.matchToPlay) < len(self.playerList):
                continue

    #on associe les différents joueurs entre eux après le filtrage évitant les doublons
    def sortPlayersByMatch(self):
        #on boucle sur l'ensemble des joueurs à coupler dans un match
        for players in self.matchToPlay:
            #on boucle sur l'ensemble des joueurs présent dans le tri effectué
            for i in range(len(self.playerList)):
                #on récupère les joueurs et leurs scores dans l'ordre
                if players == self.playersSorted[i][0]:
                    self.playersSorted.append(self.playersSorted[i])
                    #on supprime les joueurs déjà trouvés
                    del self.playersSorted[i]

    #on joue les matchs crées auparavant
    def playMatch(self):
        self.match.clear()

        #génération aléatoire de la victoire / égalité / défaite sur les matchs
        for i in range(0, len(self.playerList),2):
            randomScore = [0, 0.5, 1]
            x = randomScore[randint(0, 2)]
            #si le score de X est 0, le joueur Y gagne 1. (perdu pour X)
            if x == 0:
                x = self.playersSorted[i][1]
                y = self.playersSorted[i+1][1] + 1
            #si le score de X est 0,5, le joueur Y gagne 0,5. (égalité)
            elif x == 0.5:
                y = self.playersSorted[i+1][1] + 0.5
                x = self.playersSorted[i][1] + 0.5
            #si le score de X est 1, le joueur Y gagne 0. (perdu pour Y)
            else:
                x = self.playersSorted[i][1] + 1
                y = self.playersSorted[i+1][1]
            #on ajoute le tuple joueur / score au round actuel puis au total des matchs
            self.match.append(([self.playersSorted[i][0], x], [self.playersSorted[i+1][0], y]))
            self.totalMatch.append(([self.playersSorted[i][0], x], [self.playersSorted[i+1][0], y]))

    #permet le tri par rang et par score
    def getScore(self, elem):
        return elem[1]

    #on trie les joueurs par rapport à leur score et leur rang
    def sortPlayersByScore(self, match):
        self.playersToSort.clear()
        #on ajoute les tuples à la variable pour pouvoir trier l'ensemble
        for i in range(self.middleNumberPlayers):
            self.playersToSort.append(match[i][0])
            self.playersToSort.append(match[i][1])

        #Tri des joueurs par rang
        self.playersToSort.sort()

        #Tri des joueurs par rang et par score
        self.playersToSort.sort(key=self.getScore, reverse=True)
        self.playersSorted = self.playersToSort



class PlayerCreationController:
    """Contrôleur responsable de gérer le menu de création d'un nouveau
    joueur.
    """

    def __init__(self):
        self.view = views.PlayerCreationView()

    def run(self):
        self.view.render()
        next_action = self.view.get_user_choice()
        if next_action == "1":
            return HomeController()
        elif next_action == "2":
            return EndController()
        else:
            self.view.notify_invalid_choice()
            return PlayerCreationController()


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