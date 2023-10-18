class Board:
    # rows & columns
    rows_indexes = ["0", "1", "2"]
    columns_indexes = ["a", "b", "c"]

    # board
    def __init__(self) -> None:
        self.clear_board()

    # printing board
    def display_board(self):
        print("\ A B C")
        for idx, line in enumerate(self.board):
            print(self.rows_indexes[idx], "|".join(line))

    # updating board after move
    def update_board(self, column, row, player):
        row = self.rows_indexes.index(row)
        column = self.columns_indexes.index(column)
        if self.board[row][column] == "-":
            self.board[row][column] = player
            return True
        else:
            return False

    def clear_board(self):
        self.board = [
            ["0", "0", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ]


class Ai:
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

        if row_from_left.count(mark) == 2:
            try:
                return row_from_left.index("-"), row_from_left.index("-")
            except:
                return None

        if row_from_right.count(mark) == 2:
            try:
                if row_from_right.index("-") == 0:
                    return 0, 2
            except:
                try:
                    if row_from_right.index("-") == 2:
                        return 2, 0
                except:
                    try:
                        return 1, 1
                    except:
                        return None

    def check_center(self):
        if self.board[1][1] == "-":
            return (1, 1)

    def check_corners(self, mark):
        if self.board[0][0] == mark:
            return (2, 2)
        elif self.board[0][2] == mark:
            return (2, 0)
        elif self.board[2][2] == mark:
            return (0, 0)
        elif self.board[2][0] == mark:
            return (0, 2)

    def check_first_free(self):
        for idx_row in range(3):
            for idx_col in range(3):
                if self.board[idx_row][idx_col] == "-":
                    return (idx_row, idx_col)

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
