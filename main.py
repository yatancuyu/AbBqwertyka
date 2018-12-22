import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QPainter, QColor, QFont, QPen,QIcon
from PyQt5.QtCore import QTimer, Qt
import json
from random import choice

with open("l.json") as l,open('keyboard-set.json') as keyboard_set:
    keyboard = json.load(keyboard_set)
    data = json.load(l)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.screensize_x, self.screensize_y = 1500, 800
        self.setFixedSize(self.screensize_x, self.screensize_y)
        self.setWindowTitle('AБВqwertyKa')
        self.setWindowIcon(QIcon("icon.png"))
        self.move(50, 20)
        self.background = QLabel(self)
        self.background.setGeometry(0,0,1500,800)
        self.background.setStyleSheet("background-color:rgb(150,200,255)")

        self.hello_window = QLabel(self)
        self.hello_window.move(500, 100)
        self.dialogs = []

        self.current_word = 0
        self.test_result = QLabel(self)
        self.test_result.setGeometry(500, 250, 259, 260)
        self.inputer = QLineEdit(self)
        self.inputer.setGeometry(100, 460, 800, 30)
        self.inputer.setDisabled(True)


        self.test_words = [QLabel(self) for i in range(10)]
        self.test_statistics = [0, 0, 0, 0, 0, 0]
        self.statistics = [QLabel(self) for i in range(6)]

        self.timer = QTimer(self)
        self.time_show = QLabel(self)
        self.time_show.setFont(QFont("Arial", 20))
        self.time_show.setGeometry(900, 445, 100, 50)
        self.timer_start = False
        self.timer_value = 60

        self.start_ex = QPushButton("Начать", self)
        self.start_ex.setGeometry(1200, 500, 200, 50)
        self.start_ex.setDisabled(True)
        self.start_ex.setFont(QFont("Arial", 40))
        self.start_ex.hide()
        self.choice = ''
        self.levels_list = QComboBox(self)
        self.levels_list.setGeometry(1200, 300, 200, 50)
        self.levels_list.setStyleSheet('''border-width: 1px;
    padding: 1px;
    border-style: solid;
    border-color: rgb(0,170,255);
    border-radius: 5px;
''')
        self.level_programme = {}
        self.tutorialimg = QLabel(self)
        self.tutorialimg.setGeometry(200,0,953,800)
        self.tutorialimg.setStyleSheet("background-image: url(tutorial.jpg)")

        self.menu_buttons = []
        self.functions = [self.learning, self.test, self.exit]
        menu_buttons_text = ["Обучение", "Тестирование", "Выход"]
        for i in range(3):
            self.menu_buttons.append(QPushButton(menu_buttons_text[i], self))
            self.menu_buttons[i].setGeometry(self.screensize_x / 2.6, self.screensize_y / 3 + 90 * i, 200, 80)
            self.menu_buttons[i].clicked.connect(self.functions[i])
            self.menu_buttons[i].setStyleSheet('''                            
                             background-color: rgb({},{},{});         
                             border-width: 6px;            
                             border-radius: 10px;          
                             border-color: beige;          
                             font: italic   25px;          
                             min-width: 1em;               
                             padding: 5px; '''.format(200 + i * 5, 200 + i * 2, 255))
        self.back_menu = QPushButton("В Меню", self)
        self.back_menu.move(10, 20)
        self.back_menu.clicked.connect(self.menu)
        self.menu()


    def exit(self):
        self.close()


    def learning(self):
        self.clear()
        self.tutorialimg.show()
        self.dialogs = []
        with open("level_programmes.json") as j:
            self.level_programme = json.load(j)
        self.levels_list.clear()
        for i in range(9):
            if self.level_programme[str(i + 1) + " Уровень"][1]:
                self.levels_list.addItem(str(i + 1) + " Уровень\u2713")
            else:
                self.levels_list.addItem(str(i + 1) + " Уровень\u2715")
        self.levels_list.show()
        self.start_ex.show()
        self.levels_list.activated[str].connect(self.select)
        self.start_ex.clicked.connect(self.run)
        self.back_menu.show()


    def select(self, choice):
        self.choice = choice
        if self.level_programme[self.choice[:-1]][1]:
            self.start_ex.setEnabled(True)
        else:
            self.start_ex.setDisabled(True)


    def run(self):
        self.start_ex.setDisabled(True)
        print(self.level_programme[self.choice[:-1]]+[int(self.choice[0])])
        dialog = Keyboard(self.level_programme[self.choice[:-1]]+[int(self.choice[0])])
        dialog.show()
        self.dialogs.append(dialog)


    def test(self):
        self.clear()
        self.timer = QTimer(self)
        self.timer_start = False
        self.inputer.setEnabled(True)
        self.inputer.show()
        self.test_statistics = [0 for i in range(6)]
        self.timer_value = 60
        self.time_show.show()
        self.time_show.setText("1:00")
        self.refresh()
        self.inputer.setFont(QFont('Courier New', 16))
        self.back_menu.show()
        self.inputer.textEdited.connect(self.input)


    def refresh(self):
        self.current_word = 0
        prev = 100
        for i in range(10):
            self.test_words[i].show()
            self.test_words[i].setText(choice(data))
            self.test_words[i].setGeometry(prev, 400, len(self.test_words[i].text()) * 20, 32)
            prev += len(self.test_words[i].text()) * 20 + 1
            self.test_words[i].setFont(QFont('Courier-12', 20))
            self.test_words[i].setStyleSheet("color:none")


    def input(self):
        print("___")
        if not self.timer_start:
            self.timer_start = True
            self.timer.timeout.connect(self.on_timer)
            self.timer.start(1000)


        if ' ' in self.inputer.text():
            self.current_word += 1
            if self.inputer.text()[:-1] == self.test_words[self.current_word - 1].text():
                self.test_words[self.current_word - 1].setStyleSheet("color:green")
                self.test_statistics[4] += 1
            else:
                self.test_words[self.current_word - 1].setStyleSheet("color:red")
                self.test_statistics[5] += 1
            self.inputer.setText('')
        else:
            if not (self.test_words[self.current_word].text().startswith(self.inputer.text())):
                self.test_words[self.current_word].setStyleSheet("color:red")
                self.test_statistics[1] += 1
            elif self.test_words[self.current_word].text().startswith(self.inputer.text()):
                self.test_words[self.current_word].setStyleSheet("color:rgb(160,160,160)")
                self.test_statistics[2] += 1
        if self.current_word == 10:
            self.refresh()


    def on_timer(self):
        self.timer_value -= 1
        self.time_show.setText('0:' + str(self.timer_value).rjust(2, '0'))
        if self.timer_value == 0:
            self.timer.stop()
            self.result()


    def result(self):
        self.clear()
        self.back_menu.show()
        self.test_result.show()
        self.test_statistics[0] = int(self.test_statistics[4] * 1.1)
        self.test_statistics[3] = self.test_statistics[1] + self.test_statistics[2]
        self.test_result.setStyleSheet('background-image: url(resultimg.png)')
        coords = [((550, 265, 50, 50), QFont('Arial', 30), 'green'),
                  ((650, 333, 50, 50), QFont('Arial', 18), 'red'),
                  ((700, 333, 50, 50), QFont('Arial', 18), 'green'),
                  ((750, 333, 50, 50), QFont('Arial', 18), 'grey'),
                  ((750, 370, 50, 50), QFont('Arial', 18), 'green'),
                  ((750, 400, 50, 50), QFont('Arial', 18), 'red')]
        for i in range(6):
            self.statistics[i].show()
            self.statistics[i].setGeometry(*coords[i][0])
            self.statistics[i].setFont(coords[i][1])
            self.statistics[i].setStyleSheet('color:' + coords[i][2])
            self.statistics[i].setText(str(self.test_statistics[i]))


    def clear(self):
        for i in self.menu_buttons:
            i.hide()
            i.setDisabled(True)
        self.hello_window.hide()
        self.back_menu.hide()
        self.levels_list.hide()
        self.test_result.hide()
        self.tutorialimg.hide()
        for i in self.statistics:
            i.hide()
        for i in self.test_words:
            i.hide()
        self.time_show.hide()
        self.timer.stop()
        self.inputer.hide()
        self.inputer.setDisabled(True)
        self.inputer.setText('')
        self.start_ex.hide()
        self.inputer.setDisabled(True)


    def menu(self):
        self.clear()
        for i in self.menu_buttons:
            i.setEnabled(True)
            i.show()
        self.hello_window.show()


class Keyboard(QWidget):
    def __init__(self, text):
        super().__init__()
        self.dialog_data = text
        self.initUI()

    def initUI(self):
        """Cоздание клавиатуры и переменных учета"""
        self.move(50, 20)
        self.setFixedSize(1500, 800)
        self.setWindowTitle('Упражнение')
        self.setWindowIcon(QIcon("icon.png"))
        self.current_sign = 0
        self.before_start = True
        self.timer_value = 60
        self.timer = QTimer(self)
        self.time_show = QLabel("1:00", self)
        self.time_show.setGeometry(1000, 200, 300, 50)
        self.time_show.setFont(QFont("Arial", 30))
        self.text = self.dialog_data[0]
        self.keyboard = []
        self.mistake = False

        for i in range(0, 48, 12):
            for j in range(12):
                try:
                    self.keyboard.append(QLabel(self))
                    if i < 12:
                        self.keyboard[-1].setGeometry(340 + j * 60 + 1.5 * i, 500 + i * 5, 60, 60)
                    else:
                        self.keyboard[-1].setGeometry(400 + j * 60 + 1.5 * i, 500 + i * 5, 60, 60)
                    self.keyboard[-1].setText(keyboard[i + j][0])
                    if self.keyboard[-1].text() == self.text[0]:
                        self.keyboard[-1].setStyleSheet(self.set_style("grey"))
                        self.previoskey = [self.keyboard[-1], keyboard[i + j][1]]
                    else:
                        self.keyboard[-1].setStyleSheet(self.set_style(keyboard[i + j][1]))
                except Exception:
                    break
        self.keyboard.append(QLabel(" ", self))
        self.keyboard[-1].setGeometry(560, 740, 370, 60)
        self.keyboard[-1].setStyleSheet(self.set_style('green'))
        self.keyboard.append(QLabel("Backspace", self))
        self.keyboard[-1].setGeometry(1000, 500, 125, 60)
        self.keyboard[-1].setStyleSheet(self.set_style('orange'))
        self.show()
        self.begin_x = 400


    def set_style(self, color):
        """Создание стилистики клавиши"""
        return '''
                    background-color: {};
                    border-width: 6px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 20px;
                    min-width: 1em;
                    padding: 5px;
                '''.format(color)


    def paintEvent(self, event):
        """Создание вступительного текста"""
        qp = QPainter(self)
        if self.before_start:
            qp.setPen(QColor(168, 8, 9))
            qp.setFont(QFont('Courier New', 20))
            qp.drawText(350, 0, 800, 500, Qt.AlignCenter, '''Чтобы выйти, нажмите Esc
            \n Положите пальцы в базовую позицию А|О\nНажмите клавишу, чтобы начать.''')

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 400, 1500, 80)

        qp.setPen(QPen(Qt.black, 5))
        qp.drawRect(400, 400, 50, 80)

        self.drawText(event, qp)


    def drawText(self, event, qp):
        """Создание и движение текста по горизонтали"""

        current_x = self.begin_x
        current_x += 48 * self.current_sign
        for i in range(self.current_sign, len(self.text)):
            qp.setPen(QColor(0, 0, 0))
            qp.setFont(QFont('Courier New', 60))
            qp.drawText(current_x, 400, 1500, 80, Qt.AlignLeft, self.text[i])
            current_x += 48


    def keyPressEvent(self, event):
        """Мезанизм подсвечивания клавиш на клавиатуре"""
        if event.key() == Qt.Key_Escape:
            self.close()
        if self.current_sign < len(self.text):
            if self.before_start:
                self.timer.timeout.connect(self.on_timer)
                self.timer.start(1000)
                self.before_start = False
                self.taunt_event()
            if event.key() == Qt.Key_Backspace and self.mistake:
                self.mistake = False
                self.keyboard[-1].setStyleSheet(self.set_style("orange"))

            if self.previoskey:
                self.previoskey[0].setStyleSheet(self.set_style(self.previoskey[1]))
                self.previoskey = []
            if event.key() == Qt.Key_Space:
                if self.text[self.current_sign] == ' ':
                    self.current_sign += 1
                    self.begin_x -= 48
                    self.taunt_event()
                else:
                    self.keyboard[-2].setStyleSheet(self.set_style('red'))
                    self.previoskey = [self.keyboard[-2], 'green']

            for i in range(len(self.keyboard[:-2])):
                try:
                    if self.keyboard[i].text() == chr(event.key()).lower():
                        if self.keyboard[i].text() != self.text[self.current_sign]:
                            self.keyboard[i].setStyleSheet(self.set_style("red"))
                            self.mistake = True
                            self.keyboard[-1].setStyleSheet(self.set_style("grey"))
                            self.previoskey = [self.keyboard[i], keyboard[i][1]]
                            self.taunt_event()

                        elif self.keyboard[i].text() == self.text[self.current_sign] and not(self.mistake):
                            self.current_sign += 1
                            self.begin_x -= 48
                            self.taunt_event()
                        break
                except Exception:
                    continue

            for i in range(len(self.keyboard[:-1])):
                print(i)
                try:
                    if self.current_sign < len(self.text) \
                            and self.text[self.current_sign] == self.keyboard[i].text() and not (self.mistake):
                        self.keyboard[i].setStyleSheet(self.set_style("grey"))
                        self.previoskey = [self.keyboard[i], keyboard[i][1]]
                except Exception:
                    self.previoskey = [self.keyboard[i],"green"]
        if self.current_sign == len(self.text):
            self.timer.stop()
            self.finish()


    def finish(self):
        """Итог"""
        for i in self.keyboard:
            i.hide()
        self.taunt_event()
        if self.current_sign == len(self.text):
            self.time_show.setText("ЗАЧТЕНО\u2713")
            self.time_show.setStyleSheet("color: green")
            if self.dialog_data[2] < 7:
                with open("level_programmes.json") as programme:
                    level = json.load(programme)
                    print(level[str(self.dialog_data[2] + 1) + " Уровень"][1])
                    level[str(self.dialog_data[2] + 1) + " Уровень"][1] = True
                with open("level_programmes.json", "w") as programme:
                    json.dump(level, programme)
        else:
            self.time_show.setText("НЕ ЗАЧТЕНО\u2715")
            self.time_show.setStyleSheet("color: red")


    def on_timer(self):
        """Cчет времени"""
        self.timer_value -= 1
        self.time_show.setText('0:' + str(self.timer_value).rjust(2, '0'))
        if self.timer_value == 0:
            self.timer.stop()
            self.finish()


    def taunt_event(self):
        """Принудительный вызов PaintEvent"""
        self.setFixedSize(1500, 801)
        self.setFixedSize(1500, 800)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
