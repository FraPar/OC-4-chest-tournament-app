#from lib import Operation
#from lib.operation import Operation (sans __init__.py)
from lib import Tournament
from tinydb import TinyDB, Query, where
from random import *
import operator

db = TinyDB('db.json')


"""newOperation = Operation()

x = 5
y = 7

sum = newOperation.add(x, y)

print(sum)"""


"""print(db.search(where("Name") == "1"))"""

# --- CHOIX EN DEBUT DE PROGRAMME --- #
menuChoice = input("1 = Tournoi; 2 = Joueurs; 3 = Match ; 4 = Création complète : ")
#print(menuChoice)

# --- DEFINITION DES TABLES EN BASE DE DONNEES --- #
tournamentTable = db.table('tournament_table')
playerTable = db.table('player_table')
roundTable = db.table('round_table')

# --- CHOIX DE LA PARTIE TOURNOI --- #
if menuChoice == "1":
    tournamentChoice = input("1 = Ajouter un Tournoi; 2 = Supprimer un Tournoi; 3 = Consulter les Tournois : ")
    if tournamentChoice == "1":
        tournamentName = input("Entrez le nom du tournoi : ")
        tournamentLocation = input("Entrez le lieu du tournoi : ")
        tournamentDate = input("Entrez la date du tournoi : ")
        tournamentRound = input("Entrez le nombre de round du tournoi : ")
        #tournamentAllRound = input("Entrez le nom du tournoi : ")
        #tournamentPlayers = input("Entrez le nom des joueurs : ")
        tournamentTime = input("Entrez le temps du tournoi : ")
        tournamentDescription = input("Entrez la description du tournoi : ")
        #tournamentData = {"Name":tournamentName, "Location":tournamentLocation, "Date":tournamentDate, "Round":tournamentRound, "Players":{'Player1':[], 'Player2':{}, 'Player3':{}, 'Player4':{}, 'Player5':{}, 'Player6':{}, 'Player7':{}, 'Player8':{}}, "Time":tournamentTime, "Description":tournamentDescription}
        tournamentData = {"Name":tournamentName, "Location":tournamentLocation, "Date":tournamentDate, "Round":tournamentRound, "Time":tournamentTime, "Description":tournamentDescription}
        tournamentTable.insert(tournamentData)

    elif tournamentChoice == "2":
        for datas in tournamentTable.all():
            print(datas)
        deleteChoice = input("Quel tournoi souhaitez vous supprimer ? ")
        tournamentTable.remove(where('Name') == deleteChoice)

    elif tournamentChoice == "3":
        for datas in tournamentTable.all():
            print(datas)

    else:
        print("Veuillez taper une commande prévue")

# --- CHOIX DE LA PARTIE JOUEUR --- #
elif menuChoice == "2":
    playerChoice = input("1 = Ajouter un Joueur; 2 = Consulter les Joueurs : ")
    if playerChoice == "1":
        for datas in tournamentTable.all():
            print("Tournoi : " + datas.get('Name'))
        tournamentChoice = input("Séléctionnez le tournoi :")
        print(db.tables())
        showTable = playerTable.search(where("Name") == tournamentChoice)
        print(showTable)

        playerName = input("Entrez le nom du joueur : ")
        playerSurname = input("Entrez le prénom du joueur : ")
        playerBirthdate = input("Entrez la date de naissance du joueur : ")
        playerGender = input("Entrez le genre du joueur : ")
        playerRank = input("Entrez le rang du joueur : ")
        playerData = {"tournamentName":tournamentChoice, "playerName":playerName, "playerSurname":playerSurname, "playerBirthdate":playerBirthdate, "playerGender":playerGender, "playerRank":playerRank}

        playerTable.insert(playerData)

        for datas in playerTable.all():
            print(datas)

        """
        #print(db.all())
        print("Données entrée : " + str(playerData))
        print("Dictionnaire visé : " + str(showTable[0]))
        print("Contenant : " + str(showTable[0]["Players"]["Player1"]))
        #print(showTable[0]["Name"])
        dataToUpdate = showTable[0]["Players"]
        updatedData = {"Player1":playerData}
        dataToUpdate.update({"Player1":updatedData},  dataToUpdate == "Player1")
        #showTable[0]["Players"].update({"Player1":playerData},)
        #print(showTable[0]["Name"])
        print("Maintenant : " + str(showTable[0]["Players"]["Player1"]))
        print("Globalement : " + str(showTable[0]))
        print("db.all() = " + str(db.table('tournament_table').all()))
        #tournamentTable.search(where("Name") == tournamentChoice)[0]["Players"].update({"Player1":{"a"}})
        #print("TEST : " + str(db.update(where("Name") == tournamentChoice)[0]["Players"]))
        #db.search(where("Name") == tournamentChoice)[0]["Players"][1] = playerData
        #db["Name" == tournamentChoice][0]["Players"]["Player1"] = playerData
        #db.search(User.name.exists())
        #pip install tabulate
        #for datas in tournamentTable.all():
        #    print(datas)
        """

    if playerChoice == "2":
        for datas in playerTable.all():
            print(datas)

# --- CHOIX DE LA PARTIE MATCH --- #
elif menuChoice == "3":
    print("Match pas encore dispo")

elif menuChoice == "4":
    """DONNEES TOURNOI"""
    tournamentName = input("Entrez le nom du tournoi : ")
    tournamentLocation = input("Entrez le lieu du tournoi : ")
    tournamentDate = input("Entrez la date du tournoi : ") #1 ou plusieurs jours
    tournamentRound = 4 #par défaut
    tournamentTime = input("Entrez le temps du tournoi : ") #bullet, blitz ou coup rapide
    tournamentDescription = input("Entrez la description du tournoi : ") #Remarques générales du directeur du tournoi
    tournamentData = {"Name":tournamentName, "Location":tournamentLocation, "Date":tournamentDate, "Round":tournamentRound, "Time":tournamentTime, "Description":tournamentDescription}
    tournamentTable.insert(tournamentData)

    """DONNEES JOUEURS"""
    swissRule = []
    for i in range(1,9):
        """
        playerName = input("Entrez le nom du joueur : ")
        playerSurname = input("Entrez le prénom du joueur : ")
        playerBirthdate = input("Entrez la date de naissance du joueur : ")
        playerGender = input("Entrez le genre du joueur : ")
        playerRank = input("Entrez le rang du joueur : ")
        playerData = {"tournamentName":tournamentName, "index":i, "playerName":playerName, "playerSurname":playerSurname, "playerBirthdate":playerBirthdate, "playerGender":playerGender, "playerRank":playerRank}
        """
        playerData = {"tournamentName":tournamentName, "index":i, "playerName":i, "playerSurname":i, "playerBirthdate":i, "playerGender":i, "playerRank":1}
        playerTable.insert(playerData)

        #TRI DES JOUEURS SELON LEUR ELO
        print(playerData["playerRank"])
        print(len(swissRule))
        if len(swissRule) == 0:
            print("1ere entrée")
            swissRule.append((i, playerData["playerRank"]))
            pass
        else:
            for j in range(len(swissRule)):
                print("j = " + str(j))
                if swissRule[j][1] < playerData["playerRank"]:
                    print("côte sup")
                    print(swissRule[j][1])
                    print(playerData["playerRank"])
                    swissRule.insert(j, (i, playerData["playerRank"]))
                    break
                elif  j == (len(swissRule) - 1) :
                    print("i == len(swissRule)")
                    swissRule.append((i, playerData["playerRank"]))
                    break
        #swissRule.append((i, playerData["playerRank"]))
        #print(swissRule[0][1])
        print(swissRule)
        print(str(len(swissRule)) + " joueur(s) crée(s)")

    """ROUND 1"""
    #sortedDict = sorted(swissRule, key=operator.itemgetter(1))
    #print(sortedDict)
    print("ROUND 1")
    roundTuple = []

    print("Joueur " + str(swissRule[0][0]) + " contre Joueur " + str(swissRule[4][0]))
    matchWinner = int(input("Entrez le numéro du gagnant : "))
    scoreW = 1
    scoreL = 0
    if matchWinner == swissRule[0][0]:
        matchLoser = swissRule[4][0]
    elif matchWinner == swissRule[4][0]:
        matchLoser = swissRule[0][0]
    else:
        print("Tapez un joueur valide")
    print("Winner : " + str(matchWinner) + " ; Loser : " + str(matchLoser))
    tupleData = ([matchWinner,scoreW], [matchLoser,scoreL])
    roundTuple.append(tupleData)
    print(roundTuple)

    print("Joueur " + str(swissRule[1][0]) + " contre Joueur " + str(swissRule[5][0]))
    matchWinner = int(input("Entrez le numéro du gagnant : "))
    scoreW = 1
    scoreL = 0
    if matchWinner == swissRule[1][0]:
        matchLoser = swissRule[5][0]
    elif matchWinner == swissRule[5][0]:
        matchLoser = swissRule[1][0]
    else:
        print("Tapez un joueur valide")
    print("Winner : " + str(matchWinner) + " ; Loser : " + str(matchLoser))
    tupleData = ([matchWinner,scoreW], [matchLoser,scoreL])
    roundTuple.append(tupleData)
    print(roundTuple)

    print("Joueur " + str(swissRule[2][0]) + " contre Joueur " + str(swissRule[6][0]))
    matchWinner = int(input("Entrez le numéro du gagnant : "))
    scoreW = 1
    scoreL = 0
    if matchWinner == swissRule[2][0]:
        matchLoser = swissRule[6][0]
    elif matchWinner == swissRule[6][0]:
        matchLoser = swissRule[2][0]
    else:
        print("Tapez un joueur valide")
    print("Winner : " + str(matchWinner) + " ; Loser : " + str(matchLoser))
    tupleData = ([matchWinner,scoreW], [matchLoser,scoreL])
    roundTuple.append(tupleData)
    print(roundTuple)

    print("Joueur " + str(swissRule[3][0]) + " contre Joueur " + str(swissRule[7][0]))
    matchWinner = int(input("Entrez le numéro du gagnant : "))
    scoreW = 1
    scoreL = 0
    if matchWinner == swissRule[3][0]:
        matchLoser = swissRule[7][0]
    elif matchWinner == swissRule[7][0]:
        matchLoser = swissRule[3][0]
    else:
        print("Tapez un joueur valide")
    print("Winner : " + str(matchWinner) + " ; Loser : " + str(matchLoser))
    tupleData = ([matchWinner,scoreW], [matchLoser,scoreL])
    roundTuple.append(tupleData)

    roundData = {"tournamentName":tournamentName, "round":1, "matchs":roundTuple}
    roundTable.insert(roundData)

    """ROUND 2"""

    print("ROUND2")
    print("swissRule")
    print(swissRule)
    print("roundTuple")
    print(roundTuple)
    """print("roundTuple[0]")
    print(roundTuple[0])
    print("roundTuple[0][0]")
    print(roundTuple[0][0])
    print("roundTuple[0][0][0]")
    print(roundTuple[0][0][0])"""

    nextRound = []
    i = 0
    for tuples in roundTuple[::-1]:
        j = 0
        for datas in swissRule:
            """print("datas[0]")
            print(datas[0])
            print("J = ")
            print(j)"""
            if tuples[0][0] == datas[0]:
                rank = j + 1
                break
            j += 1
        print("I est égal à : " + str(i))
        print("Le joueur " + str(tuples[0][0]) + " est de rang " + str(rank))
        if (len(swissRule)/2) > rank:
            print(str(len(swissRule)/2) + "est > à " + str(rank))
            nextRound.insert(i, tuples[1])
            nextRound.insert(-i, tuples[0])
        elif (len(swissRule)/2) <= rank:
            print(str(len(swissRule)/2) + "est < à " + str(rank))
            nextRound.insert(i, tuples[1])
            nextRound.insert(-i, tuples[0])
        print(nextRound)
        i += 1

    """ROUND 3"""



    """ROUND 4"""


else:
    print("Veuillez taper une commande prévue à cet effet")