class Board:
    def __init__(self, rows=5, cols=5, win_length=4):
        self.rows = rows
        self.cols = cols
        self.win_length = win_length
        self.grid = [["" for _ in range(cols)] for _ in range(rows)]

    def make_move(self, row, col, player):
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True

    def undo_move(self, row, col):
        self.grid[row][col] = ""

    def is_valid_move(self, row, col):
        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
            and self.grid[row][col] == ""
        )

    def get_legal_moves(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == "":
                    moves.append((r, c))
        return moves

    def is_full(self):
        return len(self.get_legal_moves()) == 0

    def check_winner(self):
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal down-right
            (1, -1),  # diagonal down-left
        ]

        for r in range(self.rows):
            for c in range(self.cols):
                player = self.grid[r][c]

                if player == "":
                    continue

                for dr, dc in directions:
                    if self._check_direction(r, c, dr, dc, player):
                        return player

        return None

    def _check_direction(self, row, col, dr, dc, player):
        for i in range(self.win_length):
            r = row + dr * i
            c = col + dc * i

            if not (0 <= r < self.rows and 0 <= c < self.cols):
                return False

            if self.grid[r][c] != player:
                return False

        return True

    def print_board(self):
        for row in self.grid:
            print(row)
