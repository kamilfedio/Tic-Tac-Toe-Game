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
    def __init__(self, name="Player", is_bot=False) -> None:
        self.name = name
        self.wins = 0
        self.loses = 0
        self.draws = 0
        self.used_marks = []
        self.is_bot = is_bot

    def __repr__(self):
        return f"{self.name} {'[bot]' if self.is_bot else ''} | {self.wins}W/{self.draws}D/{self.loses}L | {', '.join(self.used_marks[:-1])}"


class Game:
    import random

    players = []

    def __init__(self):
        # init players
        self.player_one = Player()
        self.player_two = Player()
        self.players.extend([self.player_one, self.player_two])

        # init board
        self.board = Board()

        # settings
        self.automate_game: bool = True  # True/False
        self.player_one.name: str = "Player 1"  # custom player name
        self.player_two.name: str = "Player 2"  # custom player name
        self.player_one.is_bot: bool = True  # True/False
        self.player_two.is_bot: bool = True  # True/False
        self.to_win: int = 5  # count of wins to end game if automate_game is True

    def change_marks(self):
        self.player_one.used_marks.append(self.random.choice(["x", "0"]))
        if self.player_one.used_marks[-1] == "0":
            self.player_two.used_marks.append("x")
        else:
            self.player_two.used_marks.append("0")

    def bot_play(self, mark, board):
        from bot import TicTacToeBot

        if mark == "x":
            opponent_mark = "0"
        else:
            opponent_mark = "x"
        tic_tac_toe_bot = TicTacToeBot(mark, opponent_mark, board)
        return tic_tac_toe_bot.main()

    def show_scoreboard(self):
        print(self.player_one)
        print(self.player_two)
        print()

    def continue_playing(self):
        import os
        import time

        if self.automate_game:
            if max(self.player_one.wins, self.player_two.wins) == self.to_win:
                os.system("cls")
                print("Winner")
                self.show_scoreboard()
                return False

            time.sleep(1)
            os.system("cls")
            self.board.clear_board()
            return True

        if not self.automate_game:
            user_dec = input("\n\nDo you want to play next? [y/n]: ")
            if user_dec == "y":
                self.board.clear_board()
                os.system("cls")
                return True
            else:
                return False

    def play(self):
        import os
        import time

        while True:
            os.system("cls")
            round_idx = 0
            self.change_marks()
            queue = self.random.sample(self.players, k=2)

            while True:
                self.show_scoreboard()
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

                while True:
                    if queue[round_idx].is_bot:
                        res = self.bot_play(
                            queue[round_idx].used_marks[-1], self.board.board
                        )
                        self.board.update_board(
                            str(res[1]), str(res[0]), queue[round_idx].used_marks[-1]
                        )
                        self.board.display_board()
                        time.sleep(1)
                        break

                    self.board.display_board()

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
                    self.player_one.draws += 1
                    self.player_two.draws += 1
                    self.show_scoreboard()

                    print("Draw\n\n")
                    self.board.display_board()
                    time.sleep(1)
                    break

                if self.board.check_win(queue[round_idx].used_marks[-1]):
                    if queue[round_idx].name == self.player_one.name:
                        self.player_one.wins += 1
                        self.player_two.loses += 1
                    else:
                        self.player_one.loses += 1
                        self.player_two.wins += 1

                    self.show_scoreboard()
                    print(f"{queue[round_idx].name} is winner\n\n")

                    self.board.display_board()

                    break

                if round_idx == 0:
                    round_idx = 1
                else:
                    round_idx = 0

            if not self.continue_playing():
                break


if __name__ == "__main__":
    game = Game()
    game.play()

### 88-94 line - settings
