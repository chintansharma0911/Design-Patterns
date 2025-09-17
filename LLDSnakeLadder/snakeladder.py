from abc import ABC, abstractmethod
from enum import Enum
import random
from collections import deque

# -----------------------
# Observer Pattern
# -----------------------

class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str):
        pass


class ConsoleNotifier(IObserver):
    def update(self, msg: str):
        print("[NOTIFY] ", msg)


# -----------------------
# Board Entities
# -----------------------

class BoardEntity(ABC):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @abstractmethod
    def display(self):
        pass


class Snake(BoardEntity):
    def display(self):
        print(f"Snake: {self.start} -> {self.end}")


class Ladder(BoardEntity):
    def display(self):
        print(f"Ladder: {self.start} -> {self.end}")


# -----------------------
# Difficulty Levels
# -----------------------

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


# -----------------------
# Strategy Pattern (Board setup)
# -----------------------

class SetStrategy(ABC):
    @abstractmethod
    def set_board(self, board):
        pass


class RandomBoardStrat(SetStrategy):
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty

    def set_board(self, board):
        if self.difficulty == Difficulty.EASY:
            snakes = random.randint(2, 3)
            ladders = random.randint(6, 8)
        elif self.difficulty == Difficulty.MEDIUM:
            snakes = random.randint(4, 6)
            ladders = random.randint(4, 6)
        else:  # HARD
            snakes = random.randint(6, 8)
            ladders = random.randint(2, 4)

        for _ in range(snakes):
            start = random.randint(10, board.size - 1)
            end = random.randint(1, start - 1)
            board.add_board_entity(Snake(start, end))

        for _ in range(ladders):
            start = random.randint(1, board.size - 10)
            end = random.randint(start + 1, board.size - 1)
            board.add_board_entity(Ladder(start, end))


class StandardStrat(SetStrategy):
    def set_board(self, board):
        # Fixed snakes and ladders
        board.add_board_entity(Snake(14, 7))
        board.add_board_entity(Snake(31, 26))
        board.add_board_entity(Snake(38, 20))
        board.add_board_entity(Ladder(3, 22))
        board.add_board_entity(Ladder(5, 8))
        board.add_board_entity(Ladder(11, 26))


class CustomConfStrat(SetStrategy):
    def __init__(self):
        self.snake_positions = []
        self.ladder_positions = []

    def add_snake(self, start, end):
        self.snake_positions.append((start, end))

    def add_ladder(self, start, end):
        self.ladder_positions.append((start, end))

    def set_board(self, board):
        for s, e in self.snake_positions:
            board.add_board_entity(Snake(s, e))
        for s, e in self.ladder_positions:
            board.add_board_entity(Ladder(s, e))


# -----------------------
# Rules
# -----------------------

class Rule(ABC):
    @abstractmethod
    def is_valid_move(self, pos, dice_val, board):
        pass

    @abstractmethod
    def calc_new_pos(self, pos, dice_val, board):
        pass

    @abstractmethod
    def check_win(self, pos, board):
        pass


class StandardRules(Rule):
    def is_valid_move(self, pos, dice_val, board):
        return pos + dice_val <= board.size

    def calc_new_pos(self, pos, dice_val, board):
        new_pos = pos + dice_val
        if new_pos in board.entities:
            new_pos = board.entities[new_pos].end
        return new_pos

    def check_win(self, pos, board):
        return pos == board.size


# -----------------------
# Board
# -----------------------

class Board:
    def __init__(self, size=50):
        self.size = size
        self.sl = []
        self.entities = {}

    def add_board_entity(self, entity: BoardEntity):
        self.sl.append(entity)
        self.entities[entity.start] = entity

    def display(self):
        print("\n--- Board Entities ---")
        for ent in self.sl:
            ent.display()
        print("----------------------\n")


# -----------------------
# Game Components
# -----------------------

class Dice:
    def __init__(self, faces=6):
        self.faces = faces

    def roll(self):
        return random.randint(1, self.faces)


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.pos = 0
        self.score = 0


# -----------------------
# Game Class
# -----------------------

class Game:
    def __init__(self, board, dice, rules):
        self.board = board
        self.dice = dice
        self.rules = rules
        self.players = deque()
        self.observers = []
        self.game_over = False

    def add_player(self, player):
        self.players.append(player)

    def add_observer(self, obs: IObserver):
        self.observers.append(obs)

    def notify(self, msg):
        for obs in self.observers:
            obs.update(msg)

    def play(self):
        while not self.game_over:
            player = self.players.popleft()
            roll = self.dice.roll()
            self.notify(f"{player.name} rolled a {roll}")

            if self.rules.is_valid_move(player.pos, roll, self.board):
                player.pos = self.rules.calc_new_pos(player.pos, roll, self.board)
                self.notify(f"{player.name} moved to {player.pos}")

            if self.rules.check_win(player.pos, self.board):
                self.notify(f"{player.name} WINS!")
                self.game_over = True
                break

            self.players.append(player)


# -----------------------
# Game Factory
# -----------------------

class GameFactory:
    @staticmethod
    def create_game(difficulty: Difficulty = None):
        board = Board(50)

        if difficulty:  # Random board based on difficulty
            strategy = RandomBoardStrat(difficulty)
        else:  # Default to standard
            strategy = StandardStrat()

        strategy.set_board(board)
        rules = StandardRules()
        dice = Dice(6)

        game = Game(board, dice, rules)
        game.add_observer(ConsoleNotifier())
        return game


# -----------------------
# Main Execution
# -----------------------

if __name__ == "__main__":
    # You can switch difficulty here: EASY / MEDIUM / HARD
    game = GameFactory.create_game(Difficulty.HARD)

    p1 = Player(1, "Alice")
    p2 = Player(2, "Bob")

    game.add_player(p1)
    game.add_player(p2)

    game.board.display()
    game.play()
