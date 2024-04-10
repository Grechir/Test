from art import tprint

field = [[" "] * 3 for i in range(3)]


def greets():
    print("=" * 86)
    tprint("Tick - Tack - Toe")
    print("""        Game Rules:
        1) The first player goes with X, second player goes with O. 
        2) These symbols will be placed on the table, in an attempt 
        to have three of them in a row.
        3) The first player to draw three of their symbols in a row, 
        whether it is horizontal, vertical, or diagonal, has won tic-tac-toe.
        4) Enter your symbols in a console according to the coordinates 
        of the field. For example, to put your symbol in the center of 
        the field, you need to enter - 1 1, separated by a space. 
        It looks like:
                Your turn: 1 1 
    """)
    new_game()


def print_field():
    print("   | 0 | 1 | 2 |")
    for i, row in enumerate(field):  # the object index (i) the object (row)
        stroke = f" {i} | {" | ".join(row)} | "
        print("-" * 16)
        print(stroke)
    print("-" * 16)


def player_step():
    while True:
        try:
            x, y = map(int, input("     Your turn: ").split())
            if x in range(3) and y in range(3):
                if field[x][y] == " ":
                    return x, y
                else:
                    print("the cell is occupied")
            else:
                print("the cell is out of range")
        except ValueError:
            print("Invalid number of arguments. Enter 2 arguments.")


def field_step(player):
    x, y = player_step()
    if player == "X":
        field[x][y] = "X"
    else:
        field[x][y] = "O"
    return field[x][y]


def win_check():
    all_wins = [
        ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
        ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
        ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))
            ]
    for win in all_wins:
        symbol_row = []
        for i in win:
            symbol_row.append(field[i[0]][i[1]])
        if symbol_row == ["X", "X", "X"]:
            print_field()
            print("The winner is - X!")
            return True
        if symbol_row == ["O", "O", "O"]:
            print_field()
            print("The winner is - O!")
            return True
    return False


def new_game():
    global field
    ask = input("Press Enter to start a new game: ")
    while True:
        if ask == "":
            field = [[" "] * 3 for i in range(3)]
            break
        else:
            ask = input("Press Enter to start a new game: ")
    print("=" * 86)
    print()


def main():
    greets()
    count = 0
    while True:
        print_field()
        count += 1
        if count % 2 == 1:
            print("         X")
            field_step("X")
        else:
            print("         O")
            field_step("O")

        if win_check():
            count = 0
            new_game()

        if count == 9:
            print_field()
            print("Draw")
            count = 0
            new_game()


if __name__ == "__main__":
    main()
