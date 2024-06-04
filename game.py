import random


def day_discussion():
    return "Обсуждение началось. Подозреваемых на данный момент нет."


class MafiaGame:
    def __init__(self, players):
        self.players = players
        self.mafia = random.choice(players)
        self.citizens = [player for player in players if player != self.mafia]
        self.votes = {}
        self.winner = None

    def start_game(self):
        return f"Игра началась! В городе {len(self.players)} игроков. Подозреваемых на данный момент нет."

    def get_alive_players(self):
        return [player for player in self.players if player.is_alive()]

    def night_actions(self):
        if self.mafia.is_alive():
            target = random.choice(self.get_alive_players())
            return f"Мафия выбрала свою цель: {target.name}"
        else:
            return "Мафия уже мертва и не может совершать действия ночью."

    def vote(self, player, target):
        if player in self.get_alive_players() and target in self.get_alive_players():
            self.votes[player] = target
            return f"{player.name} проголосовал против {target.name}"
        else:
            return "Ошибка: невозможно проголосовать. Проверьте, что оба игрока живы."

    def resolve_votes(self):
        if not self.votes:
            return "Голосов нет."
        vote_counts = {}
        for target in self.votes.values():
            if target in vote_counts:
                vote_counts[target] += 1
            else:
                vote_counts[target] = 1
        max_votes = max(vote_counts.values())
        targets_with_max_votes = [target for target, count in vote_counts.items() if count == max_votes]
        if len(targets_with_max_votes) == 1:
            target = targets_with_max_votes[0]
            target.die()
            return f"{target.name} был выбран и покинул игру."
        else:
            return "Никто не был выбран. Ничья."

    def check_winner(self):
        if self.mafia.is_alive() and len(self.citizens) == 0:
            self.winner = "Мафия"
        elif not self.mafia.is_alive():
            self.winner = "Мирные жители"
        return f"Победитель: {self.winner}" if self.winner else "Победитель пока не определен."

    def reset_game(self):
        self.players = []
        self.mafia = None
        self.citizens = []
        self.votes = {}
        self.winner = None


class Player:
    def __init__(self, name):
        self.name = name
        self.alive = True

    def is_alive(self):
        return self.alive

    def die(self):
        self.alive = False
