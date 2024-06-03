import tkinter as tk


class CheckersGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()
        self.selected_piece_outline = None
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(col * 100, row * 100, (col + 1) * 100, (row + 1) * 100, fill=color)
                piece = self.game.board.get_piece(row, col)
                if piece:
                    self.draw_piece(row, col, piece)

    def draw_piece(self, row, col, piece):
        x = col * 100 + 50
        y = row * 100 + 50
        color = 'black' if piece.color == 'black' else 'white'
        self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill=color)
        if piece.is_king:
            self.canvas.create_text(x, y, text='K', fill='gold', font=('Arial', 24))

    def highlight_piece(self, row, col):
        if self.selected_piece_outline:
            self.canvas.delete(self.selected_piece_outline)
        self.selected_piece_outline = self.canvas.create_rectangle(col * 100, row * 100, (col + 1) * 100,
                                                                   (row + 1) * 100, outline="red", width=3)

    def clear_highlight(self):
        if self.selected_piece_outline:
            self.canvas.delete(self.selected_piece_outline)
            self.selected_piece_outline = None

    def update(self):
        self.draw_board()
