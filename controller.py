import tkinter as tk

from model import Game
from view import CheckersGUI


class CheckersController:
    def __init__(self, game, view):
        self.game = game
        self.view = view
        self.selected_piece = None
        self.view.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        row, col = event.y // 100, event.x // 100
        if self.selected_piece:
            from_row, from_col = self.selected_piece
            if self.game.make_move(from_row, from_col, row, col):
                if self.game.must_capture:
                    self.selected_piece = (row, col)
                    self.view.highlight_piece(row, col)
                else:
                    self.selected_piece = None
                    self.view.clear_highlight()
                    self.view.update()
            else:
                self.selected_piece = None
                self.view.clear_highlight()
        else:
            piece = self.game.board.get_piece(row, col)
            if piece and piece.color == self.game.current_turn:
                if self.game.must_capture_exists() and not self.game.has_valid_capture(row, col):
                    self.selected_piece = None
                    self.view.clear_highlight()
                else:
                    self.selected_piece = (row, col)
                    self.view.highlight_piece(row, col)
            else:
                self.selected_piece = None
                self.view.clear_highlight()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game()
    view = CheckersGUI(root, game)
    controller = CheckersController(game, view)
    root.mainloop()
