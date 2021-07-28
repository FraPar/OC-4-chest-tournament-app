#from lib import Operation
#from lib.operation import Operation (sans __init__.py)
from lib import Tournament
from tinydb import TinyDB, Query, where
from random import randint, random
import random
import operator

db = TinyDB('db.json')

"""FONCTION ROUND"""
#fonction globale permettant d'assurer les rounds 2 à 4
def getPlayerMatchs(totalMatch, playerMatch, playersSorted):
    playerMatch = []
    playerOrder = []
    #on prépare les données de joueurs pour mettre en place les paires du round
    #on insert l'ensemble des matchs dans une liste pour ne pas avoir de matchs doublons
    for matchs in totalMatch:
        playerMatch.append(matchs)
    #on insert les joueurs par rapport à leur score et leur rang dans une variable
    for player in playersSorted:
        playerOrder.append(player[0])
    #on appelle la fonction permettant de connaître quels match ont été joué par nos joueurs
    matchPlayed(playerOrder, totalMatch)

    matchToAdd(matchToPlay, playerList, playerOrder, totalMatch)
    sortPlayersByMatch(matchToPlay, playersSorted)
    playMatch(sortPlayersByMatch.result)
    sortPlayersByScore(playMatch.results)

#fonction permettant de connaître les matchs joués par notre joueur
def matchPlayed(playerOrder, totalMatch):
    matchToPlay.clear()
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
        sortMatch(playedMatchs, players, playerOrder)
    pass

#fonction permettant de mettre un joueur face à un autre sans doublon de match
def sortMatch(playedMatchs, players, playerOrder):
    for i in range(len(playerOrder)):
        #on teste si le joueur n'a pas déjà été aloué a un autre match dans ce round, s'il n'a pas déjà été joué ou si on ne met pas un joueur face à lui même
        if players != playerOrder[i] and (playerOrder[i] in playedMatchs) == False and ((players in matchToPlay) == False and (playerOrder[i] in matchToPlay) == False):
            matchToPlay.append(players)
            matchToPlay.append(playerOrder[i])
            break

#fonction permettant de gérer le cas particulier des 2 derniers joueurs ayant déjà joué ensemble
def matchToAdd(matchToPlay, playerList, playerOrder, totalMatch):
    #on met i à 3 pour garder les 4 derniers joueurs dans notre piscine de joueurs à mettre en face
    i = 3
    #on teste si tous les matchs ont été alloué ou non.
    while len(matchToPlay) < len(playerList) and i <= len(playerList):
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
        matchPlayed(playerOrder, totalMatch)
        #si le nombre de joueurs présents dans le tournoi n'est pas équivalent à celui de joueurs a qui on a trouvé un match, on continue la boucle
        if len(matchToPlay) < len(playerList):
            continue

#on associe les différents joueurs entre eux après le filtrage évitant les doublons
def sortPlayersByMatch(matchToPlay, playersSorted):
    #on boucle sur l'ensemble des joueurs à coupler dans un match
    for players in matchToPlay:
        #on boucle sur l'ensemble des joueurs présent dans le tri effectué
        for i in range(len(playerList)):
            #on récupère les joueurs et leurs scores dans l'ordre
            if players == playersSorted[i][0]:
                playersSorted.append(playersSorted[i])
                #on supprime les joueurs déjà trouvés
                del playersSorted[i]
    sortPlayersByMatch.result = playersSorted

#on joue les matchs crées auparavant
def playMatch(playersSorted):
    match = []

    #génération aléatoire de la victoire / égalité / défaite sur les matchs
    for i in range(0, len(playerList),2):
        randomScore = [0, 0.5, 1]
        x = randomScore[randint(0, 2)]
        #si le score de X est 0, le joueur Y gagne 1. (perdu pour X)
        if x == 0:
            x = playersSorted[i][1]
            y = playersSorted[i+1][1] + 1
        #si le score de X est 0,5, le joueur Y gagne 0,5. (égalité)
        elif x == 0.5:
            y = playersSorted[i+1][1] + 0.5
            x = playersSorted[i][1] + 0.5
        #si le score de X est 1, le joueur Y gagne 0. (perdu pour Y)
        else:
            x = playersSorted[i][1] + 1
            y = playersSorted[i+1][1]
        #on ajoute le tuple joueur / score au round actuel puis au total des matchs
        match.append(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
        totalMatch.append(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
    playMatch.results = match

#permet le tri par rang et par score
def getScore(elem):
    return elem[1]

#on trie les joueurs par rapport à leur score et leur rang
def sortPlayersByScore(match):
    playersToSort.clear()
    #on ajoute les tuples à la variable pour pouvoir trier l'ensemble
    for i in range(middleNumberPlayers):
        playersToSort.append(match[i][0])
        playersToSort.append(match[i][1])

    #Tri des joueurs par rang
    playersToSort.sort()

    #Tri des joueurs par rang et par score
    playersToSort.sort(key=getScore, reverse=True)
    playersSorted = playersToSort


"""DEBUT DU SCRIPT"""

# --- CHOIX EN DEBUT DE PROGRAMME --- #
menuChoice = input("1 = Tournoi; 2 = Joueurs; 3 = Match ; 4 = Création automatique tournoi : ")

# --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
tournamentTable = db.table('tournament_table')
playerTable = db.table('player_table')
roundTable = db.table('round_table')

# --- CHOIX DE LA PARTIE TOURNOI --- #
if menuChoice == "4":
    """CREATION DE LA LISTE DES JOUEURS"""
    playerList = [1, 2, 3, 4, 5, 6, 7, 8]

    """NOMBRE DE JOUEURS DANS LA PARTIE"""
    nbPlayers = len(playerList)

    """DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE"""
    middleNumberPlayers = int(nbPlayers/2)
    first_halfPlayers = playerList[:middleNumberPlayers]
    second_halfPlayers = playerList[middleNumberPlayers:]

    """Définition des variables"""
    playerMatch = []
    totalMatch = []
    round1 = []
    round2 = []
    round3 = []
    round4 = []

    """ROUND 1"""
    print()
    print("ROUND 1 :")

    for i in range(middleNumberPlayers):
        randomScore = [0, 0.5, 1]
        x = randomScore[randint(0, 2)]
        if x == 0:
            y = 1
        elif x == 0.5:
            y = 0.5
        else:
            y = 0
        round1.append(([first_halfPlayers[i], x], [second_halfPlayers[i], y]))
        totalMatch.append(([first_halfPlayers[i], x], [second_halfPlayers[i], y]))

    """TRI DES JOUEURS PAR RANG ET PAR POINTS"""
    #Tri des joueurs
    playersToSort = []
    for i in range(middleNumberPlayers):
        playersToSort.append(round1[i][0])
        playersToSort.append(round1[i][1])

    #Tri des joueurs par rang
    playersToSort.sort()

    #Tri des joueurs par rang et par score
    playersToSort.sort(key=getScore, reverse=True)
    playersSorted = playersToSort
    print("playersSorted ROUND 1")
    print(playersSorted)

    playersToMatch = []
    listOfPlayers = []
    matchToPlay = []

    print(playersSorted)

    """ROUND 2"""
    print()
    print("ROUND 2 :")

    getPlayerMatchs(totalMatch, playerMatch, playersSorted)

    print(playersSorted)

    """ROUND 3"""
    print()
    print("ROUND 3 :")

    getPlayerMatchs(totalMatch, playerMatch, playersSorted)

    print(playersSorted)

    """ROUND 4"""
    print()
    print("ROUND 4 :")

    getPlayerMatchs(totalMatch, playerMatch, playersSorted)

    print()
    print("Score final :")
    print(playersSorted)
