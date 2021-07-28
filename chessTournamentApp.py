#from lib import Operation
#from lib.operation import Operation (sans __init__.py)
from lib import Tournament
from tinydb import TinyDB, Query, where
from random import randint, random
import random
import operator

db = TinyDB('db.json')

"""FONCTION ROUND"""
def getPlayerMatchs(totalMatch, playerMatch, playersSorted):
    playerMatch = []
    playerOrder = []
    for matchs in totalMatch:
        playerMatch.append(matchs)
    for player in playersSorted:
        playerOrder.append(player[0])
    matchPlayed(playerOrder, totalMatch)
    matchToAdd(matchToPlay, playerList, playerOrder, totalMatch)
    sortPlayersByMatch(matchToPlay, playersSorted)
    playMatch(sortPlayersByMatch.result)
    sortPlayersByScore(playMatch.results)

def matchPlayed(playerOrder, totalMatch):
    matchToPlay.clear()
    for players in playerOrder:
        playedMatchs = []
        for plays in totalMatch:
            player1 = plays[0][0]
            player2 = plays[1][0]
            if player1 == players:
                playedMatchs.append(player2)
            elif player2 == players:
                playedMatchs.append(player1)
        print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))
        sortMatch(playedMatchs, players, playerOrder)
    pass

def sortMatch(playedMatchs, players, playerOrder):
    for i in range(len(playerOrder)):
        if players != playerOrder[i] and (playerOrder[i] in playedMatchs) == False and ((players in matchToPlay) == False and (playerOrder[i] in matchToPlay) == False):
            matchToPlay.append(players)
            matchToPlay.append(playerOrder[i])
            break

def matchToAdd(matchToPlay, playerList, playerOrder, totalMatch):
    i = 3
    while len(matchToPlay) < len(playerList) and i <= len(playerList):
        i += 1
        print()
        print("Shuffle")
        newPlayerOrder = playerOrder[-i:]
        random.shuffle(newPlayerOrder)
        playerOrder = playerOrder[:4]
        for players in newPlayerOrder:
            playerOrder.append(players)
        matchPlayed(playerOrder, totalMatch)
        if len(matchToPlay) < len(playerList):
            continue

def sortPlayersByMatch(matchToPlay, playersSorted):
    for players in matchToPlay:
        for i in range(len(playerList)):
            if players == playersSorted[i][0]:
                playersSorted.append(playersSorted[i])
                del playersSorted[i]
    sortPlayersByMatch.result = playersSorted

def playMatch(playersSorted):
    match = []

    for i in range(0, len(playerList),2):
        randomScore = [0, 0.5, 1]
        x = randomScore[randint(0, 2)]
        if x == 0:
            x = playersSorted[i][1]
            y = playersSorted[i+1][1] + 1
        elif x == 0.5:
            y = playersSorted[i+1][1] + 0.5
            x = playersSorted[i][1] + 0.5
        else:
            x = playersSorted[i][1] + 1
            y = playersSorted[i+1][1]
        match.append(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
        totalMatch.append(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
    playMatch.results = match

def getScore(elem):
    return elem[1]

def sortPlayersByScore(match):
    #Tri des joueurs
    playersToSort.clear()
    for i in range(middleNumberPlayers):
        playersToSort.append(match[i][0])
        playersToSort.append(match[i][1])

    #Tri des joueurs par rang
    playersToSort.sort()

    #Tri des joueurs par rang et par score
    playersToSort.sort(key=getScore, reverse=True)
    playersSorted = playersToSort


# --- CHOIX EN DEBUT DE PROGRAMME --- #
menuChoice = input("1 = Tournoi; 2 = Joueurs; 3 = Match ; 4 = Création complète : ")
#print(menuChoice)

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
    #Prise du score
    def getScore(elem):
        return elem[1]

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

    print(playersSorted)
