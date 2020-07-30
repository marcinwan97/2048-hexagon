# Marcin Wankiewicz 172118, gra 2048 na hexagonach, konfiguracja w JSON, historia w XML, replay
import sys
import ui_2048
import resources
import jsonpickle
import distutils.util
from copy import deepcopy
from xml.dom import minidom
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore
from classes_2048 import Configuration, Network, Board, Agent       # klasa pola również znajduje się w classes_2048!


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(1200, 800)
        self.ui = ui_2048.Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        # zmienne dotyczące replaya
        self.history = ""
        self.history_index = 0
        self.replay_timer = QtCore.QTimer(self)
        self.replay_timer.timeout.connect(self.tick_timer_replay)

        # zmienne internetowe
        self.net = None
        self.ip = 'localhost'
        self.online = False
        self.active_players = 0
        self.net_timer = QtCore.QTimer(self)
        self.net_timer.timeout.connect(self.update_game)

        # zmienne gry
        self.board_size = 3
        self.two_players = False
        self.ai = False
        self.wrong_timer = QtCore.QTimer(self)
        self.wrong_timer.timeout.connect(self.reset_wrong_move)
        self.ai_timer = QtCore.QTimer(self)
        self.ai_timer.timeout.connect(self.ai_move)
        self.game_over = False
        self.turn_one = True
        self.p_one = Agent(1)                  # zamiast kolorów cyfry sa identyfikatorem graczy
        self.p_two = Agent(2)
        self.wrong = False

        # połączenie z push buttonami
        self.ui.pushButtonNewGame.clicked.connect(self.push_button_new_game_click)
        self.ui.pushButtonUp.clicked.connect(self.push_button_up_click)
        self.ui.pushButtonLeftUp.clicked.connect(self.push_button_left_up_click)
        self.ui.pushButtonRightUp.clicked.connect(self.push_button_right_up_click)
        self.ui.pushButtonDown.clicked.connect(self.push_button_down_click)
        self.ui.pushButtonLeftDown.clicked.connect(self.push_button_left_down_click)
        self.ui.pushButtonRightDown.clicked.connect(self.push_button_right_down_click)
        self.ui.pushButtonSaveConfig.clicked.connect(self.save_configuration)
        self.ui.pushButtonLoadConfig.clicked.connect(self.load_configuration)
        self.ui.pushButtonReplay.clicked.connect(self.push_button_replay_click)
        self.ui.hexLabel.setPixmap(QtGui.QPixmap(':/gray'))
        self.ui.hexLabel.setScaledContents(True)

        # wczytanie konfiguracji z pliku JSON
        self.load_configuration()
        self.board = Board(self.board_size, self.two_players)
        self.paint_graphics()

    # start replaya
    def push_button_replay_click(self):
        if not self.online:
            self.history_index = 0
            self.replay_timer.start(1000)

    # jeden krok replaya
    def tick_timer_replay(self):
        try:
            history = minidom.parse('history.xml')
            steps = history.getElementsByTagName('STEP')
            self.board = jsonpickle.decode(steps[self.history_index].getElementsByTagName('BOARD')[0].firstChild.nodeValue)
            self.two_players = bool(distutils.util.strtobool(steps[self.history_index].getElementsByTagName('TWO_P')[0].firstChild.nodeValue))
            self.turn_one = bool(distutils.util.strtobool(steps[self.history_index].getElementsByTagName('TURN')[0].firstChild.nodeValue))
            self.game_over = bool(distutils.util.strtobool(steps[self.history_index].getElementsByTagName('OVER')[0].firstChild.nodeValue))
            self.p_one.score = steps[self.history_index].getElementsByTagName('SCORE_1')[0].firstChild.nodeValue
            self.p_two.score = steps[self.history_index].getElementsByTagName('SCORE_2')[0].firstChild.nodeValue
            self.board_size = self.board.size
            self.wrong = False
            self.paint_graphics()
            self.history_index += 1

            # zatrzymanie timera na końcu historii
            if self.history_index > len(steps)-1:
                self.replay_timer.stop()
        except:
            pass

    # dodanie kroku do historii wywoływane po każdym prawidłowym ruchu
    def add_history(self):
        self.history += "\t<STEP>\n"
        self.history += "\t\t<BOARD>" + jsonpickle.encode(self.board) + "</BOARD>\n"
        self.history += "\t\t<TWO_P>" + str(self.two_players) + "</TWO_P>\n"
        self.history += "\t\t<TURN>" + str(self.turn_one) + "</TURN>\n"
        self.history += "\t\t<OVER>" + str(self.game_over) + "</OVER>\n"
        self.history += "\t\t<SCORE_1>" + str(self.p_one.score) + "</SCORE_1>\n"
        self.history += "\t\t<SCORE_2>" + str(self.p_two.score) + "</SCORE_2>\n"
        self.history += "\t</STEP>\n"
        self.save_history()

    # zapis historii wywoływany na koniec dodawania do historii
    def save_history(self):
        history_file = open("history.xml", "w")

        # opatrzenie historii odpowiednimi znacznikami xml
        history_file.write('<?xml version="1.0"?>\n<HISTORY>\n' + self.history + "</HISTORY>")
        history_file.close()

    def load_configuration(self):
        try:
            # Wczytanie konfiguracji po rozpoczęciu programu
            config_file = open("config.json", "r")
            data = config_file.read()
            config_file.close()
            configuration = jsonpickle.decode(data)
            self.board_size = configuration.board_size
            if self.board_size == 2:
                self.ui.radioButton2.setChecked(True)
            elif self.board_size == 3:
                self.ui.radioButton3.setChecked(True)
            elif self.board_size == 4:
                self.ui.radioButton4.setChecked(True)
            elif self.board_size == 5:
                self.ui.radioButton5.setChecked(True)
            self.two_players = configuration.two_players
            if self.two_players:
                self.ui.radioButtonHotSeat.setChecked(True)
            else:
                self.ui.radioButtonSingle.setChecked(True)
            self.online = configuration.online
            if self.online:
                self.ui.radioButtonOnline.setChecked(True)
                self.net = Network(configuration.ip)
                self.update_game("NEWGAME" + str(self.board_size))
                self.net_timer.start(500)
            self.ai = configuration.ai
            if self.ai:
                self.ui.radioButtonAI.setChecked(True)
            self.ui.lineEditServer.setText(str(configuration.ip))
        except:
            pass

    def save_configuration(self):
        # Zapis konfiguracji preferowanej po wciśnięciu przycisku
        configuration = Configuration()
        if self.ui.radioButton2.isChecked():
            configuration.board_size = 2
        elif self.ui.radioButton3.isChecked():
            configuration.board_size = 3
        elif self.ui.radioButton4.isChecked():
            configuration.board_size = 4
        else:
            configuration.board_size = 5
        if self.ui.radioButtonSingle.isChecked():
            configuration.two_players = False
        else:
            configuration.two_players = True
        if self.ui.radioButtonOnline.isChecked():
            configuration.online = True
        else:
            configuration.online = False
        if self.ui.radioButtonAI.isChecked():
            configuration.ai = True
        else:
            configuration.ai = False
        configuration.ip = self.ui.lineEditServer.text()

        data = jsonpickle.encode(configuration)
        config_file = open("config.json", "w")
        config_file.write(data)
        config_file.close()

    def reset_wrong_move(self):
        self.ui.hexLabel.setPixmap(QtGui.QPixmap(':/gray'))

    def paint_graphics(self):
        self.scene.clear()
        for field in self.board.fields:
            hexagon = QGraphicsPixmapItem()
            hexagon.setScale(0.4/self.board_size)
            if field.value is not None:
                resource_name = str(field.value)
                if field.color == 1:
                    resource_name += 'g'
                else:
                    resource_name += 'r'
                hexagon.setPixmap(QtGui.QPixmap(':/' + resource_name))
            else:
                hexagon.setPixmap(QtGui.QPixmap(':/gray'))

            hexagon.setPos(field.x0 / self.board_size * 29, field.y0 / self.board_size * 85.5)
            self.scene.addItem(hexagon)

        if self.game_over:
            self.ui.hexLabel.setPixmap(QtGui.QPixmap(':/over'))
        elif self.wrong:
            self.ui.hexLabel.setPixmap(QtGui.QPixmap(':/wrong'))
            self.wrong_timer.start(1000)
        if self.two_players:
            if self.turn_one:
                self.ui.labelTurn.setText('<html><head/><body><p><span style="font-weight:600;color:#33dc30;">Player '
                                          '1 turn</span></p></body></html>')
            else:
                self.ui.labelTurn.setText('<html><head/><body><p><span style="font-weight:600;color:#aa1900;">Player '
                                          '2 turn</span></p></body></html>')
            self.ui.label1.setText('<html><head/><body><p><span style="font-weight:600;color:#33dc30;">Player 1 score: '
                                   + str(self.p_one.score) + '</span></p></body></html>')
            self.ui.label2.setText('<html><head/><body><p><span style="font-weight:600;color:#aa1900;">Player 2 score: '
                                   + str(self.p_two.score) + '</span></p></body></html>')
        else:
            self.ui.labelTurn.setText('')
            self.ui.label1.setText('<html><head/><body><p><span style="font-weight:600; color:#33dc30;">Score: '
                                   + str(self.p_one.score) + '</span></p></body></html>')
            self.ui.label2.setText('')
        if self.online:
            self.ui.labelInfo.setText("Only player 1 can start a new online game!")
            if self.active_players == "2":
                self.ui.labelStatus.setText("Connected! You are player " + str(int(self.net.id) + 1))
            else:
                self.ui.labelStatus.setText("Waiting for connection...")
        else:
            self.ui.labelInfo.setText("")
            self.ui.labelStatus.setText("")

    def keyPressEvent(self, e):
        # sterowanie z klawiatury
        if e.key() == QtCore.Qt.Key_1:
            self.push_button_left_down_click()
        elif e.key() == QtCore.Qt.Key_2:
            self.push_button_down_click()
        elif e.key() == QtCore.Qt.Key_3:
            self.push_button_right_down_click()
        elif e.key() == QtCore.Qt.Key_7:
            self.push_button_left_up_click()
        elif e.key() == QtCore.Qt.Key_8:
            self.push_button_up_click()
        elif e.key() == QtCore.Qt.Key_9:
            self.push_button_right_up_click()
        elif e.key() == QtCore.Qt.Key_Q or e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def push_button_new_game_click(self):
        # rozpoczęcie nowej gry
        self.ui.hexLabel.setPixmap(QtGui.QPixmap(':/gray'))
        self.game_over = False
        self.turn_one = True
        self.history_index = 0
        self.history = ""
        self.replay_timer.stop()
        self.ip = self.ui.lineEditServer.text()
        self.active_players = 0
        if self.ui.radioButton2.isChecked():
            self.board_size = 2
        elif self.ui.radioButton3.isChecked():
            self.board_size = 3
        elif self.ui.radioButton4.isChecked():
            self.board_size = 4
        else:
            self.board_size = 5
        if self.ui.radioButtonSingle.isChecked():
            self.two_players = False
        else:
            self.two_players = True
        if self.ui.radioButtonOnline.isChecked():
            self.online = True
            if self.net is None:
                self.net = Network(self.ip)
            self.update_game("NEWGAME" + str(self.board_size))
            self.net_timer.start(500)
        else:
            self.online = False
            self.net = None
            self.net_timer.stop()
            self.board = Board(self.board_size, self.two_players)
        if self.ui.radioButtonAI.isChecked():
            self.ai = True

        self.p_one = Agent(1)
        self.p_two = Agent(2)
        self.wrong = False
        self.paint_graphics()

    # sterowanie przy pomocy przycisków interfejsu
    def push_button_up_click(self):
        self.button_move("8")

    def push_button_left_up_click(self):
        self.button_move("7")

    def push_button_right_up_click(self):
        self.button_move("9")

    def push_button_down_click(self):
        self.button_move("2")

    def push_button_left_down_click(self):
        self.button_move("1")

    def push_button_right_down_click(self):
        self.button_move("3")

    def button_move(self, move_key):
        if self.history_index != 0:
            self.push_button_new_game_click()
        elif not self.online:
            # wywołanie ruchu odpowiedniego agenta w zależności od wybranego kierunku
            self.wrong = False
            if not self.game_over:
                if self.turn_one or not self.two_players:
                    second_score, self.wrong = self.p_one.move(move_key, self.board.fields)
                    self.p_two.score += second_score
                    if not self.wrong:
                        self.add_history()
                        if self.two_players:
                            self.board.spawn_field(2)
                        else:
                            self.board.spawn_field(1)
                        self.turn_one = not self.turn_one
                        if self.ai:
                            self.ai_timer.start(500)
                elif not self.ai:
                    second_score, self.wrong = self.p_two.move(move_key, self.board.fields)
                    self.p_one.score += second_score
                    if not self.wrong:
                        self.add_history()
                        self.board.spawn_field(1)
                        self.turn_one = not self.turn_one

                # sprawdzanie końca gry, aktualizacja planszy
                self.game_over = self.check_game_over()
            else:
                self.add_history()
        else:
            self.update_game(move_key)
        self.paint_graphics()

    def ai_move(self):
        other_score = self.p_two.ai_move(self.board.fields)
        self.p_one.score += other_score
        self.add_history()
        self.board.spawn_field(1)
        self.turn_one = not self.turn_one
        self.game_over = self.check_game_over()
        self.paint_graphics()
        self.ai_timer.stop()

    def update_game(self, move_key="0"):
        # pobranie odpowiednich parametrów z serwera, funkcja wywoływana cyklicznie
        self.board, self.turn_one, self.p_one.score, self.p_two.score, self.wrong, self.active_players, self.game_over\
            = self.parse_data(self.send_data(move_key))
        self.board_size = self.board.size
        self.paint_graphics()

    def send_data(self, move_key):
        # wysłanie żądania ruchu (lub nowej gry)
        data = str(self.net.id) + ":" + str(move_key)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            # podział wiadomości na poszczególne zmienne
            d = data.split(":", 1)[1].split("&&&")
            data_board = jsonpickle.decode(d[0])
            data_turn = bool(distutils.util.strtobool(d[1]))
            data_score1 = d[2]
            data_score2 = d[3]
            data_wrong = bool(distutils.util.strtobool(d[4]))
            data_active = d[5]
            data_over = bool(distutils.util.strtobool(d[6]))
            return data_board, data_turn, data_score1, data_score2, data_wrong, data_active, data_over
        except:
            print("Parsing error.")
            return 0

    def check_game_over(self):
        # jeśli jest jakieś puste pole to na pewno nie jest koniec gry
        for field in self.board.fields:
            if field.value is None:
                return False
        # jeśli plansza jest pełna, to sprawdzamy czy jest możliwość jakiegoś ruchu
        move_possible = self.can_move()
        # zwracamy negację aby zachować logiczny sens funkcji (jeśli nie ma ruchu, to game over)
        return not move_possible

    def can_move(self):
        # to tylko sprawdzenie - nie chcemy, by oryginalne pola uległy zmianie
        test_fields = deepcopy(self.board.fields)
        # sprawdzamy teoretyczną możliwość ruchu w każdym kierunku, jeśli jakiś jest możliwy to gra się nie kończy
        for key0 in ['1', '2', '3', '7', '8', '9']:
            _, invalid_move = self.p_one.move(key0, test_fields, False)
            if not invalid_move:
                return True
        return False


# uruchomienie gry
app = QApplication()
win = MainWindow()
win.show()
sys.exit(app.exec_())
