import tkinter as tk
from tkinter import font
from itertools import cycle
from typing import NamedTuple

# Define Constants
BOARD_SIZE = 3
DEFAULT_PLAYERS = [
    {"label": "X", "color": "blue"},
    {"label": "O", "color": "green"},
]

# Define Player and Move
class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int

# Tic Tac Toe Board
class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_board_display()
        self._create_game_board()
        self._create_play_again_button()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Player X's Turn",
            font=font.Font(size=24, weight="bold"),
            fg="green",
        )
        self.display.pack()

    def _create_game_board(self):
        board_frame = tk.Frame(master=self)
        board_frame.pack()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                button = tk.Button(
                    master=board_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    width=5,
                    height=2,
                    bg="white",
                    command=lambda row=row, col=col: self._handle_click(row, col),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                self._cells[(row, col)] = button

    def _handle_click(self, row, col):
        if self._game._has_winner or self._game._current_moves[row][col] is not None:
            return
        button = self._cells[(row, col)]
        button.config(
            text=self._game.current_player.label,
            fg=self._game.current_player.color,
        )
        self._game._current_moves[row][col] = self._game.current_player
        if self._game._check_winner():
            self.display.config(
                text=f'Player "{self._game.current_player.label}" won!',
                fg=self._game.current_player.color,
            )
            self._highlight_winner()
        elif not any(None in row for row in self._game._current_moves):
            self.display.config(text="It's a Tie!", fg="red")
        else:
            self._game.current_player = next(self._game._players)
            self.display.config(
                text=f"Player {self._game.current_player.label}'s Turn",
                fg=self._game.current_player.color,
            )

    def _highlight_winner(self):
        for row, col in self._game.winner_combo:
            button = self._cells[(row, col)]
            button.config(bg="lightgreen")

    def _create_play_again_button(self):
        """Add a Play Again button below the game board."""
        play_again_frame = tk.Frame(master=self)
        play_again_frame.pack(pady=10)
        play_again_button = tk.Button(
            master=play_again_frame,
            text="Play Again",
            font=font.Font(size=16, weight="bold"),
            bg="lightgray",
            command=self._reset_game,
        )
        play_again_button.pack()

    def _reset_game(self):
        """Reset the game to its initial state."""
        self._game.reset()
        for button in self._cells.values():
            button.config(text="", bg="white")
        self.display.config(text="Player X's Turn", fg="green")

# Tic Tac Toe Game Logic
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle([Player(**player) for player in players])
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = [[None] * board_size for _ in range(board_size)]
        self._has_winner = False
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(r, c) for c in range(self.board_size)] for r in range(self.board_size)]
        cols = [[(r, c) for r in range(self.board_size)] for c in range(self.board_size)]
        diag1 = [(i, i) for i in range(self.board_size)]
        diag2 = [(i, self.board_size - i - 1) for i in range(self.board_size)]
        return rows + cols + [diag1, diag2]

    def _check_winner(self):
        for combo in self._winning_combos:
            marks = {self._current_moves[r][c] for r, c in combo}
            if len(marks) == 1 and None not in marks:
                self.winner_combo = combo
                self._has_winner = True
                return True
        return False

    def reset(self):
        """Reset game state."""
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = [[None] * self.board_size for _ in range(self.board_size)]
        self._has_winner = False

# Run the Game
if __name__ == "__main__":
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()
