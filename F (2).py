# from secrets import API_KEY
# from chess import Board
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters


class Game:
    def __init__(self):
        self.chess_on_board = [[None] * 10 for _ in range(10)]
        self.chess_on_board[1] = [Toat('Bl', 0, 1), Pawn('Bl', 1, 1), Pawn('Bl', 2, 1),
                                  Pawn('Bl', 3, 1), Pawn('Bl', 4, 1), Pawn('Bl', 5, 1),
                                  Pawn('Bl', 6, 1), Pawn('Bl', 7, 1), Pawn('Bl', 8, 1),
                                  Toat('Bl', 9, 1)]

        self.chess_on_board[0] = [Warrior('Bl', 0, 0), PodDwar('Bl', 1, 0), Dwar('Bl', 2, 0),
                                  Pilot('Bl', 3, 0), Princess('Bl', 4, 0), Leader('Bl', 5, 0),
                                  Pilot('Bl', 6, 0), Dwar('Bl', 7, 0), PodDwar('Bl', 8, 0),
                                  Warrior('Bl', 9, 0)]

        self.chess_on_board[8] = [Toat('Wt', 0, 8), Pawn('Wt', 1, 8), Pawn('Wt', 2, 8),
                                  Pawn('Wt', 3, 8), Pawn('Wt', 4, 8), Pawn('Wt', 5, 8),
                                  Pawn('Wt', 6, 8), Pawn('Wt', 7, 8), Pawn('Wt', 8, 8),
                                  Toat('Wt', 9, 8)]

        self.chess_on_board[9] = [Warrior('Wt', 0, 9), PodDwar('Wt', 1, 9), Dwar('Wt', 2, 9),
                                  Pilot('Wt', 3, 9), Leader('Wt', 4, 9), Princess('Wt', 5, 9),
                                  Pilot('Wt', 6, 9), Dwar('Wt', 7, 9), PodDwar('Wt', 8, 9),
                                  Warrior('Wt', 9, 9)]
        self.color = 'Wt'

    def new_game(self):
        self.chess_on_board = [[None] * 10 for _ in range(10)]
        self.chess_on_board[1] = [Toat('Bl', 0, 1), Pawn('Bl', 1, 1), Pawn('Bl', 2, 1),
                                  Pawn('Bl', 3, 1), Pawn('Bl', 4, 1), Pawn('Bl', 5, 1),
                                  Pawn('Bl', 6, 1), Pawn('Bl', 7, 1), Pawn('Bl', 8, 1),
                                  Toat('Bl', 9, 1)]

        self.chess_on_board[0] = [Warrior('Bl', 0, 0), PodDwar('Bl', 1, 0), Dwar('Bl', 2, 0),
                                  Pilot('Bl', 3, 0), Princess('Bl', 4, 0), Leader('Bl', 5, 0),
                                  Pilot('Bl', 6, 0), Dwar('Bl', 7, 0), PodDwar('Bl', 8, 0),
                                  Warrior('Bl', 9, 0)]

        self.chess_on_board[8] = [Toat('Wt', 0, 8), Pawn('Wt', 1, 8), Pawn('Wt', 2, 8),
                                  Pawn('Wt', 3, 8), Pawn('Wt', 4, 8), Pawn('Wt', 5, 8),
                                  Pawn('Wt', 6, 8), Pawn('Wt', 7, 8), Pawn('Wt', 8, 8),
                                  Toat('Wt', 9, 8)]

        self.chess_on_board[9] = [Warrior('Wt', 0, 9), PodDwar('Wt', 1, 9), Dwar('Wt', 2, 9),
                                  Pilot('Wt', 3, 9), Leader('Wt', 4, 9), Princess('Wt', 5, 9),
                                  Pilot('Wt', 6, 9), Dwar('Wt', 7, 9), PodDwar('Wt', 8, 9),
                                  Warrior('Wt', 9, 9)]
        self.update()

    def draw_pc(self):
        s = ["```", "   0    1    2    3    4    5    6    7    8    9",
             "+----+----+----+----+----+----+----+----+----+----+"]
        for q, i in enumerate(self.chess_on_board):
            s1 = []
            for j in i:
                j1 = '|    '
                if j is not None:
                    j1 = '|' + j.look()
                s1.append(j1)
            s.append(''.join(s1) + '| ' + str(q))
            s.append("+----+----+----+----+----+----+----+----+----+----+")
        s.append("```")
        if self.color == 'Wt':
            cl = 'белых'
        else:
            cl = 'чёрных'
        s.append(f'Сейчас ход {cl}')
        return s

    def move_figure_helper(self, x_pos, y_pos, al):  # движение фигур по доске
        try:
            x, y = int(x_pos), int(y_pos)
            fl = False
            if self.chess_on_board[y][x] is not None:
                cl = self.chess_on_board[y][x].r_color()
                if cl == self.color:
                    fl = self.chess_on_board[y][x].move(al)
            if fl:
                if self.color == 'Wt':
                    self.color = 'Bl'
                else:
                    self.color = 'Wt'
            return fl
        except TypeError:
            return False

    def move_figure(self, x_pos, y_pos, al):
        fl = self.move_figure_helper(x_pos, y_pos, al)
        self.update()
        return fl

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
        self.run_counter = 1

    def r_color(self):
        return self.color

    def new_board(self, chess_on_board):
        self.chess_on_board = chess_on_board


class Pawn(Chess):  # пешка
    def look(self):
        return f'Pn{self.color}'

    def move(self, al):
        x2, y2 = int(al[0]), int(al[1])
        c = 0

        if self.chess_on_board[y2][x2] is not None:
            cl = self.chess_on_board[y2][x2].r_color()
            if cl == self.color:
                return False

        if self.color == 'Wt':
            if self.y - 1 <= y2 <= self.y:
                if y2 == self.y and x2 != self.x and self.x - 1 <= x2 <= self.x + 1:
                    c += 1
                elif self.x - 1 <= x2 <= self.x + 1:
                    c += 1
        else:
            if self.y <= y2 <= self.y + 1:
                if self.x - 2 < x2 < self.x + 2 and self.y == y2 and x2 != self.x:
                    c += 1
                elif self.x - 2 < x2 < self.x + 2:
                    c += 1
        if c == 1:
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y2][x2] = Pawn(self.color, x2, y2)

        if c == 1:
            return True
        else:
            return False


class Toat(Chess):  # тоат
    def look(self):
        return f'Tt{self.color}'

    def move(self, al):
        x2, y2, x3, y3 = int(al[0]), int(al[1]), int(al[2]), int(al[3])
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
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y3][x3] = Toat(self.color, x3, y3)

        if c == 3:
            return True
        return False


class Warrior(Chess):  # воин
    def look(self):
        return f'Wa{self.color}'

    def move(self, al):
        x2, y2, x3, y3 = int(al[0]), int(al[1]), int(al[2]), int(al[3])
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
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y3][x3] = Warrior(self.color, x3, y3)

        if c == 2:
            return True
        return False


class PodDwar(Chess):  # под-двар
    def look(self):
        return f'Pd{self.color}'

    def move(self, al):
        x2, y2, x3, y3 = int(al[0]), int(al[1]), int(al[2]), int(al[3])
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
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y3][x3] = PodDwar(self.color, x3, y3)

        if c == 2:
            return True
        return False


class Dwar(Chess):  # двар
    def look(self):
        return f'Dw{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = int(al[0]), int(al[1]), int(al[2]), int(al[3]), int(al[4]), int(
            al[5])
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
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y4][x4] = Dwar(self.color, x4, y4)

        if c == 3:
            return True
        return False


class Pilot(Chess):  # лётчик
    def look(self):
        return f'Pl{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = int(al[0]), int(al[1]), int(al[2]), int(al[3]), int(al[4]), int(
            al[5])
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
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y4][x4] = Pilot(self.color, x4, y4)

        if c == 3:
            return True
        return False


class Leader(Chess):  # вождь
    def look(self):
        return f'Ld{self.color}'

    def move(self, al):
        x2, y2, x3, y3, x4, y4 = int(al[0]), int(al[1]), int(al[2]), int(al[3]), int(al[4]), int(
            al[5])
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
            self.chess_on_board[self.y][self.x] = None
            self.chess_on_board[y4][x4] = Leader(self.color, x4, y4)

        if c == 3:
            return True
        return False


class Princess(Chess):  # принцесса
    def look(self):
        return f'Pr{self.color}'

    def move(self, al):
        if len(al) > 2:
            x2, y2, x3, y3, x4, y4 = int(al[0]), int(al[1]), int(al[2]), int(al[3]), int(al[4]), int(al[5])
            c = 0

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
                self.chess_on_board[self.y][self.x] = None
                self.chess_on_board[y4][x4] = Princess(self.color, x4, y4)

            if c == 3:
                return True
            return False

        elif len(al) == 2:
            if self.run_counter == 1:
                x4, y4 = int(al[2]), int(al[3])

                if self.chess_on_board[y4][x4] is not None:
                    return False

                self.chess_on_board[self.y][self.x] = None
                self.chess_on_board[y4][x4] = Princess(self.color, x4, y4)

                return True
            return False
        return False


def first_help(update, context):
    update.message.reply_text('Кхм... Здрасте, пожалуйста, выберете одну из представленных команд',
                              reply_markup=ReplyKeyboardMarkup([['/start', '/help', '/command_help']],
                                                               one_time_keyboard=True, resize_keyboard=True))


def start(update, context):
    update.message.reply_text('Игра начнётся/продолжится тогда, когда вы выберете платформу.\n'
                              'Для этого выберете команду ниже',
                              reply_markup=ReplyKeyboardMarkup([['/pc', '/help']], one_time_keyboard=True,
                                                               resize_keyboard=True))


def game_pc(update, context):
    s = game.draw_pc()
    w = '\n'.join(s)
    update.message.reply_text(w, parse_mode="Markdown")
    if w.count('Pr') == 1:
        game.new_game()
        update.message.reply_text('Опа, а тут игра закончена. Можно начать заново.\nУдачи! :]',
                                  reply_markup=ReplyKeyboardMarkup([['/end', '/help']], one_time_keyboard=True,
                                                                   resize_keyboard=True))


def end_game(update, context):
    update.message.reply_text('RELOAD SYSTEM')
    game.new_game()
    update.message.reply_text('Здрасте, система перезагружена, в шахматы можно играть :]',
                              reply_markup=ReplyKeyboardMarkup([['/start', '/help']], one_time_keyboard=True,
                                                               resize_keyboard=True))


def help(update, context):
    update.message.reply_text('Здрасте ещё раз (даже если это первый). Здесь ведётся игра в марсианские шахматы. '
                              'Правила можно посмотреть написав соответствующую команду',
                              reply_markup=ReplyKeyboardMarkup([['/start', '/roots', '/command_help']],
                                                               one_time_keyboard=True, resize_keyboard=True))


def roots(update, context):
    update.message.reply_text('Марсианские шахматы\n'
                              'В этих шахматах фигуры ходят совсем не стандартным образом, а так же в один ход игрока'
                              ', каждая определённая фигура должна сходить на строго определённое количество шагов/'
                              'клеток.\n'
                              'Расстановка фигур тоже жёсткая: Тоат, Пешка * 8, Тоат; Воин, Под-Двар, Двар, Лётчик,'
                              ' Вождь, Принцесса, Лётчик, Двар, Под-Двар, Воин.\n'
                              'Соответственно и само поле является доской 10*10.\n'
                              '\nКак ходят фигуры?\n'
                              'Первыми ходят белые.\n'
                              'Пешка / Pn.\n'
                              'Пешка может ходить на соседние клетки в 5-ти сторонах: вперёд, '
                              'в бока и по диагонали вперёд.\n'
                              'Тоат / Tt.\n'
                              'Тоат уже имеет комбинаторное движение, т.е. имеет уже несколько шагов за 1 ход игрока.'
                              ' Он должен ходить на 1 соседнюю клетку по диагонали и на 1 соседнюю по '
                              'горизонталям/вертикалям. Ходить в такой последовательности не обязательно, но '
                              'обязательно знать, что он свои шаги чередует, и за 1 ход игрока не может перейти '
                              'более или менее 2 клеток.\n'
                              'Воин / Wa.\n'
                              'Воин ходит только по горизонталям/вертикалям, и шагает он 2 раза.\n'
                              'Под-Двар / Pd.\n'
                              'Под-Двар ходит по 2-ум соседним клеткам по диагонали.\n'
                              'Двар / Dw.\n'
                              'Двар ходит по 3 соседним клеткам по горизонталям/вертикалям.\n'
                              'Лётчик / Pl.\n'
                              'Лётчик, в отличии от остальных фигур (за исключением Принцессы), может перепрыгивать '
                              'через другие фигуры и прийти на место назначения "по головам" фигур. '
                              'Ходит по 3 соседним диагоналям.\n'
                              'Вождь / Ld.\n'
                              'Та фигура, которая не имеет границ по направлению движения, но ограничена '
                              'в шагах, их всего 3.\n'
                              'Принцесса / Pr.\n'
                              'Фигура, что считает в себе ходы Вождя и возможность перепрыгивать через другие фигуры. '
                              'В отличии от всех остальных фигур, её нужно оберегать от съедения противником.\n'
                              '\nВсе, кроме принцессы, могут поедать все фигуры, только на последнем своём шаге.\n',
                              reply_markup=ReplyKeyboardMarkup([['/start', '/help']], one_time_keyboard=True,
                                                               resize_keyboard=True, parse_mode="Markdown"))


def move(update, context):
    args = context.args
    try:
        x1, y1, al = args[0], args[1], args[2:]
        # print(x1, y1, al)
        fl = game.move_figure(x1, y1, al)
        if fl:
            res = 'Передвигаем фигуру'
        else:
            res = 'Фигура не выбрана / выбрана фигура другого цвета / фигура не способна на такое перемещение /' \
                  ' фигура встаёт на союзника) / неверный тип данных\n' \
                  'Выполните команду ещё раз, но уже с корректными значениями'
        update.message.reply_text(res)
        game_pc(update, context)
    except (IndexError, ValueError):
        update.message.reply_text('Вы ввели недостаточное количество пар для фигуры / пара не полноценная / вы ничего '
                                  'не ввели.\n'
                                  'Посмотрите правила для полного понимания движений фигур',
                                  reply_markup=ReplyKeyboardMarkup([['/roots', '/help']], one_time_keyboard=True,
                                                                   resize_keyboard=True))
        update.message.reply_text('Использование: /move <х-координата> <у-координата> + '
                                  'ещё 1-3 пары координат в таком стиле>')


def command_help(update, context):
    update.message.reply_text('Тут можно узнать, какая команда за что отвечает, и какие есть вообще (может вы их'
                              ' ещё не видели):\n'
                              '/help - команда даёт некоторую информацию о том, что тут происходит\n'
                              '/start - помогает начать игру\n'
                              '/pc - эта команда отвечает за "прорисовку" шахмотной доски для пк\n'
                              '/move - передвижение фигур. При вводе неверных данных говорит об этом\n'
                              '/roots - правила самой игры с примерами видов\n'
                              '/end - команда сделана для начала новой игры самостоятельно\n'
                              '/command_help - вызывает этот список, на случай чего\n',
                              reply_markup=ReplyKeyboardMarkup([['/start', '/help']], one_time_keyboard=True,
                                                               resize_keyboard=True))


def main():
    # Создаём объект updater - связь сервера и клиента.
    updater = Updater('5316221762:AAFjaEjaQa7Tu6HUuNoaN9cPR7Xd8c1zZ00')

    # Получаем из него диспетчер сообщений (соединяет обработчики сообщение с клиентом).
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, first_help)
    # reply_markup = ReplyKeyboardMarkup([['/start', '/help']], one_time_keyboard=False)

    # Регистрируем обработчик в диспетчере.
    # dp.add_handler(reply_markup)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("pc", game_pc))
    dp.add_handler(CommandHandler("move", move))
    dp.add_handler(CommandHandler("roots", roots))
    dp.add_handler(CommandHandler("end", end_game))
    dp.add_handler(CommandHandler("command_help", command_help))
    dp.add_handler(text_handler)
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    game = Game()
    main()
