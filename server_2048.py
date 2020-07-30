# Marcin Wankiewicz 172118, serwer gry 2048 na hexagonach
import socket
from _thread import *
from classes_2048 import Board, Agent  # klasa pola również znajduje się w classes_2048!
import jsonpickle
from copy import deepcopy

server_address = 'localhost'
port = 5555


board = Board(3, True)
player_one = Agent(1)
player_two = Agent(2)
turn_one = True
wrong = False
game_over = False
active_connections = 0
total_connections = 0
movement_keys = ['1', '2', '3', '7', '8', '9']


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = socket.gethostbyname(server_address)

try:
    s.bind((server_address, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Server started.")


def client_thread(connection):
    global wrong, turn_one, active_connections, game_over, board, total_connections
    active_connections += 1
    total_connections += 1
    connection.send(str.encode(str((total_connections + 1) % 2)))
    while True:
        try:
            data = connection.recv(8192)
            reply = data.decode('utf-8')
            if not data:
                break
            else:
                id = reply.split(":", 1)[0]
                command = reply.split(":", 1)[1]
                wrong = False
                if "NEWGAME" in command and id == "0":
                    board = Board(int(command[7]), True)
                    turn_one = True
                    player_one.score = 0
                    player_two.score = 0
                if command in movement_keys and active_connections == 2:
                    if turn_one and id == '0':
                        second_score, wrong = player_one.move(command, board.fields)
                        player_two.score += second_score
                        if not wrong:
                            board.spawn_field(2)
                            turn_one = not turn_one
                    elif not turn_one and id == '1':
                        second_score, wrong = player_two.move(command, board.fields)
                        player_one.score += second_score
                        if not wrong:
                            board.spawn_field(1)
                            turn_one = not turn_one
                    game_over = check_game_over(board)

                reply = str(id) + ":"
                reply += jsonpickle.encode(board)
                reply += "&&&" + str(turn_one) + "&&&" + str(player_one.score) + "&&&" + str(player_two.score) + "&&&" + str(wrong) + "&&&" + str(active_connections) + "&&&" + str(game_over)

            connection.sendall(str.encode(reply))
        except:
            break

    print("Connection closed")
    active_connections -= 1
    connection.close()


def check_game_over(board0):
    # jeśli jest jakieś puste pole to na pewno nie jest koniec gry
    for field in board0.fields:
        if field.value is None:
            return False
    # jeśli plansza jest pełna, to sprawdzamy czy jest możliwość jakiegoś ruchu
    move_possible = can_move(board0)
    # zwracamy negację aby zachować logiczny sens funkcji (jeśli nie ma ruchu, to game over)
    return not move_possible


def can_move(board0):
    # to tylko sprawdzenie - nie chcemy, by oryginalne pola uległy zmianie
    test_fields = deepcopy(board0.fields)
    # sprawdzamy teoretyczną możliwość ruchu w każdym kierunku, jeśli jakiś jest możliwy to gra się nie kończy
    for key0 in ['1', '2', '3', '7', '8', '9']:
        _, invalid_move = player_one.move(key0, test_fields)
        if not invalid_move:
            return True
    return False


while active_connections < 2:
    connection0, address = s.accept()
    print("Connected to ", address)
    start_new_thread(client_thread, (connection0,))
