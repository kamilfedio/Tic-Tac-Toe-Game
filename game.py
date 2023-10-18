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
        if column not in self.rows_indexes:
            column = self.columns_indexes.index(column)
        else:
            column = int(column)
        if self.board[row][column] == "-":
            self.board[row][column] = player
            return True
        else:
            return False

    # check rows if win
    def check(self, board, player):
        for row in board:
            if row.count(player) == 3:
                return True

    # check if win
    def check_win(self, player):
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "-":
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "-":
            return True

        reversed_board = [
            [self.board[col][row] for col in range(3)] for row in range(3)
        ]

        return self.check(self.board, player) or self.check(reversed_board, player)

    def check_if_draw(self):
        for row in self.board:
            if row.count("-") > 0:
                return False

        return True

    # reset board
    def clear_board(self):
        self.board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]


class Player:
    def __init__(self, name, is_ai=False) -> None:
        self.name = name
        self.wins = 0
        self.loses = 0
        self.draws = 0
        self.used_marks = []
        self.is_ai = is_ai

    def __repr__(self):
        return f"{self.name} | {self.wins}W/{self.draws}D/{self.loses}L | {', '.join(self.used_marks)}"


class Game:
    import random

    players = []

    def __init__(self, name_one="Player 1", name_two="Player 2"):
        # init players
        self.player_one = Player(name_one)
        self.player_two = Player(name_two, is_ai=True)
        self.players.extend([self.player_one, self.player_two])

        # init board
        self.board = Board()

    def change_marks(self):
        self.player_one.used_marks.append(self.random.choice(["x", "0"]))
        if self.player_one.used_marks[-1] == "0":
            self.player_two.used_marks.append("x")
        else:
            self.player_two.used_marks.append("0")

    def ai_play(self, mark, board):
        from adding_ai import Ai

        if mark == "x":
            opponent_mark = "0"
        else:
            opponent_mark = "x"
        ai = Ai(mark, opponent_mark, board)
        return ai.main()

    def play(self):
        import os

        while True:
            round_idx = 0
            self.change_marks()
            queue = self.random.sample(self.players, k=2)
            print("\n" + "-" * 20, "START", "-" * 20)

            while True:
                if queue[round_idx].name == self.player_one.name:
                    print(
                        f"{self.player_one.name} - {self.player_one.used_marks[-1]}",
                        "<",
                    )
                    print(
                        f"{self.player_two.name} - {self.player_two.used_marks[-1]}\n"
                    )
                else:
                    print(f"{self.player_one.name} - {self.player_one.used_marks[-1]}")
                    print(
                        f"{self.player_two.name} - {self.player_two.used_marks[-1]}",
                        "<\n",
                    )

                self.board.display_board()

                while True:
                    if queue[round_idx].is_ai:
                        res = self.ai_play(
                            queue[round_idx].used_marks[-1], self.board.board
                        )
                        self.board.update_board(
                            str(res[1]), str(res[0]), queue[round_idx].used_marks[-1]
                        )
                        break

                    user_input = input("Enter place: ")

                    if (
                        user_input[0].lower() in "abc"
                        and user_input[1].lower() in "012"
                    ):
                        if self.board.update_board(
                            user_input[0].lower(),
                            user_input[1].lower(),
                            queue[round_idx].used_marks[-1],
                        ):
                            self.board.update_board(
                                user_input[0].lower(),
                                user_input[1].lower(),
                                queue[round_idx].used_marks[-1],
                            )
                            break
                    print("[ERROR] You entered wrong place name")

                os.system("cls")

                if self.board.check_if_draw():
                    print("Draw")
                    self.player_one.draws += 1
                    self.player_two.draws += 1
                    break

                if self.board.check_win(queue[round_idx].used_marks[-1]):
                    print(f"{queue[round_idx].name} is winner")
                    self.board.display_board()

                    if queue[round_idx].name == self.player_one.name:
                        self.player_one.wins += 1
                        self.player_two.loses += 1
                    else:
                        self.player_one.loses += 1
                        self.player_two.wins += 1

                    break

                if round_idx == 0:
                    round_idx = 1
                else:
                    round_idx = 0

            print("\n" + "*" * 20, "SCOREBOARD", "*" * 20)
            print(self.player_one)
            print(self.player_two)
            user_dec = input("\n\nDo you want to play next? [y/n]: ")
            if user_dec == "y":
                self.board.clear_board()
                os.system("cls")
                continue
            else:
                break


if __name__ == "__main__":
    game = Game()
    game.play()
