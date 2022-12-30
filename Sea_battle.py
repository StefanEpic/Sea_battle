import random


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'GlaDOS: Ты пыталась выстрелить за доску!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'GlaDOS: В эту клетку ты уже стреляла!'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, position, len_ship, horizontally):
        self.position = position
        self.len_ship = len_ship
        self.horizontally = horizontally
        self.health = len_ship

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.len_ship):
            cur_x = self.position.x
            cur_y = self.position.y

            if self.horizontally:
                cur_x += i

            elif not self.horizontally:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=10):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["_"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dot_x, dot_y in near:
                cur = Dot(dot.x + dot_x, dot.y + dot_y)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = '    ' + '   '.join([str(i) for i in range(self.size)])
        for i, row in enumerate(self.field):
            res += f"\n{i} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "_")
        return res

    def out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.health -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.health == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("GlaDOS: Корабль уничтожен!")
                    return False
                else:
                    print("GlaDOS: Корабль ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("GlaDOS: Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(random.randint(0, 9), random.randint(0, 9))
        print(f"GLaDOS: Мой ход: {dot.x} {dot.y}")
        return dot


class User(Player):
    def ask(self):
        while True:
            cords = input("GlaDOS: Твой ход: ").split()

            if len(cords) != 2:
                print("GlaDOS: Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("GlaDOS: Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x, y)


class Game:
    def __init__(self, size=10):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(random.randint(0, self.size), random.randint(0, self.size)), l, random.randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greetings(self):
        player_name = int(random.randint(100, 1000))
        print(f'\t\t┈┈┈☆☆☆☆☆☆☆┈┈┈')
        print(f'\t\t┈┈╭┻┻┻┻┻┻┻┻┻╮┈┈')
        print(f'\t\t┈┈┃╱╲╱╲╱╲╱╲╱┃┈┈')
        print(f'\t\t┈╭┻━━━━━━━━━┻╮┈')
        print(f'\t\t┈┃╱╲╱╲╱╲╱╲╱╲╱┃┈')
        print(f'\t\t┈┗━━━━━━━━━━━┛┈ ')
        print(f'\tGlaDOS: И снова рада видеть тебя, Испытуемая №{player_name}!')
        print(f'\tGlaDOS: В этом маленьком тесте GLaDOS проверит, насколько ты смышленая...')
        print()
        mode = input('\tGlaDOS: Поиграем? Правила помнишь? (+/-):')
        if mode == '-':
            print("\t-------------------")
            print("\t формат ввода: x y ")
            print("\t x - номер строки  ")
            print("\t y - номер столбца ")
            print("\t-------------------")
            input("\tGlaDOS: Жми любую клавишу, если готова...")

    def loop(self):
        num = 0
        while True:
            if num % 2 == 0:
                print("-" * 20)
                print("GlaDOS: Твое поле:")
                print(self.us.board)
                print("-" * 20)
                print("GlaDOS: Мое поле:")
                print(self.ai.board)
                print("-" * 20)
                print("GlaDOS: Ходи...")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("GlaDOS: Мой ход!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 10:
                print("-" * 20)
                print("GLaDOS: Молодец! Ты прошла испытание и заслужила тор+тик! 🎂")
                input("Нажмите любую клавишу для завершения...")
                break

            if self.us.board.count == 10:
                print("-" * 20)
                print("GlaDOS: Хех, это было просто!")
                input("Нажмите любую клавишу для завершения...")
                break
            num += 1

    def start(self):
        self.greetings()
        self.loop()


g = Game()
g.start()
