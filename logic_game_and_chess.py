class Game:
    def __init__(self):
        self.chess_on_board = []
        self.color = 'Wt'
        self.new_game()

    def new_game(self):
        self.chess_on_board = [[None] * 10 for _ in range(10)]

        self.chess_on_board[1] = [
            Toat('Bl', 0, 1),
            Pawn('Bl', 1, 1),
            Pawn('Bl', 2, 1),
            Pawn('Bl', 3, 1),
            Pawn('Bl', 4, 1),
            Pawn('Bl', 5, 1),
            Pawn('Bl', 6, 1),
            Pawn('Bl', 7, 1),
            Pawn('Bl', 8, 1),
            Toat('Bl', 9, 1)
        ]

        self.chess_on_board[0] = [
            Warrior('Bl', 0, 0),
            PodDwar('Bl', 1, 0),
            Dwar('Bl', 2, 0),
            Pilot('Bl', 3, 0),
            Princess('Bl', 4, 0, 1),
            Leader('Bl', 5, 0),
            Pilot('Bl', 6, 0),
            Dwar('Bl', 7, 0),
            PodDwar('Bl', 8, 0),
            Warrior('Bl', 9, 0)
        ]

        self.chess_on_board[8] = [
            Toat('Wt', 0, 8),
            Pawn('Wt', 1, 8),
            Pawn('Wt', 2, 8),
            Pawn('Wt', 3, 8),
            Pawn('Wt', 4, 8),
            Pawn('Wt', 5, 8),
            Pawn('Wt', 6, 8),
            Pawn('Wt', 7, 8),
            Pawn('Wt', 8, 8),
            Toat('Wt', 9, 8)
        ]

        self.chess_on_board[9] = [
            Warrior('Wt', 0, 9),
            PodDwar('Wt', 1, 9),
            Dwar('Wt', 2, 9),
            Pilot('Wt', 3, 9),
            Leader('Wt', 4, 9),
            Princess('Wt', 5, 9, 1),
            Pilot('Wt', 6, 9),
            Dwar('Wt', 7, 9),
            PodDwar('Wt', 8, 9),
            Warrior('Wt', 9, 9)
        ]

        self.color = 'Wt'
        self.update()

    def draw_pc(self):
        s = ["```", "+----+----+----+----+----+----+----+----+----+----+"]
        for q, i in enumerate(self.chess_on_board):
            s1 = []
            for j in i:
                j1 = '|    '
                if j is not None:
                    j1 = '|' + j.look()
                s1.append(j1)
            s.append(''.join(s1) + '| ' + str(q + 1))
            s.append("+----+----+----+----+----+----+----+----+----+----+")
        s.append("  1    2    3    4    5    6    7    8    9    10")
        s.append("```")
        if self.color == 'Wt':
            cl = 'белых'
        else:
            cl = 'чёрных'
        s.append(f'Сейчас ход {cl}')
        return s

    def move_figure_helper(self, x_pos, y_pos, al):  # движение фигур по доске
        try:
            flag = False
            if self.chess_on_board[y_pos][x_pos] is not None:
                cl = self.chess_on_board[y_pos][x_pos].r_color()
                if cl == self.color:
                    flag = self.chess_on_board[y_pos][x_pos].move(al)
            if flag:
                if self.color == 'Wt':
                    self.color = 'Bl'
                else:
                    self.color = 'Wt'
            return flag
        except TypeError:
            return False

    def move_figure(self, x_pos, y_pos, al):
        flag = self.move_figure_helper(x_pos, y_pos, al)
        self.update()
        return flag

    def update(self):
        for y in self.chess_on_board:
            for x in y:
                if x is not None:
                    x.new_board(self.chess_on_board)


class Chess:  # сами фигуры
    def __init__(self, color, x, y):
        self.chess_on_board = []
        self.color = color
        self.x = x
        self.y = y

    def r_color(self):
        return self.color

    def new_board(self, chess_on_board):
        self.chess_on_board = chess_on_board

    def return_board(self):
        return self.chess_on_board


class Pawn(Chess):  # пешка
    def look(self):
        return f'Pn{self.color}'

    def move(self, al):
        x2, y2 = al[0], al[1]
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            cl = self.chess_on_board[y2][x2].r_color()
            if cl == self.color:
                return False

        if self.color == 'Wt':
            if self.y - 1 == y2 or y2 == self.y:
                if y2 == self.y and x2 != self.x and (self.x - 1 == x2 or x2 == self.x + 1):
                    c += 1
                elif self.x - 1 <= x2 <= self.x + 1:
                    c += 1
        else:
            if self.y == y2 or y2 == self.y + 1:
                if (self.x - 1 == x2 or x2 == self.x + 1) and self.y == y2 and x2 != self.x:
                    c += 1
                elif self.x - 1 <= x2 <= self.x + 1:
                    c += 1
        if c == 1:
            self.chess_on_board[y2][x2] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x2, y2
            return True
        return False


class Toat(Chess):  # тоат
    def look(self):
        return f'Tt{self.color}'

    def move(self, al):
        x2, y2, x3, y3 = al[0], al[1], al[2], al[3]
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            return False
        if self.chess_on_board[y3][x3] is not None:
            cl = self.chess_on_board[y3][x3].r_color()
            if cl == self.color:
                return False

        if abs(self.x - x2) == 0 and abs(self.y - y2) == 1:
            c = 2
        elif abs(self.x - x2) == 1 and abs(self.y - y2) == 0:
            c = 2
        elif abs(self.x - x2) == 1 and abs(self.y - y2) == 1:
            c = 1
        if c == 2:
            if abs(x2 - x3) == 1 and abs(y2 - y3) == 1:
                c += 1
        if c == 1:
            if abs(x2 - x3) == 0 and abs(y2 - y3) == 1:
                c += 2
            elif abs(x2 - x3) == 1 and abs(y2 - y3) == 0:
                c += 2

        if c == 3:
            self.chess_on_board[y3][x3] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x3, y3
            return True
        return False


class Warrior(Chess):  # воин
    def look(self):
        return f'Wa{self.color}'

    def move(self, al):
        x2, y2, x3, y3 = al[0], al[1], al[2], al[3]
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            return False
        if self.chess_on_board[y3][x3] is not None:
            cl = self.chess_on_board[y3][x3].r_color()
            if cl == self.color:
                return False

        if abs(self.x - x2) == 1 and abs(self.y - y2) == 0:
            c += 1
        elif abs(self.x - x2) == 0 and abs(self.y - y2) == 1:
            c += 1
        if c == 1:
            if abs(x2 - x3) == 1 and abs(y2 - y3) == 0:
                c += 1
            elif abs(x2 - x3) == 0 and abs(y2 - y3) == 1:
                c += 1

        if c == 2:
            self.chess_on_board[y3][x3] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x3, y3
            return True
        return False


class PodDwar(Chess):  # под-двар
    def look(self):
        return f'Pd{self.color}'

    def move(self, al):
        x2, y2, x3, y3 = al[0], al[1], al[2], al[3]
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            return False
        if self.chess_on_board[y3][x3] is not None:
            cl = self.chess_on_board[y3][x3].r_color()
            if cl == self.color:
                return False

        if abs(self.x - x2) == 1 and abs(self.y - y2) == 1:
            c += 1
        if c == 1:
            if abs(x2 - x3) == 1 and abs(y2 - y3) == 1:
                c += 1

        if c == 2:
            self.chess_on_board[y3][x3] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x3, y3
            return True
        return False


class Dwar(Chess):  # двар
    def look(self):
        return f'Dw{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = al[0], al[1], al[2], al[3], al[4], al[5]
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            return False
        if self.chess_on_board[y3][x3] is not None:
            return False
        if self.chess_on_board[y4][x4] is not None:
            cl = self.chess_on_board[y4][x4].r_color()
            if cl == self.color:
                return False

        if abs(self.x - x2) == 1 and abs(self.y - y2) == 0:
            c += 1
        elif abs(self.x - x2) == 0 and abs(self.y - y2) == 1:
            c += 1
        if c == 1:
            if abs(x2 - x3) == 1 and abs(y2 - y3) == 0:
                c += 1
            elif abs(x2 - x3) == 0 and abs(y2 - y3) == 1:
                c += 1
        if c == 2:
            if abs(x3 - x4) == 1 and abs(y3 - y4) == 0:
                c += 1
            elif abs(x3 - x4) == 0 and abs(y3 - y4) == 1:
                c += 1

        if c == 3:
            self.chess_on_board[y4][x4] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x4, y4
            return True
        return False


class Pilot(Chess):  # лётчик
    def look(self):
        return f'Pl{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = al[0], al[1], al[2], al[3], al[4], al[5]
        c = 0

        if self.chess_on_board[y4][x4] is not None:
            cl = self.chess_on_board[y4][x4].r_color()
            if cl == self.color:
                return False

        if abs(self.x - x2) == 1 and abs(self.y - y2) == 1:
            c += 1
        if c == 1:
            if abs(x2 - x3) == 1 and abs(y2 - y3) == 1:
                c += 1
        if c == 2:
            if abs(x3 - x4) == 1 and abs(y3 - y4) == 1:
                c += 1

        if c == 3:
            self.chess_on_board[y4][x4] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x4, y4
            return True
        return False


class Leader(Chess):  # вождь
    def look(self):
        return f'Ld{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = al[0], al[1], al[2], al[3], al[4], al[5]
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            return False
        if self.chess_on_board[y3][x3] is not None:
            return False
        if self.chess_on_board[y4][x4] is not None:
            cl = self.chess_on_board[y4][x4].r_color()
            if cl == self.color:
                return False

        if abs(self.x - x2) < 2 and abs(self.y - y2) < 2 or abs(self.x - x2) + abs(self.y - y2) == 1:
            c += 1
        if c == 1:
            if abs(x2 - x3) < 2 and abs(y2 - y3) < 2 or abs(x2 - x3) + abs(y2 - y3) == 1:
                c += 1
        if c == 2:
            if abs(x3 - x4) < 2 and abs(y3 - y4) < 2 or abs(x3 - x4) + abs(y3 - y4) == 1:
                c += 1

        if c == 3:
            self.chess_on_board[y4][x4] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x4, y4
            return True
        return False


class Princess(Chess):  # принцесса
    def __init__(self, color, x, y, run=0):
        super().__init__(color, x, y)
        self.run_counter = run

    def look(self):
        return f'Pr{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = al[0], al[1], al[2], al[3], al[4], al[5]
        c = 0

        if self.chess_on_board[y4][x4] is not None:
            cl = self.chess_on_board[y4][x4].r_color()
            if cl == self.color:
                return False

        if self.run_counter == 1 and (x2 == x3 and y2 == y3 and x3 == x4 and y3 == y4):
            if self.chess_on_board[y4][x4] is not None:
                return False

            self.chess_on_board[y4][x4] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x4, y4
            self.run_counter -= 1
            return True
        if abs(self.x - x2) < 2 and abs(self.y - y2) < 2 or abs(self.x - x2) + abs(self.y - y2) == 1:
            c += 1
        if c == 1:
            if abs(x2 - x3) < 2 and abs(y2 - y3) < 2 or abs(x2 - x3) + abs(y2 - y3) == 1:
                c += 1
        if c == 2:
            if abs(x3 - x4) < 2 and abs(y3 - y4) < 2 or abs(x3 - x4) + abs(y3 - y4) == 1:
                c += 1

        if c == 3:
            self.chess_on_board[y4][x4] = self.chess_on_board[self.y][self.x]
            self.chess_on_board[self.y][self.x] = None
            self.x, self.y = x4, y4
            return True
        return False
