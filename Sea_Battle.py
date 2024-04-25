from random import randint
from art import tprint
import colorama as clr


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # метод для удобного сравнения
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # метод для представления точки в виде строки (похож на __str__)
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, length, orient):
        self.bow = bow  # это Dot(x, y)
        self.length = length
        self.orient = orient
        self.lives = length  # корабль состоит из n-го кол-ва клеток, которое определяется длиной корабля

    @property
    def dots(self):
        ship_dots = []  # здесь будет собран корабль по клеткам
        for i in range(self.length):
            cur_x = self.bow.x  # где bow.x и bow.y это Dot(x, y).x/y соответственно
            cur_y = self.bow.y

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def hit(self, shot):
        return shot in self.dots  # если попал в корабль, то выводится True, иначе False


class Board:
    def __init__(self, hide=False, size=6):
        self.size = size
        self.hide = hide
        self.count = 0

        self.field = [["0"] * size for _ in range(size)]  # "~" типа волна, мыж на море
        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):  # the object index (i) the object (row)
            res += f"\n{i+1} | {" | ".join(row)} |"

        if self.hide:
            res = res.replace(clr.Fore.GREEN + "■" + clr.Style.RESET_ALL, "0")
        return res

    def out_of_field(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:  # dots это список с кораблем
            for dot_x, dot_y in near:
                cur = Dot(dot.x + dot_x, dot.y + dot_y)  # изменение точки на значения из near
                if not (self.out_of_field(cur)) and cur not in self.busy:
                    if verb:  # если видимая клетка (она будет видимой при попадании в корабль)
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out_of_field(dot) or dot in self.busy:
                raise BoardWrongShipException()  # вызывается исключение
        for dot in ship.dots:
            self.field[dot.x][dot.y] = clr.Fore.GREEN + "■" + clr.Style.RESET_ALL
            self.busy.append(dot)

        self.ships.append(ship)  # корабль добавляется в список кораблей
        self.contour(ship)  # и "обводится" контуром

    def shot(self, dot):
        if self.out_of_field(dot):  # если за пределами доски, вызываем соответствующее исключение
            raise BoardOutException

        if dot in self.busy:  # если клетка занята, вызываем соответствующее исключение
            raise BoardUsedException

        self.busy.append(dot)  # в начале хода сразу добавляем точку в занятые, после чего:

        for ship in self.ships:
            if dot in ship.dots:  # для каждой точки корабля при попадании
                ship.lives -= 1
                self.field[dot.x][dot.y] = clr.Fore.RED + "X" + clr.Style.RESET_ALL
                # минус жизнь и ставится Х на корабле
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    # если корабль был уничтожен это все равно произошло в результате успешного попадания,
                    # следовательно, выводим True
                    return True
                else:
                    print("Корабль ранен!")
                    # успешное попадание - выводим True
                    return True

        self.field[dot.x][dot.y] = "."
        print("Промах!")
        # в случаях промаха ход передается оппоненту, поэтому выводим - False
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:  # бесконечный цикл
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):

        dot = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {dot.x + 1}, {dot.y + 1}")  # +1 здесь для того, чтобы точка совпала с полем.
        # поле пронумеровано в интерфейсе с 1, а по факту нумерация начинается с 0.
        return dot


class User(Player):
    def ask(self):
        while True:
            try:
                x, y = map(int, input("     Ваш ход: ").split())
                return Dot(x - 1, y - 1)
            except ValueError:
                print("Введите 2 числовых аргумента.")


class Game:
    def __init__(self, size=6):
        self.size = size
        player_board = self.random_board()
        computer_board = self.random_board()
        computer_board.hide = True

        self.AI = AI(computer_board, player_board)
        self.User = User(player_board, computer_board)

    @staticmethod
    def greets():
        print("=" * 87)
        tprint("Battleship Game")
        print("""   Правила игры:
        1) Игроки по очереди делают "выстрел", выбирая координату на поле
        2) Игрок, который «ранил» или «убил» корабль оппонента, 
        получает право сделать еще один ход — и так до тех пор, 
        пока он не промахнется. После этого очередь «стрелять» 
        переходит к другому игроку.
        3) Партию выигрывает тот игрок, который первым уничтожит 
        все корабли врага.
        4) поле 6 на 6 клеток, корабли расставляются в случайном
        порядке: один 3-х палубный, два 2-х палубных, четыре 4-х палубных.
        5) Введите выбранные координаты поля (к примеру - 1 2) в консоли, где:
        первое число (1) - номер строки, второе (2) - номер столбца, разделенные пробелом 
        Это выглядит так:
                Ваш ход: 1 2
        """)

    def board_try(self):
        all_ship_lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for ship_len in all_ship_lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), ship_len, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.board_try()
        return board

    def players_board_type(self):
        print("-" * 27)
        print("Доска пользователя:")
        print(self.User.board)
        print("-" * 27)
        print("Доска компьютера:")
        print(self.AI.board)
        print("-" * 27)

    def loop(self):
        step_count = 0
        while True:
            self.players_board_type()
            if step_count % 2 == 0:
                print("Ходит Пользователь!")
                repeat = self.User.move()
            else:
                print("Ходит компьютер!")
                repeat = self.AI.move()
            if repeat:
                step_count -= 1

            if self.AI.board.count == 7:
                self.players_board_type()
                print("Ура, Вы умнее, чем компьютер!")
                break

            if self.User.board.count == 7:
                self.players_board_type()
                print("ха-ха-ха, я умнее тебя, у меня памяти 16 мегабайт!")
                break

            step_count += 1

    def start(self):
        self.greets()

        ask = input("Нажмите Enter для начала новой игры: ")
        while True:
            print("=" * 87)
            if ask == "":
                self.loop()
                break
            else:
                ask = input("Нажмите Enter для начала игры: ")
        print()


# классы исключений ---------------------------------------------------------------------


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы не можете стрелять за пределы игровой доски!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class BoardWrongShipException(BoardException):
    pass

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    game = Game()
    game.start()
