from datetime import datetime


class Tournament:
    """Représente un tournoi commencé par l'utilisateur."""

    def __init__(self, title, content=None, tournament=None, players=[]):
        self.updated_datetime = None
        self.title = title
        self.content = content
        self.created_datetime = datetime.now()
        self.tournament = tournament
        self.players = []
        self.add_players(*players)

    @property
    def title(self):
        """Titre du tournoi."""
        return self._title

    @title.setter
    def title(self, new_title):
        self._title = new_title
        self.updated_datetime = datetime.now()

    def add_players(self, *players):
        """Ajouter un ou plusieurs joueurs au tournoi."""
        for player in players:
            player = Player(player)
            player.add_note(self)
            self.players.append(player)

    def move(self, new_tournament):
        """Déplacer le tournoi dans un autre dossier."""
        self.tournament = new_tournament

    def __repr__(self):
        return f"Tournament(title={self.title})"


class Match:
    def __init__(self):
        self.title = None
        self.players = []
        self.created_datetime = None
        self.updated_datetime = None

    def create_match(self):
        pass

    def search(self, text):
        pass

    def search_content(self, text):
        pass

    def __repr__(self):
        return f"Match(title={self.title})"


class Player:
    def __init__(self, name):
        self.name = name
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def __repr__(self):
        return f"Player(name={self.name})"
