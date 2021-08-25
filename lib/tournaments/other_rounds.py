import random
from .play_match import PlayMatch


class OtherRounds:
    """Jouer les rounds 2 à 4"""

    def __init__(self, total_match, players_sorted):
        self.players_sorted = players_sorted
        self.total_match = total_match

    # fonction globale permettant d'assurer les rounds 2 à 4
    def get_player_match(self):
        self.player_match.clear()
        self.player_order.clear()
        # on prépare les données de joueurs pour mettre en
        # place les paires du round
        # on insert l'ensemble des matchs dans une liste
        # pour ne pas avoir de matchs doublons
        for matchs in self.total_match:
            self.player_match.append(matchs)
        # on insert les joueurs par rapport à leur score
        # et leur rang dans une variable
        for player in self.players_sorted:
            self.player_order.append(player[0])
        # fonction permettant de connaître quels match ont été joué par nos joueurs
        OtherRounds.match_played(self)
        # fonction permettant de trouver un match dans le cas d'un doublon de match
        OtherRounds.match_to_add(self)
        # fonction permettant d'associer les joueurs entre eux avant de jouer le match
        self.sort_player_by_match()
        # fonction permettant de jouer le match
        PlayMatch.play_match(self)
        # fonction permettant de trier les joueurs selon leur rang / nouveau score
        self.sort_players_by_score()

    # fonction permettant de connaître les matchs joués par notre joueur
    def match_played(self):
        self.match_to_play.clear()
        # on boucle sur les joueurs du tournoi, du 1er au dernier
        for players in self.player_order:
            played_matchs = []
            # on boucle sur les matchs déjà joué lors du tournoi
            for plays in self.total_match:
                player1 = plays[0][0]
                player2 = plays[1][0]
                # on teste si le joueur 1 est le joueur sur lequel
                # on boucle pour connaître son adversaire
                if player1 == players:
                    played_matchs.append(player2)
                # on teste si le joueur 2 est le joueur sur lequel
                # on boucle pour connaître son adversaire
                elif player2 == players:
                    played_matchs.append(player1)
            # on appelle la fonction permettant de mettre
            # un adversaire face à un autre
            OtherRounds.sort_match(self, played_matchs, players)
        pass

    # fonction permettant de mettre un joueur face à un
    # autre sans doublon de match
    def sort_match(self, played_matchs, players):
        for i in range(len(self.player_order)):
            # on teste si le joueur n'a pas déjà été aloué
            # a un autre match dans ce round, s'il n'a pas
            # déjà été joué ou si on ne met pas un joueur
            # face à lui même
            if players != self.player_order[i] and \
                         (self.player_order[i] in played_matchs) is False and \
                         ((players in self.match_to_play) is False and
                          (self.player_order[i] in self.match_to_play) is False):
                self.match_to_play.append(players)
                self.match_to_play.append(self.player_order[i])
                break

    # fonction permettant de gérer le cas particulier des 2
    # derniers joueurs ayant déjà joué ensemble
    def match_to_add(self):
        # on met i à 3 pour garder les 4 derniers joueurs dans
        # notre piscine de joueurs à mettre en face
        i = 3
        # on teste si tous les matchs ont été alloué ou non.
        while len(self.match_to_play) < len(self.player_list) \
                and i <= len(self.player_list):
            i += 1
            # on récupère les 4+ derniers joueurs pour trouver un match à jouer
            new_player_order = self.player_order[-i:]
            # on mélange les joueurs pour trouver un match à jouer
            random.shuffle(new_player_order)
            self.player_order = self.player_order[:4]
            # on ajoute les joueurs ayant été mis face à face pour
            # tester s'ils ont déjà joués ensemble
            for players in new_player_order:
                self.player_order.append(players)
            # on appelle la fonction permettant de connaître quels
            # match ont été joué par nos joueurs
            OtherRounds.match_played(self)
            # si le nombre de joueurs présents dans le tournoi n'est
            # pas équivalent à celui de joueurs a qui on a trouvé un
            # match, on continue la boucle
            if len(self.match_to_play) < len(self.player_list):
                continue