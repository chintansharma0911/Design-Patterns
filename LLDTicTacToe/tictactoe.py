from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str) -> None:
        pass


class ConsoleNotifier(IObserver):
    def update(self, msg: str) -> None:
        print(msg)


@dataclass
class Symbol:
    mark: str

    def get_mark(self) -> str:
        return self.mark


@dataclass
class Player:
    id: int
    name: str
    symbol: Symbol
    score: int = 0


class Rules(ABC):
    @abstractmethod
    def is_valid_move(self, board: "Board", row: int, col: int) -> bool:
        pass

    @abstractmethod
    def check_win(self, board: "Board", symbol: Symbol) -> bool:
        pass

    @abstractmethod
    def check_draw(self, board: "Board") -> bool:
        pass


class StandardRules(Rules):
    def is_valid_move(self, board: "Board", row: int, col: int) -> bool:
        return board.is_cell_empty(row, col)

    def check_win(self, board: "Board", symbol: Symbol) -> bool:
        n = board.size
        g = board.grid
        m = symbol.get_mark()

        # Check rows
        for r in range(n):
            if all(g[r][c] is not None and g[r][c].get_mark() == m for c in range(n)):
                return True

        # Check cols
        for c in range(n):
            if all(g[r][c] is not None and g[r][c].get_mark() == m for r in range(n)):
                return True

        # Main diagonal
        if all(g[i][i] is not None and g[i][i].get_mark() == m for i in range(n)):
            return True

        # Anti-diagonal
        if all(g[i][n - 1 - i] is not None and g[i][n - 1 - i].get_mark() == m for i in range(n)):
            return True

        return False

    def check_draw(self, board: "Board") -> bool:
        return all(board.grid[r][c] is not None for r in range(board.size) for c in range(board.size))


class Board:
    def __init__(self, size: int = 3):
        self.size = size
        # grid holds Optional[Symbol]
        self.grid: List[List[Optional[Symbol]]] = [[None for _ in range(size)] for _ in range(size)]

    def is_cell_empty(self, row: int, col: int) -> bool:
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col] is None
        return False

    def place_mark(self, row: int, col: int, symbol: Symbol) -> bool:
        if self.is_cell_empty(row, col):
            self.grid[row][col] = symbol
            return True
        return False

    def get_cell(self, row: int, col: int) -> Optional[Symbol]:
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None

    def display(self) -> None:
        n = self.size
        def cell_str(r, c):
            s = self.grid[r][c]
            return s.get_mark() if s is not None else ' '
        sep = "---+" * (n - 1) + "---" if n > 0 else ""
        for r in range(n):
            row_marks = " | ".join(cell_str(r, c) for c in range(n))
            print(" " + row_marks)
            if r < n - 1:
                print(sep)
        print()  # blank line


class GameType(Enum):
    STANDARD = 1


class Game:
    def __init__(self, board: Board, rules: Rules):
        self.board = board
        self.rules = rules
        self.players: List[Player] = []
        self.observers: List[IObserver] = []
        self.game_over: bool = False
        self.current_index: int = 0

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def add_observer(self, obs: IObserver) -> None:
        self.observers.append(obs)

    def notify(self, msg: str) -> None:
        for o in self.observers:
            o.update(msg)

    def switch_turn(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.players)

    def current_player(self) -> Player:
        return self.players[self.current_index]

    def play(self) -> None:
        if len(self.players) < 2:
            raise ValueError("Need at least two players to play")

        self.game_over = False
        self.current_index = 0
        self.notify("Game started!")
        self.board.display()

        while not self.game_over:
            player = self.current_player()
            self.notify(f"{player.name}'s turn ({player.symbol.get_mark()})")

            # read move from console safely
            move = self.read_move(player)
            if move is None:
                # in case of ctrl-c or abort, break
                self.notify("Game aborted.")
                break
            r, c = move

            if not self.rules.is_valid_move(self.board, r, c):
                self.notify("Invalid move. Try again.")
                continue

            self.board.place_mark(r, c, player.symbol)
            self.board.display()

            # check for win
            if self.rules.check_win(self.board, player.symbol):
                self.notify(f"Player {player.name} ({player.symbol.get_mark()}) wins!")
                player.score += 1
                self.game_over = True
                break

            # check draw
            if self.rules.check_draw(self.board):
                self.notify("Game is a draw.")
                self.game_over = True
                break

            # continue
            self.switch_turn()

    def read_move(self, player: Player) -> Optional[Tuple[int, int]]:
        """
        Ask player for a move in format 'row col' with 1-based indexing.
        Returns (row0based, col0based) or None if input EOF.
        """
        n = self.board.size
        prompt = f"Enter move for {player.name} as 'row col' (1-{n}): "
        while True:
            try:
                s = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                return None
            if not s:
                print("Please enter a move.")
                continue
            parts = s.split()
            if len(parts) != 2:
                print("Enter two numbers: row and column.")
                continue
            try:
                r = int(parts[0]) - 1
                c = int(parts[1]) - 1
            except ValueError:
                print("Please enter valid integers.")
                continue
            if not (0 <= r < n and 0 <= c < n):
                print(f"Row and column must be between 1 and {n}.")
                continue
            return r, c


class GameFactory:
    @staticmethod
    def create_game(game_type: GameType = GameType.STANDARD, size: int = 3) -> Game:
        if game_type == GameType.STANDARD:
            board = Board(size=size)
            rules = StandardRules()
            return Game(board, rules)
        else:
            raise ValueError("Unknown game type")


def tictactoe():
    print("Welcome to Tic-Tac-Toe (console).")
    size = 3
    while True:
        try:
            s = input("Board size (default 3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return
        if s == "":
            size = 3
            break
        try:
            size_val = int(s)
            if size_val < 3:
                print("Please choose size >= 3.")
                continue
            size = size_val
            break
        except ValueError:
            print("Enter an integer or blank for default.")

    game = GameFactory.create_game(GameType.STANDARD, size=size)
    notifier = ConsoleNotifier()
    game.add_observer(notifier)

    # get player names
    p1_name = input("Enter name for Player 1 (X): ").strip() or "Player1"
    p2_name = input("Enter name for Player 2 (O): ").strip() or "Player2"

    p1 = Player(id=1, name=p1_name, symbol=Symbol("X"))
    p2 = Player(id=2, name=p2_name, symbol=Symbol("O"))
    game.add_player(p1)
    game.add_player(p2)

    # Play loop - allow rematches
    while True:
        # reset board
        game.board = Board(size=size)
        game.game_over = False
        game.current_index = 0
        game.play()

        ans = input("Play again? (y/n): ").strip().lower()
        if ans != 'y':
            print("Final scores:")
            for pl in game.players:
                print(f"{pl.name}: {pl.score}")
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    tictactoe()
