class TicTacToeBot:
    def __init__(self, player_mark, opponent_mark, board) -> None:
        self.player_mark = player_mark
        self.opponent_mark = opponent_mark
        self.board = board

    def check_rows(self, mark):
        for idx in range(3):
            col_idx = None
            if "-" in self.board[idx]:
                if self.board[idx].count(mark) == 2:
                    col_idx = self.board[idx].index("-")
                    return idx, col_idx

    def check_columns(self, mark):
        for col_idx in range(3):
            row = []
            for row_idx in range(3):
                row.append(self.board[row_idx][col_idx])
            if "-" in row:
                if row.count(mark) == 2:
                    return row.index("-"), col_idx

    def check_slants(self, mark):
        row_from_left = [self.board[i][i] for i in range(3)]
        row_from_right = [self.board[i][2 - i] for i in range(3)]

        if row_from_left.count(mark) == 2 and "-" in row_from_left:
            return row_from_left.index("-"), row_from_left.index("-")

        if row_from_right.count(mark) == 2 and "-" in row_from_right:
            if row_from_right.index("-") == 0:
                return 0, 2
            if row_from_right.index("-") == 2:
                return 2, 0
            else:
                return 1, 1

    def check_center(self):
        if self.board[1][1] == "-":
            return (1, 1)

    def check_corners(self, mark):
        if self.board[0][0] == mark and self.board[2][2] == "-":
            return (2, 2)
        elif self.board[0][2] == mark and self.board[2][0] == "-":
            return (2, 0)
        elif self.board[2][2] == mark and self.board[0][0] == "-":
            return (0, 0)
        elif self.board[2][0] == mark and self.board[0][2] == "-":
            return (0, 2)

    def check_first_free(self):
        locations = []
        for idx_row in range(3):
            for idx_col in range(3):
                if self.board[idx_row][idx_col] == "-":
                    locations.append((idx_row, idx_col))
        
        import random
        return random.choice(locations)

    def main(
        self,
    ):
        # win req
        if self.check_rows(self.player_mark) != None:
            return self.check_rows(self.player_mark)

        if self.check_columns(self.player_mark) != None:
            return self.check_columns(self.player_mark)

        if self.check_slants(self.player_mark) != None:
            return self.check_slants(self.player_mark)

        if self.check_rows(self.opponent_mark) != None:
            return self.check_rows(self.opponent_mark)

        if self.check_columns(self.opponent_mark) != None:
            return self.check_columns(self.opponent_mark)

        if self.check_slants(self.opponent_mark) != None:
            return self.check_slants(self.opponent_mark)

        if self.check_center() != None:
            return self.check_center()

        if self.check_corners(self.opponent_mark) != None:
            return self.check_corners(self.opponent_mark)

        if self.check_first_free() != None:
            return self.check_first_free()
