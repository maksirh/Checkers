import tkinter as tk



class InfoPanel:
    def __init__(self, root, game, gui):
        self.root = root
        self.game = game
        self.gui = gui
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.Y)
        self.current_turn_label = tk.Label(self.frame, text="Current Turn: White")
        self.current_turn_label.pack(side=tk.TOP, expand=True, anchor="center")

        # Add restart button
        self.restart_button = tk.Button(self.frame, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.surrender_button = tk.Button(self.frame, text="Surrender", command=self.surrender_game)
        self.surrender_button.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def restart_game(self):
        self.game.restart_game()
        self.gui.draw_board()  # Redraw the board after restarting the game
        self.update()

    def surrender_game(self):
        self.game.end_game()

    def update(self):
        current_turn = "White" if self.game.current_turn == 'white' else "Black"
        self.current_turn_label.config(text=f"Current Turn: {current_turn}")


class CheckersGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.panel_frame = tk.Frame(root)
        self.panel_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.info_panel = InfoPanel(self.panel_frame, game, self)
        self.info_panel.frame.pack(side=tk.TOP, fill=tk.X)
        self.board_frame = tk.Frame(root)
        self.board_frame.pack()
        self.canvas = tk.Canvas(self.board_frame, width=800, height=800)
        self.canvas.pack(anchor="center")
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
        self.info_panel.update()
