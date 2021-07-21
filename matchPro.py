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
print()
print()
print("ROUND 2 :")
match = []
for matchs in round1:
    match.append(matchs)
print("PRECEDENTS MATCHS")
print(match)
playersToMatch = []
listOfPlayers = []
matchToPlay = []

#On transfert les joueurs triés dans les listes qui vont nous servir à comparer la liste des joueurs et les matchs à jouer ou déjà joués
for players in playerSorted:
    #print(players[0])
    playersToMatch.append(players[0])
    listOfPlayers.append(players[0])

#print(listOfPlayers)
#print()

#On boucle sur le nombre de joueurs présent dans le tournoi pour trouver un tuple valide
for players in listOfPlayers:
    #print("Joueur " + str(players))
    playedMatchs = []
    #print("Cas particulier à <= 4 : " + str((len(listOfPlayers) - len(matchToPlay))))
    #S'il ne reste plus que 4 joueurs, on met en place les tests particulier
    if (len(listOfPlayers) - len(matchToPlay)) <= 4:
        #print("ATTENTION ON EST DANS LE CAS PARTICULIER A 4")
        #print()
        for i in range(len(playersToMatch)):
            playedMatchs = []
            #print("i = " + str(i))
            #print("Joueur " + str(playersToMatch[i]))
            for plays in match:
                player1 = plays[0][0]
                player2 = plays[1][0]
                if player1 == playersToMatch[i]:
                    #print(player2)
                    playedMatchs.append(player2)
                elif player2 == playersToMatch[i]:
                    #print(player1)
                    playedMatchs.append(player1)
            #print(playedMatchs)
            if (playersToMatch[i + 1] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 1]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 1])
                del playersToMatch[i+1]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            elif (playersToMatch[i + 2] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 2]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 2])
                del playersToMatch[i+2]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            elif (playersToMatch[i + 3] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 3]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 3])
                del playersToMatch[i+3]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            #print(len(playersToMatch) - 1)
        break

    #Si le tuple à déjà été entré, on passe au joueur suivant en supprimant le joueur de la liste
    elif (playersToMatch[0] in matchToPlay) == True:
        #print("Tuple déjà trouvé")
        del playersToMatch[0]
    else:
        #On s'occupe de trouver les matchs déjà joués avec le joueur qu'on teste
        for plays in match:
            player1 = plays[0][0]
            player2 = plays[1][0]
            if player1 == players:
                #print(player2)
                playedMatchs.append(player2)
            elif player2 == players:
                #print(player1)
                playedMatchs.append(player1)
        #print("Match joués " + str(playedMatchs))
        #print(playersToMatch)
        #On cherche le joueur a matcher avec notre joueur actuel
        for i in range(len(playerSorted)):
            #print(len(playerSorted))
            #print(playersToMatch)
            #Si c'est le même joueur de chaque côté, on passe au joueur suivant
            if playersToMatch[0] == playersToMatch[i]:
                #print("On passe le 1er, celui qu'on cherche a matcher")
                pass
            #Si le matché a déjà été joué, on passe au joueur suivant
            elif (playersToMatch[i] in playedMatchs) == True:
                #print("Match déjà joué : Joueur " + str(playersToMatch[i]))
                pass
            #Si les autres tests sont passés, cela veux dire que nous pouvons créer le tuple entre les 2 joueurs.
            elif (playersToMatch[i] in matchToPlay) == True:
                #print("Match déjà dans le match marqués : Joueur " + str(playersToMatch[i]))
                pass
            else:
                #print("Joueur trouvé : Joueur " + str(playersToMatch[i]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i])
                del playersToMatch[0]
                break

    #print(playersToMatch)
    #print("matchToPlay :")
    #print(matchToPlay)
    #print()

print("PLACE AUX MATCHS")
print(matchToPlay)
print(playerSorted)
print()
for players in matchToPlay:
    #print(players)
    for i in range(len(playerSorted)):
        if players == playerSorted[i][0]:
            playerSorted.append(playerSorted[i])
            #print("AVANT TRI AVANT SUPPRESSION")
            #print(playerSorted)
            playerSorted.pop(i)
            #print("AVANT TRI APRES SUPPRESSION")
            #print(playerSorted)
            break

print("JOUEURS TRIÉS")
print(playerSorted)

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

print()
print("TEST DOUBLE MATCHS ROUND 2")
match = []
for matchs in round1:
    match.append(matchs)
for matchs in round2:
    match.append(matchs)
for players in listOfPlayers:
    playedMatchs = []
    for plays in match:
        player1 = plays[0][0]
        player2 = plays[1][0]
        if player1 == players:
            #print(player2)
            playedMatchs.append(player2)
        elif player2 == players:
            #print(player1)
            playedMatchs.append(player1)
    print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))

"""ROUND 3"""
print()
print()
print()
print("ROUND 3 :")
match = []
for matchs in round1:
    match.append(matchs)
for matchs in round2:
    match.append(matchs)
print("PRECEDENTS MATCHS")
print(match)
playersToMatch = []
listOfPlayers = []
matchToPlay = []

#On transfert les joueurs triés dans les listes qui vont nous servir à comparer la liste des joueurs et les matchs à jouer ou déjà joués
for players in playerSorted:
    #print(players[0])
    playersToMatch.append(players[0])
    listOfPlayers.append(players[0])

#print(listOfPlayers)
#print()

#On boucle sur le nombre de joueurs présent dans le tournoi pour trouver un tuple valide
for players in listOfPlayers:
    #print("Joueur " + str(players))
    playedMatchs = []
    #print("Cas particulier à <= 4 : " + str((len(listOfPlayers) - len(matchToPlay))))
    #S'il ne reste plus que 4 joueurs, on met en place les tests particulier
    if (len(listOfPlayers) - len(matchToPlay)) <= 4:
        #print("ATTENTION ON EST DANS LE CAS PARTICULIER A 4")
        #print()
        for i in range(len(playersToMatch)):
            playedMatchs = []
            #print("i = " + str(i))
            #print("Joueur " + str(playersToMatch[i]))
            for plays in match:
                player1 = plays[0][0]
                player2 = plays[1][0]
                if player1 == playersToMatch[i]:
                    #print(player2)
                    playedMatchs.append(player2)
                elif player2 == playersToMatch[i]:
                    #print(player1)
                    playedMatchs.append(player1)
            #print(playedMatchs)
            if (playersToMatch[i + 1] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 1]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 1])
                del playersToMatch[i+1]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            elif (playersToMatch[i + 2] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 2]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 2])
                del playersToMatch[i+2]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            elif (playersToMatch[i + 3] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 3]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 3])
                del playersToMatch[i+3]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            #print(len(playersToMatch) - 1)
        break

    #Si le tuple à déjà été entré, on passe au joueur suivant en supprimant le joueur de la liste
    elif (playersToMatch[0] in matchToPlay) == True:
        #print("Tuple déjà trouvé")
        del playersToMatch[0]
    else:
        #On s'occupe de trouver les matchs déjà joués avec le joueur qu'on teste
        for plays in match:
            player1 = plays[0][0]
            player2 = plays[1][0]
            if player1 == players:
                #print(player2)
                playedMatchs.append(player2)
            elif player2 == players:
                #print(player1)
                playedMatchs.append(player1)
        #print("Match joués " + str(playedMatchs))
        #print(playersToMatch)
        #On cherche le joueur a matcher avec notre joueur actuel
        for i in range(len(playerSorted)):
            #print(len(playerSorted))
            #print(playersToMatch)
            #Si c'est le même joueur de chaque côté, on passe au joueur suivant
            if playersToMatch[0] == playersToMatch[i]:
                #print("On passe le 1er, celui qu'on cherche a matcher")
                pass
            #Si le matché a déjà été joué, on passe au joueur suivant
            elif (playersToMatch[i] in playedMatchs) == True:
                #print("Match déjà joué : Joueur " + str(playersToMatch[i]))
                pass
            #Si les autres tests sont passés, cela veux dire que nous pouvons créer le tuple entre les 2 joueurs.
            elif (playersToMatch[i] in matchToPlay) == True:
                #print("Match déjà dans le match marqués : Joueur " + str(playersToMatch[i]))
                pass
            else:
                #print("Joueur trouvé : Joueur " + str(playersToMatch[i]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i])
                del playersToMatch[0]
                break

    #print(playersToMatch)
    #print("matchToPlay :")
    #print(matchToPlay)
    #print()

print("PLACE AUX MATCHS")
print(matchToPlay)
print(playerSorted)
print()
for players in matchToPlay:
    #print(players)
    for i in range(len(playerSorted)):
        if players == playerSorted[i][0]:
            playerSorted.append(playerSorted[i])
            #print("AVANT TRI AVANT SUPPRESSION")
            #print(playerSorted)
            playerSorted.pop(i)
            #print("AVANT TRI APRES SUPPRESSION")
            #print(playerSorted)
            break

print("JOUEURS TRIÉS")
print(playerSorted)

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

#Mise en mémoire du round 3
print(match)
round3 = match

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

print()
print("TEST DOUBLE MATCHS ROUND 3")
match = []
for matchs in round1:
    match.append(matchs)
for matchs in round2:
    match.append(matchs)
for matchs in round3:
    match.append(matchs)
for players in listOfPlayers:
    playedMatchs = []
    for plays in match:
        player1 = plays[0][0]
        player2 = plays[1][0]
        if player1 == players:
            #print(player2)
            playedMatchs.append(player2)
        elif player2 == players:
            #print(player1)
            playedMatchs.append(player1)
    print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))


"""ROUND 4"""
print()
print()
print()
print("ROUND 4 :")
match = []
for matchs in round1:
    match.append(matchs)
for matchs in round2:
    match.append(matchs)
for matchs in round3:
    match.append(matchs)
print("PRECEDENTS MATCHS")
print(match)
playersToMatch = []
listOfPlayers = []
matchToPlay = []

#On transfert les joueurs triés dans les listes qui vont nous servir à comparer la liste des joueurs et les matchs à jouer ou déjà joués
for players in playerSorted:
    #print(players[0])
    playersToMatch.append(players[0])
    listOfPlayers.append(players[0])

#print(listOfPlayers)
#print()

#On boucle sur le nombre de joueurs présent dans le tournoi pour trouver un tuple valide
for players in listOfPlayers:
    #print("Joueur " + str(players))
    playedMatchs = []
    #print("Cas particulier à <= 4 : " + str((len(listOfPlayers) - len(matchToPlay))))
    #S'il ne reste plus que 4 joueurs, on met en place les tests particulier
    if (len(listOfPlayers) - len(matchToPlay)) <= 4:
        #print("ATTENTION ON EST DANS LE CAS PARTICULIER A 4")
        #print()
        for i in range(len(playersToMatch)):
            playedMatchs = []
            #print("i = " + str(i))
            #print("Joueur " + str(playersToMatch[i]))
            for plays in match:
                player1 = plays[0][0]
                player2 = plays[1][0]
                if player1 == playersToMatch[i]:
                    #print(player2)
                    playedMatchs.append(player2)
                elif player2 == playersToMatch[i]:
                    #print(player1)
                    playedMatchs.append(player1)
            #print(playedMatchs)
            if (playersToMatch[i + 1] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 1]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 1])
                del playersToMatch[i+1]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            elif (playersToMatch[i + 2] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 2]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 2])
                del playersToMatch[i+2]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            elif (playersToMatch[i + 3] in playedMatchs) == False:
                #print("Le Joueur " + str(playersToMatch[i]) + " Jouera avec le Joueur " + str(playersToMatch[i + 3]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i + 3])
                del playersToMatch[i+3]
                del playersToMatch[0]
                #print(playersToMatch)
                for playersLeft in playersToMatch:
                    matchToPlay.append(playersLeft)
                #print(matchToPlay)
                #print()
                break
            #print(len(playersToMatch) - 1)
        break

    #Si le tuple à déjà été entré, on passe au joueur suivant en supprimant le joueur de la liste
    elif (playersToMatch[0] in matchToPlay) == True:
        #print("Tuple déjà trouvé")
        del playersToMatch[0]
    else:
        #On s'occupe de trouver les matchs déjà joués avec le joueur qu'on teste
        for plays in match:
            player1 = plays[0][0]
            player2 = plays[1][0]
            if player1 == players:
                #print(player2)
                playedMatchs.append(player2)
            elif player2 == players:
                #print(player1)
                playedMatchs.append(player1)
        #print("Match joués " + str(playedMatchs))
        #print(playersToMatch)
        #On cherche le joueur a matcher avec notre joueur actuel
        for i in range(len(playerSorted)):
            #print(len(playerSorted))
            #print(playersToMatch)
            #Si c'est le même joueur de chaque côté, on passe au joueur suivant
            if playersToMatch[0] == playersToMatch[i]:
                #print("On passe le 1er, celui qu'on cherche a matcher")
                pass
            #Si le matché a déjà été joué, on passe au joueur suivant
            elif (playersToMatch[i] in playedMatchs) == True:
                #print("Match déjà joué : Joueur " + str(playersToMatch[i]))
                pass
            #Si les autres tests sont passés, cela veux dire que nous pouvons créer le tuple entre les 2 joueurs.
            elif (playersToMatch[i] in matchToPlay) == True:
                #print("Match déjà dans le match marqués : Joueur " + str(playersToMatch[i]))
                pass
            else:
                #print("Joueur trouvé : Joueur " + str(playersToMatch[i]))
                matchToPlay.append(playersToMatch[0])
                matchToPlay.append(playersToMatch[i])
                del playersToMatch[0]
                break

    #print(playersToMatch)
    #print("matchToPlay :")
    #print(matchToPlay)
    #print()

print("PLACE AUX MATCHS")
print(matchToPlay)
print(playerSorted)
print()
for players in matchToPlay:
    #print(players)
    for i in range(len(playerSorted)):
        if players == playerSorted[i][0]:
            playerSorted.append(playerSorted[i])
            #print("AVANT TRI AVANT SUPPRESSION")
            #print(playerSorted)
            playerSorted.pop(i)
            #print("AVANT TRI APRES SUPPRESSION")
            #print(playerSorted)
            break

print("JOUEURS TRIÉS")
print(playerSorted)

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

#Mise en mémoire du round 4
print(match)
round4 = match

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

#Tri des joueurs² par rang et par score
playersToSort.sort(key=getScore, reverse=True)
playerSorted = playersToSort
print(playerSorted)

print()
print("TEST DOUBLE MATCHS ROUND 4")
match = []
for matchs in round1:
    match.append(matchs)
for matchs in round2:
    match.append(matchs)
for matchs in round3:
    match.append(matchs)
for matchs in round4:
    match.append(matchs)
for players in listOfPlayers:
    playedMatchs = []
    for plays in match:
        player1 = plays[0][0]
        player2 = plays[1][0]
        if player1 == players:
            #print(player2)
            playedMatchs.append(player2)
        elif player2 == players:
            #print(player1)
            playedMatchs.append(player1)
    print("Match joués par le Joueur " + str(players) + " : " + str(playedMatchs))
