#from lib import Operation
#from lib.operation import Operation (sans __init__.py)
from lib import Tournament
from tinydb import TinyDB, Query, where
from random import randint
import operator

db = TinyDB('db.json')



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



"""ROUND 1"""
print()
print("ROUND 1 :")
match = []

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
    match.append(([first_halfPlayers[i], x], [second_halfPlayers[i], y]))

#Mise en mémoire du round 1
print(match)
round1 = match

"""TRI DES JOUEURS PAR RANG ET PAR POINTS"""
#Prise du score
def getScore(elem):
    return elem[1]

#Tri des joueurs
playersToSort = []
for i in range(middleNumberPlayers):
    playersToSort.append(match[i][0])
    playersToSort.append(match[i][1])
#print(playersToSort)

#Tri des joueurs par rang
playersToSort.sort()
#print(playersToSort)

#Tri des joueurs par rang et par score
playersToSort.sort(key=getScore, reverse=True)
playerSorted = playersToSort
print(playerSorted)



"""ROUND 2"""
print()
print("ROUND 2 :")

match = []

for i in range(0, len(playerSorted),2):
    #print(i)
    randomScore = [0, 0.5, 1]
    x = randomScore[randint(0, 2)]
    if x == 0:
        x = playerSorted[i][1]
        y = playerSorted[i+1][1] + 1
    elif x == 0.5:
        y = playerSorted[i+1][1] + 0.5
        x = playerSorted[i][1] + 0.5
    else:
        x = playerSorted[i][1] + 1
        y = playerSorted[i+1][1]
    match.append(([playerSorted[i][0], x], [playerSorted[i+1][0], y]))

#Mise en mémoire du round 2
print(match)
round2 = match

"""TRI DES JOUEURS PAR RANG ET PAR POINTS"""

#Tri des joueurs
playersToSort = []
for i in range(middleNumberPlayers):
    playersToSort.append(match[i][0])
    playersToSort.append(match[i][1])
#print(playersToSort)

#Tri des joueurs par rang
playersToSort.sort()
#print(playersToSort)

#Tri des joueurs par rang et par score
playersToSort.sort(key=getScore, reverse=True)
playerSorted = playersToSort
print(playerSorted)



"""ROUND 3"""


"""TEST DE MATCHS DEJA JOUES"""
"""VERSION 1"""
"""
print()
print("ROUND 3 :")
print("round1")
print(round1)
print("round2")
print(round2)
print("preview round3")
print(playerSorted)
print()
validMatch = []
invalidMatch = []
invalidMatchDetected = False
for i in range(0, len(playerSorted),2):
    #print("i = ")
    #print(i)
    player1 = playerSorted[i][0]
    player2 = playerSorted[i+1][0]
    print("Joueur 1 : " + str(player1))
    print("Joueur 2 : " + str(player2))
    #print(middleNumberPlayers)
    for j in range(middleNumberPlayers):
        round1player1 = round1[j][0][0]
        round1player2 = round1[j][1][0]
        round2player1 = round2[j][0][0]
        round2player2 = round2[j][1][0]
        #print("ROUND 1 JOUEUR 1 : " + str(round1player1))
        #print("ROUND 1 JOUEUR 2 : " + str(round1player2))
        #print("ROUND 2 JOUEUR 1 : " + str(round2player1))
        #print("ROUND 2 JOUEUR 2 : " + str(round2player2))
        #print("J dans la 1ere partie = " + str(j))
        if player1 == round1player1 or player1 == round1player2:
            if player2 == round1player1 or player2 == round1player2:
                print("match déjà joué : " + str(player1) + "Versus" + str(player2))
                invalidMatch.append(playerSorted[i])
                invalidMatch.append(playerSorted[i+1])
                invalidMatchDetected = True
        elif player2 == round1player1 or player2 == round1player2:
            if player1 == round1player1 or player1 == round1player2:
                print("match déjà joué : " + str(player1) + "Versus" + str(player2))
                invalidMatch.append(playerSorted[i])
                invalidMatch.append(playerSorted[i+1])
                invalidMatchDetected = True
        elif player1 == round2player1 or player1 == round2player2:
            if player2 == round2player1 or player2 == round2player2:
                print("match déjà joué : " + str(player1) + "Versus" + str(player2))
                invalidMatch.append(playerSorted[i])
                invalidMatch.append(playerSorted[i+1])
                invalidMatchDetected = True
        elif player2 == round2player1 or player2 == round2player2:
            if player1 == round2player1 or player1 == round2player2:
                print("match déjà joué : " + str(player1) + "Versus" + str(player2))
                invalidMatch.append(playerSorted[i])
                invalidMatch.append(playerSorted[i+1])
                invalidMatchDetected = True
    if invalidMatchDetected == False:
            validMatch.append(playerSorted[i])
            validMatch.append(playerSorted[i+1])
    invalidMatchDetected = False
    #print(str(player1) + " n'a jamais joué avec " + str(player2))
print("FIN DU TEST")
print(invalidMatch)
print(validMatch)
match = []
"""

"""VERSION 2"""
print()
print("ROUND 3 :")
print("Classement pre-round3")
print(playerSorted)
allMatchs = []

#Je regroupe l'ensemble des matchs
for datas in round1:
    allMatchs.append(datas)
for datas in round2:
    allMatchs.append(datas)
print("Tous les matchs joués :")
print(allMatchs)

print("Test des matchs :")
for i in range(0, len(playerSorted), 2):
    player1 = playerSorted[i][0]
    player2 = playerSorted[i+1][0]
    print("Joueur : " + str(player1) + " VS Joueur : " + str(player2))
    #while rebuildMatch == True:
    for j in range(len(allMatchs)):
        #print(j)
        allMatchsPlayer1 = allMatchs[j][0][0]
        allMatchsPlayer2 = allMatchs[j][1][0]
        #print(allMatchsPlayer1)
        #print(allMatchsPlayer2)
        if player1 == allMatchsPlayer1 or player1 == allMatchsPlayer2:
            if player2 == allMatchsPlayer1 or player2 == allMatchsPlayer2:
                print("Match déjà joué")
        elif player2 == allMatchsPlayer1 or player2 == allMatchsPlayer2:
            if player1 == allMatchsPlayer1 or player1 == allMatchsPlayer2:
                print("Match déjà joué")

