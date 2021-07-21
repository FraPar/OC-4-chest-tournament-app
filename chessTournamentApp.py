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
    #print("Get player Matchs")
    playerMatch = []
    playerOrder = []
    for matchs in totalMatch:
        playerMatch.append(matchs)
    #print("playersSorted in getPlayerMatchs")
    #print(playersSorted)
    for player in playersSorted:
        playerOrder.append(player[0])
    #print("playerMatch")
    #print(playerMatch)
    #print("playerOrder")
    #print(playerOrder)
    #print("match")
    #print(match)
    matchPlayed(playerOrder, totalMatch)
    matchToAdd(matchToPlay, playerList, playerOrder, totalMatch)
    #print("matchToPlay")
    #print(matchToPlay)
    #print("playersSorted in getPlayerMatchs")
    #print(playersSorted)
    sortPlayersByMatch(matchToPlay, playersSorted)
    playMatch(sortPlayersByMatch.result)
    #print("match IN GENERAL FUNCTION ()")
    #print(playMatch.results)
    sortPlayersByScore(playMatch.results)

def matchPlayed(playerOrder, totalMatch):
    matchToPlay.clear()
    for players in playerOrder:
        playedMatchs = []
        for plays in totalMatch:
            player1 = plays[0][0]
            player2 = plays[1][0]
            if player1 == players:
                #print(player2)
                playedMatchs.append(player2)
            elif player2 == players:
                #print(player1)
                playedMatchs.append(player1)
        #print()
        print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))
        sortMatch(playedMatchs, players, playerOrder)
    pass

def sortMatch(playedMatchs, players, playerOrder):
    #print("Chosing one player")
    #print("playedMatchs")
    #print(playedMatchs)
    #print()
    #print("IN SORTMATCH()")
    #print("players")
    #print(players)
    for i in range(len(playerOrder)):
        #print("playerOrder[i]")
        #print(playerOrder[i])
        if players != playerOrder[i] and (playerOrder[i] in playedMatchs) == False and ((players in matchToPlay) == False and (playerOrder[i] in matchToPlay) == False):
            #print("OK : playerOrder[i]")
            #print(playerOrder[i])
            matchToPlay.append(players)
            matchToPlay.append(playerOrder[i])
            break

    #print(matchToPlay)

def matchToAdd(matchToPlay, playerList, playerOrder, totalMatch):
    i = 3
    while len(matchToPlay) < len(playerList) and i <= len(playerList):
        i += 1
        print()
        print("Shuffle")
        #print("Ups, we need one more match to find!")
        #print("len(matchToPlay) < len(playerList)")
        #print(matchToPlay)
        #print("print(playerOrder[:-4])")
        newPlayerOrder = playerOrder[-i:]
        random.shuffle(newPlayerOrder)
        #print("random.shuffle(newPlayerOrder)")
        #print(newPlayerOrder)
        playerOrder = playerOrder[:4]
        for players in newPlayerOrder:
            playerOrder.append(players)
        #print("playerOrder")
        #print(playerOrder)
        matchPlayed(playerOrder, totalMatch)
        if len(matchToPlay) < len(playerList):
            continue
        #print("ON EST PASSE PAR MATCHTOADD!!!!!!!!!!!")
    """elif len(matchToPlay) == len(playerList):
        print("It's ok, you can pass")
        print("len(matchToPlay) == len(playerList)")
        print(matchToPlay)"""

def sortPlayersByMatch(matchToPlay, playersSorted):
    #print("matchToPlay")
    #print(matchToPlay)
    for players in matchToPlay:
        #print("players in matchToPlay / playerOrder")
        #print(players)
        for i in range(len(playerList)):
            #print("players")
            #print(players)
            if players == playersSorted[i][0]:
                #print("players in playerOrder")
                playersSorted.append(playersSorted[i])
                del playersSorted[i]
                #print(playersSorted)
    #print("playersSorted")
    #print(len(playersSorted))
    #print(playersSorted)
    sortPlayersByMatch.result = playersSorted

def playMatch(playersSorted):
    #print("playersSorted IN PLAYMATCH()")
    #print(playersSorted)
    match = []
    #print("match in playMatch")
    #print(match)
    #print(playersSorted[0][0])
    #print(playersSorted[1][0])
    for i in range(0, len(playerList),2):
        #print(i)
        #print(int(i+ 1))
        #print(playersSorted[i][0])
        #print(playersSorted[i+1][0])
        #print(playersSorted)
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
        #print(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
        match.append(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
        totalMatch.append(([playersSorted[i][0], x], [playersSorted[i+1][0], y]))
    #print("match in playMatch")
    #print(match)
    playMatch.results = match
    #sortPlayersByScore(match)

def getScore(elem):
    return elem[1]

def sortPlayersByScore(match):
    #Tri des joueurs
    #print("match in sortPlayersByScore")
    #print(match)
    playersToSort.clear()
    for i in range(middleNumberPlayers):
        playersToSort.append(match[i][0])
        playersToSort.append(match[i][1])
    #print(playersToSort)

    #Tri des joueurs par rang
    playersToSort.sort()
    #print(playersToSort)

    #Tri des joueurs par rang et par score
    playersToSort.sort(key=getScore, reverse=True)
    playersSorted = playersToSort
    #print("playersSorted : match sorted in sortPlayersByScore")
    #print(playersSorted)

"""CREATION DE LA LISTE DES JOUEURS"""
playerList = [1, 2, 3, 4, 5, 6, 7, 8]
#print(playerList)



"""NOMBRE DE JOUEURS DANS LA PARTIE"""
nbPlayers = len(playerList)
#print(nbPlayers)



"""DEFINITION DE LA MOITIE SUPERIEUR ET INFERIEURE"""
middleNumberPlayers = int(nbPlayers/2)
#print(middlenbPlayers)
first_halfPlayers = playerList[:middleNumberPlayers]
second_halfPlayers = playerList[middleNumberPlayers:]
#print(first_halfPlayers)
#print(second_halfPlayers)

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
    #print(i)
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
#print(playersToSort)

#Tri des joueurs par rang
playersToSort.sort()
#print(playersToSort)

#Tri des joueurs par rang et par score
playersToSort.sort(key=getScore, reverse=True)
playersSorted = playersToSort
print("playersSorted ROUND 1")
print(playersSorted)

playersToMatch = []
listOfPlayers = []
matchToPlay = []


"""ROUND 2"""
print()
print()
print()
print("ROUND 2 :")
#print("totalMatch")
#print(totalMatch)
#print("playersSorted")
#print(playersSorted)

getPlayerMatchs(totalMatch, playerMatch, playersSorted)

#print("totalMatch")
#print(totalMatch)

"""ROUND 3"""
print()
print()
print()
print("ROUND 3 :")
#print("totalMatch")
#print(totalMatch)
#print("playersSorted")
#print(playersSorted)

getPlayerMatchs(totalMatch, playerMatch, playersSorted)

#print("totalMatch")
#print(totalMatch)

"""ROUND 4"""
print()
print()
print()
print("ROUND 4 :")
#print("totalMatch")
#print(totalMatch)
#print("playersSorted")
#print(playersSorted)

getPlayerMatchs(totalMatch, playerMatch, playersSorted)

#print("totalMatch")
#print(totalMatch)
print()

playerMatch = []
playerOrder = []
match = []
for matchs in totalMatch:
    playerMatch.append(matchs)
for player in playersSorted:
    playerOrder.append(player[0])
#print("playerMatch")
#print(playerMatch)
#print("playerOrder")
#print(playerOrder)
#print("match")
#print(match)
matchToPlay.clear()
for players in playerOrder:
    playedMatchs = []
    for plays in totalMatch:
        player1 = plays[0][0]
        player2 = plays[1][0]
        if player1 == players:
            #print(player2)
            playedMatchs.append(player2)
        elif player2 == players:
            #print(player1)
            playedMatchs.append(player1)
    #print()
    print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))