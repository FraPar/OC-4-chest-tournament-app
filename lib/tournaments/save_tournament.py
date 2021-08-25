from tinydb import TinyDB, Query


class SaveStateTournament():
    """Contrôleur reponsable de la sauvegarde d'un tournoi"""

    def __init__(self, player_list_by_rank, total_match, tournament_index, tournament_data, load_state):
        self.db = TinyDB('db.json')
        self.tournament_table = self.db.table('tournament_table')
        self.player_list_by_rank = player_list_by_rank
        self.total_match = total_match
        self.tournament_index = tournament_index
        self.tournament_data = tournament_data
        self.load_state = load_state

    def starting_tournament(self):
        if self.load_state is False:
            # renseignement des informations concernant le tournoi
            tournament_name = input("Entrez le nom du tournoi : ")
            tournament_location = input("Entrez le lieu du tournoi : ")
            tournament_date = input("Entrez la date du tournoi : ")
            tournament_round = int(4)
            tournament_time = input("Entrez le temps du tournoi : ")
            tournament_description = input("Entrez la description du tournoi : ")

            # définition de l'étape de sauvegarde au niveau 1
            self.save_step = 1
            tournament_data = {"Tournament_Id": self.tournament_index, "Name": tournament_name,
                               "Location": tournament_location, "Date": tournament_date,
                               "Round": tournament_round, "Time": tournament_time,
                               "Description": tournament_description, "save_step": self.save_step}
            # sauvegarde des données renseignées dans la BDD
            self.tournament_table.insert(tournament_data)

    def save_players(self):
        self.save_step = 2
        self.tournament_data = {"players": self.player_list_by_rank,
                            "save_step": self.save_step}
        # Mise à jour du tournoi correspondant dans la BDD des tournois
        self.tournament_table.update(self.tournament_data,
                                     Query().Tournament_Id == self.tournament_index)

    def save_round_one(self):
        self.save_step = 3
        self.tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
        # Mise à jour du tournoi correspondant dans la BDD des tournois
        self.tournament_table.update(self.tournament_data,
                                     Query().Tournament_Id == self.tournament_index)

    def save_round_two(self):
        self.save_step = 4
        self.tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
        # Mise à jour du tournoi correspondant dans la BDD des tournois
        self.tournament_table.update(self.tournament_data,
                                     Query().Tournament_Id == self.tournament_index)

    def save_round_three(self):
        self.save_step = 5
        self.tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
        # Mise à jour du tournoi correspondant dans la BDD des tournois
        self.tournament_table.update(self.tournament_data,
                                     Query().Tournament_Id == self.tournament_index)

    def save_round_four(self):
        self.save_step = 6
        self.tournament_data = {"matchs": self.total_match, "save_step": self.save_step}
        # Mise à jour du tournoi correspondant dans la BDD des tournois
        self.tournament_table.update(self.tournament_data,
                                     Query().Tournament_Id == self.tournament_index)

    def send_save(self):
        self.tournament_table.update(self.tournament_data,
                                     Query().Tournament_Id == self.tournament_index)