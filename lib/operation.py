#from .auth import Auth
#si on souhaite importer une autre classe pour l'utiliser

class Operation:
    def __init__(self):
        pass

    def add(self, a, b):
        return a + b

    def dif(self, a, b):
        return a - b

    def prod(self, a, b):
        return a * b

    def div(self, a, b):
        return a / b

class Tournament:
    def __init__(self):
        pass

    def tournament_infos(self, a, b, c, e, f, g, h):
        self.name = a
        self.location = b
        self.date = c
        self.round = 4
        self.allround = e
        self.players = f
        self.time = g
        self.description = h
        return a, b, c, e, f

    def tournament_players(self, b):
        self.players = b
        return b

    def tournament_first_round(self, c):
        self.pairs = c
        return c

    def tournament_round_results(self, d):
        self.results = d
        return d

class Player:
    def __init__(self):
        pass

    def player_infos(self, a, b, c, d, e):
        self.name = a
        self.surname = b
        self.birthdate = c
        self.gender = d
        self.rank = e

        return a, b, c, d, e

class Match:
    def __init__(self):
        pass

    def match_infos(self, a, b ,c):
        self.round = a
        self.playerpair = b
        self.result = c

