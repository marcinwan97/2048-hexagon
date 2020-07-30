# Marcin Wankiewicz 172118, klasy planszy, pola oraz agenta do gry 2048 na hexagonach
import operator
from copy import deepcopy
import random
import socket


class Configuration:
    def __init__(self, board_size=None, two_players=None, online=None, ip=None, ai=None):
        self.board_size = board_size
        self.two_players = two_players
        self.online = online
        self.ip = ip
        self.ai = ai


class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ip
        self.port = 5555
        self.id = self.connect()

    def connect(self):
        self.client.connect((self.address, self.port))
        return self.client.recv(8192).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(8192).decode()
            return reply
        except socket.error as e:
            return str(e)


class Board:
    def __init__(self, size, multi):
        # pusta tablica znaków o odpowiednim wymiarze
        board0 = [['&nbsp;' for _ in range(size * 20 - 7)] for _ in range(size * 8 - 3)]
        # inicjalizacja tablicy obiektów klasy Field
        fields0 = []
        x = 6
        index = 0
        times = size
        col = 0
        for _ in range(2 * size - 1):
            y = 2 * size - (times - size) * 2
            for _ in range(times):
                fields0.append(Field(index, x, y, None, None))
                index += 1
                y += 4
            if col < size - 1:
                times += 1
            else:
                times -= 1
            col += 1
            x += 10

        # wstawienie pól na planszę (tablicę znaków)

        self.fields = fields0

        # początkowe pola w zależności od trybu gry
        self.spawn_field(1)
        if multi:
            self.spawn_field(1)
            self.spawn_field(2)

        self.size = size

    def spawn_field(self, color):
        # pojawienie się losowego pola w kolorze danego gracza
        chosen = random.choice(self.fields)
        while chosen.value is not None:
            chosen = random.choice(self.fields)
        # tak jak w oryginalnym 2048, jest mała szansa na pojawienie się 4 zamiast 2
        if random.random() > 0.9:
            chosen.value = 4
        else:
            chosen.value = 2
        chosen.color = color


class Field:
    def __init__(self, index, x0, y0, value, color):
        self.index = index  # indeks w tablicy pól
        self.x0 = x0  # geometryczne współrzędne x, y na planszy
        self.y0 = y0
        self.value = value  # wartość pola (2, 4, 8...)
        self.color = color  # numer koloru gracza, do którego należy pole
        self.connection_block = False  # aby dany klocek połączył się jedynie raz w turze


class Agent:
    def __init__(self, color):
        self.color = color  # kolor gracza (a wlaściwie numer koloru)
        self.score = 0  # aktualny wynik
        self.ai_score = 0

    # ruch ai
    def ai_move(self, fields0):
        scores = []
        enemy_scores = []
        moves = ['1', '2', '3', '7', '8', '9']

        for key0 in moves:
            test_fields = deepcopy(fields0)
            test_score = self.ai_score
            other_score, invalid_move = self.move(key0, test_fields, False)
            enemy_scores.append(other_score)
            if not invalid_move:
                new_score = self.ai_score
                scores.append(new_score-test_score)
            else:
                scores.append(-99999)

        # print(scores)
        # print(enemy_scores)
        move_values = [a_i - b_i/2 for a_i, b_i in zip(scores, enemy_scores)]
        # print(move_values)
        choice = moves[move_values.index(max(move_values))]
        # print(choice)
        second_score, _ = self.move(choice, fields0)
        return 0

    # ruch agenta
    def move(self, move_key, fields0, save_score=True):
        invalid_move = False  # czy ruch jest możliwy
        other_score = 0  # należy śledzić również punkty, które dzięki nam zdobędzie gracz 2
        if move_key == '1':
            other_score, invalid_move = self.move_fields(fields0, 10, -2, save_score)
        elif move_key == '2':
            other_score, invalid_move = self.move_fields(fields0, 0, -4, save_score)
        elif move_key == '3':
            other_score, invalid_move = self.move_fields(fields0, -10, -2, save_score)
        elif move_key == '7':
            other_score, invalid_move = self.move_fields(fields0, 10, 2, save_score)
        elif move_key == '8':
            other_score, invalid_move = self.move_fields(fields0, 0, 4, save_score)
        elif move_key == '9':
            other_score, invalid_move = self.move_fields(fields0, -10, 2, save_score)
        return other_score, invalid_move

    # wywołanie ruchu pól na planszy
    def move_fields(self, fields0, x_offset, y_offset, save_score):
        invalid_move = True  # zakładamy, że ruch jest zły (jeśli coś się poruszy, to jest dobry)
        other_score = 0
        for _ in range(8):
            # inicjalizacja tablicy początkowej od przodu lub od końca
            # (w zależności od kierunku ruchu, zapewnia to prawidłową kolejność ruchu pól)
            if x_offset == 0:
                if y_offset > 0:
                    starting_fields = deepcopy(fields0)
                else:
                    starting_fields = deepcopy(reversed(fields0))
            else:
                if x_offset > 0:
                    starting_fields = deepcopy(fields0)
                else:
                    starting_fields = deepcopy(reversed(fields0))

            # ruch dla każdego pola
            for i, field in enumerate(starting_fields):
                # ruch jest wywoływany tylko dla zapełnionych pól
                if field.value is not None:
                    # próba znalezienia sąsiada w odpowiednim kierunku, jeśli nie istnieje to pole się nie ruszy
                    try:
                        next_field = [elem for elem in fields0 if
                                      (field.x0 == elem.x0 + x_offset and field.y0 == elem.y0 + y_offset)][0]
                        next_index = fields0.index(next_field)
                    except IndexError:
                        continue

                    # ruch do pustego pola
                    if next_field.value is None:
                        invalid_move = False
                        fields0[next_index].value = field.value
                        fields0[next_index].color = field.color
                        fields0[field.index].value = None
                        fields0[field.index].color = None
                    # jeśli pole jest w tym samym kolorze i może się połączyć
                    elif next_field.color == field.color and not field.connection_block:
                        # połączenie pól
                        if next_field.value == field.value:
                            invalid_move = False
                            if save_score:
                                if field.color == self.color:  # sprawdzamy kto zdobywa punkty za połączenie
                                    self.score += 2 * field.value
                                else:
                                    other_score += 2 * field.value
                            else:
                                if field.color == self.color:  # sprawdzamy kto zdobywa punkty za połączenie
                                    self.ai_score += 2 * field.value
                                else:
                                    other_score += 2 * field.value
                            fields0[next_index].value = 2 * field.value
                            fields0[next_index].color = field.color
                            fields0[field.index].value = None
                            fields0[field.index].color = None
                            fields0[next_index].connection_block = True
                            fields0[field.index].connection_block = True

        # odblokowanie wszystkich pól na następną turę
        for field in fields0:
            field.connection_block = False

        return other_score, invalid_move


def put_hex(board0, x, y, val, color):
    # funkcja wstawiająca sześciokąt w odpowiednim miejscu w tablicy znaków
    board0[y][x - 2], board0[y][x - 1], board0[y][x], board0[y][x + 1], board0[y][
        x + 2] = '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'
    if color == 1:
        start_marker = '<font color="green">'
    elif color == 2:
        start_marker = '<font color="red">'
    else:
        start_marker = '<font>'
    # aby wartość pola była ładnie wyświetlana, a nie np. jako 00002
    if val is not None:
        if val < 10:
            board0[y][x] = start_marker + str(val) + '</font>'
        elif val < 100:
            board0[y][x - 1] = start_marker + str(int(val / 10))
            board0[y][x] = str(val % 10) + '</font>'
        elif val < 1000:
            board0[y][x - 1] = start_marker + str(int(val / 100))
            board0[y][x] = str(int(val % 100 / 10))
            board0[y][x + 1] = str(val % 10) + '</font>'
        elif val < 10000:
            board0[y][x - 2] = start_marker + str(int(val / 1000))
            board0[y][x - 1] = str(int(val % 1000 / 100))
            board0[y][x] = str(int(val % 100 / 10))
            board0[y][x + 1] = str(val % 10) + '</font>'
        else:
            board0[y][x - 2] = start_marker + str(int(val / 10000))
            board0[y][x - 1] = str(int(val % 10000 / 1000))
            board0[y][x] = str(int(val % 1000 / 100))
            board0[y][x + 1] = str(int(val % 100 / 10))
            board0[y][x + 2] = str(val % 10) + '</font>'

    # górna i dolna część ściany pola
    board0[y + 2][x], board0[y + 2][x - 2], board0[y + 2][x + 2], board0[y + 2][x - 3], board0[y + 2][x + 3] = 5 * '_'
    board0[y - 2][x], board0[y - 2][x - 2], board0[y - 2][x + 2], board0[y - 2][x - 3], board0[y - 2][x + 3] = 5 * '_'
    board0[y - 2][x - 1], board0[y - 2][x + 1], board0[y + 2][x - 1], board0[y + 2][x + 1] = 4 * '_'

    # ściany boczne
    board0[y][x + 6], board0[y][x - 6] = '\\', '/'
    board0[y - 1][x + 5], board0[y - 1][x - 5] = '\\', '/'
    board0[y + 2][x + 4], board0[y + 2][x - 4] = '/', '\\'
    board0[y + 1][x + 5], board0[y + 1][x - 5] = '/', '\\'

    return board0
