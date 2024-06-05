from tkinter import messagebox

class Piece:
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king

    def make_king(self):
        self.is_king = True

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            if row % 2 == 0:
                start_col = 1
            else:
                start_col = 0
            for col in range(start_col, 8, 2):
                if row < 3:
                    board[row][col] = Piece('black')
                elif row > 4:
                    board[row][col] = Piece('white')
        return board

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece
        if (piece.color == 'white' and to_row == 0) or (piece.color == 'black' and to_row == 7):
            piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def count_pieces(self, color):
        count = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    count += 1
        return count

    def get_all_pieces(self, color):
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append((row, col))
        return pieces

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'
        self.must_capture = False

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        piece = self.board.get_piece(from_row, from_col)
        target = self.board.get_piece(to_row, to_col)

        if piece is None or piece.color != self.current_turn:
            return False
        if target is not None:
            return False

        if piece.is_king:
            # Check for king's move (diagonal move any distance)
            if abs(to_row - from_row) == abs(to_col - from_col):
                step_row = 1 if to_row > from_row else -1
                step_col = 1 if to_col > from_col else -1

                i, j = from_row + step_row, from_col + step_col
                opponent_pieces_count = 0

                while i != to_row and j != to_col:
                    current_piece = self.board.get_piece(i, j)
                    if current_piece:
                        if current_piece.color == piece.color:
                            return False
                        else:
                            opponent_pieces_count += 1
                            if opponent_pieces_count > 1:
                                return False
                    i += step_row
                    j += step_col
                return True if opponent_pieces_count == 1 or opponent_pieces_count == 0 else False
            return False
        else:
            # Logic for non-king pieces
            direction = -1 if piece.color == 'white' else 1
            if to_row - from_row == direction and abs(to_col - from_col) == 1:  # ordinary move
                return True

            if abs(to_row - from_row) == 2 and abs(to_col - from_col) == 2:  # capture move
                middle_row = (from_row + to_row) // 2
                middle_col = (from_col + to_col) // 2
                middle_piece = self.board.get_piece(middle_row, middle_col)
                if middle_piece and middle_piece.color != piece.color:
                    return True

            if piece.is_king and abs(to_row - from_row) > 2:
                step_row = 1 if to_row > from_row else -1
                step_col = 1 if to_col > from_col else -1

                i, j = from_row + step_row, from_col + step_col
                while i != to_row and j != to_col:
                    if self.board.get_piece(i, j):
                        return False
                    i += step_row
                    j += step_col
                return True
        return False

    def has_valid_capture(self, row, col):
        piece = self.board.get_piece(row, col)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.is_king:
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                    if self.board.get_piece(r, c) and self.board.get_piece(r, c).color != piece.color:
                        if self.board.get_piece(r + dr, c + dc) is None:
                            return True
                    r += dr
                    c += dc
        else:
            direction = -1 if piece.color == 'white' else 1
            for dr, dc in directions:
                if 0 <= row + 2 * dr < 8 and 0 <= col + 2 * dc < 8:
                    if self.board.get_piece(row + dr, col + dc) and self.board.get_piece(row + dr,
                                                                                         col + dc).color != piece.color:
                        if self.board.get_piece(row + 2 * dr, col + 2 * dc) is None:
                            return True
        return False

    def must_capture_exists(self):
        pieces = self.board.get_all_pieces(self.current_turn)
        for row, col in pieces:
            if self.has_valid_capture(row, col):
                return True
        return False

    def make_move(self, from_row, from_col, to_row, to_col):
        if self.is_valid_move(from_row, from_col, to_row, to_col):
            piece = self.board.get_piece(from_row, from_col)
            self.board.move_piece(from_row, from_col, to_row, to_col)

            if abs(to_row - from_row) == 2 and abs(to_col - from_col) == 2:
                middle_row = (from_row + to_row) // 2
                middle_col = (from_col + to_col) // 2
                self.board.board[middle_row][middle_col] = None
                self.must_capture = self.has_valid_capture(to_row, to_col)
                if not self.must_capture:
                    self.switch_turn()
            elif piece.is_king and abs(to_row - from_row) > 2:
                step_row = 1 if to_row > from_row else -1
                step_col = 1 if to_col > from_col else -1

                i, j = from_row + step_row, from_col + step_col
                while i != to_row and j != to_col:
                    if self.board.get_piece(i, j):
                        self.board.board[i][j] = None
                    i += step_row
                    j += step_col
                self.must_capture = self.has_valid_capture(to_row, to_col)
                if not self.must_capture:
                    self.switch_turn()
            else:
                self.switch_turn()

            if self.check_winner():
                self.end_game()
            return True
        return False

    def check_winner(self):
        white_pieces = self.board.count_pieces('white')
        black_pieces = self.board.count_pieces('black')
        return white_pieces == 0 or black_pieces == 0

    def end_game(self):
        winner = 'Black' if self.current_turn == 'white' else 'White'
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.board = Board()
        self.current_turn = 'white'
        self.must_capture = False

    def restart_game(self):
        self.board = Board()
        self.current_turn = 'white'
        self.must_capture = False