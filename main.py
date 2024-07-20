import telebot
from telebot import types
from logic_game_and_chess import Game

API_cod = open('appdatainfo.txt', 'r', encoding='utf-8')[0]
bot = telebot.TeleBot(API_cod)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Нажми на /main.'
    )


@bot.message_handler(commands=['main'])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('/draw_board'))
    markup.row(types.KeyboardButton('/command_help'))
    bot.send_message(
        message.chat.id,
        'Игра начнётся/продолжится тогда, когда вы сделаете ход.\nДля этого можете отобразить доску и узнать, чей ход',
        reply_markup=markup
    )


@bot.message_handler(commands=['draw_board'])
def draw_board(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('/command_help'))
    s = game.draw_pc()
    w = '\n'.join(s)
    bot.send_message(message.chat.id, w, parse_mode="Markdown")
    if w.count('Pr') == 1:
        game.new_game()
        bot.send_message(
            message.chat.id,
            'Опа, а тут игра закончена. Игру уже можно начать.\nУдачи! :]',
            reply_markup=markup
        )


@bot.message_handler(commands=['end'])
def end_game(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('/start'))
    markup.row(types.KeyboardButton('/command_help'))
    bot.send_message(message.chat.id, 'RELOAD SYSTEM')
    game.new_game()
    bot.send_message(
        message.chat.id,
        'Здрасте, система перезагружена, в шахматы можно играть :]',
        reply_markup=markup
    )


@bot.message_handler(commands=['info'])
def information(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('/start'))
    markup.row(types.KeyboardButton('/rules'))
    markup.row(types.KeyboardButton('/command_help'))
    bot.send_message(
        message.chat.id,
        'Здрасте ещё раз (даже если это первый). Здесь ведётся игра в марсианские шахматы. '
        'Правила можно посмотреть написав соответствующую команду',
        reply_markup=markup
    )


@bot.message_handler(commands=['rules'])
def roots(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('/start'))
    markup.row(types.KeyboardButton('/command_help'))
    bot.send_message(
        message.chat.id,
        'Марсианские шахматы\n'
        'В этих шахматах фигуры ходят совсем не стандартным образом, а так же в один ход игрока, '
        'каждая определённая фигура должна сходить на строго определённое количество шагов/клеток.\n'
        'Расстановка фигур тоже жёсткая:\nТоат, Пешка * 8, Тоат\nВоин, Под-Двар, Двар, Лётчик, Вождь, '
        'Принцесса, Лётчик, Двар, Под-Двар, Воин.\nСоответственно и само поле является доской 10*10.\n'
        '\nКак ходят фигуры?\nПервыми ходят белые.\nПешка / Pn.\n'
        'Пешка может ходить на соседние клетки в 5-ти сторонах: вперёд, в бока и по диагонали вперёд.\n'
        'Тоат / Tt.\nТоат уже имеет комбинаторное движение, т.е. имеет уже несколько шагов за 1 ход игрока. '
        'Он должен ходить на 1 соседнюю клетку по диагонали и на 1 соседнюю по горизонталям/вертикалям. '
        'Ходить в такой последовательности не обязательно, но обязательно знать, что он свои шаги чередует, '
        'и за 1 ход игрока не может перейти больше или меньше 2 клеток.\nВоин / Wa.\n'
        'Воин ходит только по горизонталям/вертикалям, и шагает он 2 раза.\nПод-Двар / Pd.\n'
        'Под-Двар ходит по 2-ум соседним клеткам по диагонали.\nДвар / Dw.\nДвар ходит по 3 соседним '
        'клеткам по горизонталям/вертикалям.\nЛётчик / Pl.\nЛётчик, в отличии от остальных фигур '
        '(за исключением Принцессы), может перепрыгивать через другие фигуры и прийти на место '
        'назначения "по головам" фигур. Ходит по 3 соседним диагоналям.\nВождь / Ld.\n'
        'Та фигура, которая не имеет границ по направлению движения, но ограничена в шагах, их всего 3.\n'
        'Принцесса / Pr.\nФигура, что считает в себе ходы Вождя и возможность перепрыгивать через другие фигуры. '
        'В отличии от всех остальных фигур, её нужно оберегать от съедения противником.\n'
        'Один раз за всю партию может совершить побег. Побег может произойти в любой момент, главное, чтобы на месте,'
        ' куда хотят сбежать, не было никого. А для того, чтобы сбежать, достаточно написать координаты, куда следует'
        ' переместить фигуру\n'
        '\nА чтобы вообще перемещать фигуры используйте команду /move. После самой команды, в этом же сообщении, '
        'напишите последовательно координаты (x и y, через пробел) самой фигуры, которую хотите передвигать, и '
        'последовательность координат других клеток, куда потом будет ступать фигура, в том количесвте, сколько шагов '
        'за ваш ход она делает. Как уже было написано выше, Принцесса может постоянно ходить на 3 клетки или один раз '
        'сбежать на любую другую свободную клетку, напишите только координаты правильно.\n\n'
        'А, ну и последнее, не менее важное правило: фигура может поедать вражескую только на последнем своём шаге.\n'
        '\nНа этом вроде бы всё. Удачи в играх!',
        reply_markup=markup
    )


@bot.message_handler(commands=['move'])
def move(message):
    try:
        args = [int(i) - 1 for i in message.text.split()[1:]]
        x1, y1, al = args[0], args[1], args[2:]
        fl = game.move_figure(x1, y1, al)
        if fl:
            res = 'Передвигаем фигуру'
        else:
            res = 'Фигура не выбрана / выбрана фигура другого цвета / фигура не способна на такое перемещение /' \
                  ' фигура встаёт на союзника) / неверный тип данных\n' \
                  'Выполните команду ещё раз, но уже с корректными значениями'
        bot.send_message(message.chat.id, res)
        draw_board(message)
    except (IndexError, ValueError):
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton('/rules'))
        markup.row(types.KeyboardButton('/command_help'))
        bot.send_message(
            message.chat.id,
            'Вы ввели недостаточное количество пар для фигуры / пара не полноценная / вы ничего не ввели.\n'
            'Посмотрите правила для полного понимания движений фигур'
        )
        bot.send_message(
            message.chat.id,
            'Использование: /move <х-координата> <у-координата> + ещё 1-3 пары координат в таком стиле>',
            parse_mode=markup
        )


@bot.message_handler(commands=['command_help'])
def command_help(message):
    markup = types.ReplyKeyboardMarkup()
    help_list = [
        'Тут можно узнать, какая команда за что отвечает, и какие есть вообще (может вы их ещё не видели):',
        '/help - команда даёт некоторую информацию о том, что тут происходит',
        '/start - помогает начать игру',
        '/move - передвижение фигур. При вводе неверных данных говорит об этом',
        '/rules - правила самой игры с примерами видов',
        '/draw_board - рисует доску. На ней отображаются все фигуры',
        '/end - команда сделана для начала новой игры самостоятельно',
        '/command_help - вызывает этот список, на случай чего',
        '/info - выдаёт краткую информацию, что здесь происходит',
        '/rooms - показывает информацию, в какие комнаты доступны для игры и сколько.'
    ]
    markup.row(types.KeyboardButton('/start'))
    bot.send_message(message.chat.id, '\n'.join(help_list), reply_markup=markup)


@bot.message_handler()
def random(message):
    user_text = message.text
    bot.send_message(
        message.chat.id,
        user_text
    )


if __name__ == '__main__':
    rooms = {}
    game = Game()
    bot.polling(none_stop=True)
