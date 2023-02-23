# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import sys
import pandas as pd
import random
from copy import deepcopy


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quizlet low version")

        self.setGeometry(100, 100, 1000, 500)

        with open('cards.txt', 'r') as f:
            self.cards = f.readlines()
            for i in range(len(self.cards)):
                self.cards[i] = self.cards[i].rstrip()

        self.UiComponents()

        self.show()

        self.number = 0

    def UiComponents(self):

        menu = QWidget()
        menu_lay = QVBoxLayout()
        self.head = QLabel("Main Menu", self)
        self.need_save = 0

        self.head.setGeometry(350, 10, 300, 60)

        font = QFont('Times', 14)
        font.setBold(True)

        self.head.setFont(font)

        self.head.setAlignment(Qt.AlignCenter)

        color = QGraphicsColorizeEffect(self)
        color.setColor(Qt.darkCyan)
        self.head.setGraphicsEffect(color)

        self.info = QLabel("Welcome", self)

        self.info.setGeometry(375, 85, 100, 60)

        self.info.setWordWrap(True)

        self.info.setFont(QFont('Times', 13))
        self.info.setAlignment(Qt.AlignCenter)

        self.info.setStyleSheet("QLabel"
                                "{"
                                "border : 2px solid black;"
                                "background : lightgrey;"
                                "}")


        self.check = QPushButton("Create", self)
        self.check.setMinimumHeight(100)

        self.check.setGeometry(375, 235, 250, 60)

        self.check.clicked.connect(self.create_action)

        self.start = QPushButton("Start", self)
        self.start.setMinimumHeight(100)

        self.start.clicked.connect(self.start_action)

        menu_lay.addWidget(self.head)
        menu_lay.addWidget(self.info)
        menu_lay.addWidget(self.check)
        menu_lay.addWidget(self.start)
        menu.setLayout(menu_lay)
        self.setCentralWidget(menu)

    def start_action(self):
        with open('cards.txt', 'r') as f:
            self.cards = f.readlines()
            for i in range(len(self.cards)):
                self.cards[i] = self.cards[i].rstrip()
        self.need_save = 0
        self.centralWidget().deleteLater()
        self.layout = QFormLayout()
        card_num = self.cards[1::3]
        status = self.cards[2::3]
        i=0
        groupBox = QGroupBox()
        for col in self.cards[::3]:
            col = col.rstrip()
            but1 = QPushButton(col)
            but1.setMinimumHeight(30)
            widg = QWidget()
            widg_l = QHBoxLayout()
            widg_l.addWidget(QLabel('Number of Cards: ' + str(card_num[i])))
            widg_l.addWidget(QLabel('Current Progress: ' + str(status[i])))
            widg.setLayout(widg_l)
            self.layout.addRow(but1)
            self.layout.addRow(widg)
            print(deepcopy(col))
            but1.clicked.connect(lambda: self.start_game(deepcopy(but1.sender().text())))
            i+=1
        groupBox.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        self.layout.setContentsMargins(1, 1, 1, 1)
        scroll.setWidgetResizable(True)
        layout_scr = QVBoxLayout()
        layout_scr.addWidget(QLabel('Your cards'))
        layout_scr.addWidget(scroll)
        self.window = QWidget()
        self.window.setLayout(layout_scr)
        self.setCentralWidget(self.window)
        self.show()


    def start_game(self, name):
        self.need_save = 1
        self.name = name
        print(name)
        self.centralWidget().deleteLater()
        with open("Quizlets/" + name + '.txt', 'r') as f:
            data = f.read()
        self.words = []
        self.answers = []
        self.progress = []
        self.word = 0
        for k in data.split('\n\n'):
            pair = k.split('---')
            if len(pair) == 1:
                continue
            self.words.append(pair[0])
            self.answers.append(pair[1])
            if len(pair) == 3:
                self.progress.append(int(pair[2]))
            else:
                self.progress.append(0)
        self.centr_label = QLabel()
        self.answer_widget = QWidget()
        self.upper_line = QWidget()
        but_ret = QPushButton('Return to cards')
        but_ret.clicked.connect(self.save_results)
        but_ret.clicked.connect(self.start_action)
        but_reset = QPushButton('Restart quiz')
        but_reset.clicked.connect(self.restart_game)
        up_layout = QHBoxLayout()
        up_layout.addWidget(QLabel('Title: ' + name))
        up_layout.addWidget(but_ret)
        up_layout.addWidget(but_reset)
        self.upper_line.setLayout(up_layout)
        self.progress_widget = QWidget()
        self.lcd1 = QLCDNumber()
        self.lcd2 = QLCDNumber()
        self.lcd3 = QLCDNumber()
        bar_prog_layout = QHBoxLayout()
        bar_prog_layout.addWidget(self.lcd1)
        bar_prog_layout.addWidget(self.lcd2)
        bar_prog_layout.addWidget(self.lcd3)
        self.bar1 = QProgressBar()
        self.bar2 = QProgressBar()
        self.bar3 = QProgressBar()
        bars_layout = QVBoxLayout()
        bars_layout.addWidget(self.bar1)
        bars_layout.addWidget(self.bar2)
        bars_layout.addWidget(self.bar3)
        inter_widg = QWidget()
        inter_widg.setLayout(bars_layout)
        bar_prog_layout.addWidget(inter_widg)
        self.progress_widget.setLayout(bar_prog_layout)
        self.update_progress()
        self.total = QWidget()
        total_layout = QVBoxLayout()
        total_layout.addWidget(self.upper_line)
        total_layout.addWidget(self.centr_label)
        total_layout.addWidget(self.answer_widget)
        total_layout.addWidget(self.progress_widget)
        self.answer_widget.setLayout(QVBoxLayout())
        self.total.setLayout(total_layout)
        self.setCentralWidget(self.total)
        self.centr_label.setAlignment(Qt.AlignCenter)
        self.next_word()


    def restart_game(self):
        self.progress = [0 for i in range(len(self.words))]
        self.word=0
        self.update_progress()
        self.next_word()

    def update_progress(self):
        i = 0
        c = 0
        r = len(self.progress)
        for k in self.progress:
            if k == 5:
                i += 1
            elif k>=2:
                c += 1
        self.lcd1.display(i)
        self.lcd2.display(c)
        self.lcd3.display(r-c-i)
        self.bar1.setValue(int(i*100/r))
        self.bar2.setValue(int(c*100/r))
        self.bar3.setValue(int((r-c-i)*100/r))
        pass

    def next_word(self):
        if self.word >= len(self.answers):
            self.word = 0
        k = self.progress[self.word]
        i = 0
        d = len(self.progress)
        while k==5:
            self.word += 1
            if self.word >= len(self.answers):
                self.word = 0
            k = self.progress[self.word]
            i+=1
            if i == d:
                self.quiz_done()
                return
        self.centr_label.setStyleSheet('')
        self.centr_label.setText(self.words[self.word])
        self.centr_label.setFont(QFont('Times', 23))
        print(1)
        for i in reversed(range(self.answer_widget.layout().count())):
            self.answer_widget.layout().itemAt(i).widget().deleteLater()

        if self.progress[self.word] <= 2:
            resss = random.randint(0, 3)
            a = []
            a.append(self.word)
            c = self.word
            for nbut in range(4):
                if nbut == resss:
                    tx_but = self.answers[self.word]
                    but = QPushButton(tx_but)
                    but.clicked.connect(self.true_answer)
                else:
                    while c in a:
                        c = random.randint(0, d-1)
                    a.append(c)
                    tx_but = self.answers[c]
                    but = QPushButton(tx_but)
                    but.clicked.connect(self.wrong_answer)
                self.answer_widget.layout().addWidget(but)
        else:
            self.ans_wind = QTextEdit()
            self.answer_widget.layout().addWidget(self.ans_wind)
            but1 = QPushButton('Next')
            but1.clicked.connect(self.check_answer)
            self.answer_widget.layout().addWidget(but1)

    def check_answer(self):
        if self.ans_wind.toPlainText() in self.answers[self.word] and len(self.ans_wind.toPlainText()) >= 3:
            self.true_answer()
        else:
            self.wrong_answer()

    def wrong_answer(self):
        if self.progress[self.word] != 0:
            self.progress[self.word] -= 1
        self.update_progress()
        self.centr_label.setStyleSheet("QLabel"
                                "{"
                                "background : red;"
                                "}")
        self.show_answer()

    def true_answer(self):
        self.progress[self.word] += 1
        self.update_progress()
        self.centr_label.setStyleSheet("QLabel"
                                "{"
                                "border : 2px solid black;"
                                "background : green;"
                                "}")
        self.show_answer()

    def show_answer(self):
        self.centr_label.setText(self.answers[self.word])
        self.centr_label.setFont(QFont('Times', 23))
        self.word += 1
        new_lay = QHBoxLayout()
        but1 = QPushButton('Next')
        but1.clicked.connect(self.next_word)
        for i in reversed(range(self.answer_widget.layout().count())):
            self.answer_widget.layout().itemAt(i).widget().deleteLater()
        self.answer_widget.layout().addWidget(but1)

    def quiz_done(self):
        for i in reversed(range(self.answer_widget.layout().count())):
            self.answer_widget.layout().itemAt(i).widget().deleteLater()
        self.centr_label.setText('You are done!')
        self.update_progress()
        self.centr_label.setFont(QFont('Times', 23))

    def save_results(self):
        res_str=''
        for i in range(len(self.progress)):
            if self.words[i] == self.words[i]:
                res_str += self.words[i] + '---' + self.answers[i] +'---'+ str(self.progress[i]) + '\n\n'
        with open('Quizlets/'+self.name+'.txt', 'w') as f:
            f.write(res_str)

        with open('cards.txt', 'r') as f:
            k = f.readlines()
            for i in range(len(k)):
                k[i] = k[i].rstrip()
        cards = k[::3]
        print(cards)
        if self.name in cards:
            print('true')
            print(self.name)
            ind = cards.index(self.name)
            print(ind)
            k[1+3*ind] = len(self.progress)
            i=0
            for g in self.progress:
                if g == 5:
                    i+=1
            k[3*ind+2] = i/k[3*ind+1]
        else:
            print('false')
            print(self.name)
            k.append(self.name)
            k.append(len(self.progress))
            i=0
            for g in self.progress:
                if g == 5:
                    i+=1
            k.append(i/len(self.progress))
        string=''
        for name in k:
            string += str(name) + '\n'
        with open('cards.txt', 'w') as f:
            f.write(string)


    def create_action(self):
        self.centralWidget().deleteLater()
        total = QWidget()
        total_lay = QVBoxLayout()
        upper_level = QWidget()
        upper_level_lay = QHBoxLayout()
        but1 = QPushButton('Save')
        but2 = QPushButton('Delete')
        upper_level_lay.addWidget(but1)
        upper_level_lay.addWidget(but2)
        upper_level.setLayout(upper_level_lay)
        total_lay.addWidget(upper_level)
        self.title_new = QTextEdit('')
        self.title_new.setMaximumHeight(25)
        but1.clicked.connect(self.save_new)
        but1.clicked.connect(self.go_to_menu)
        but2.clicked.connect(self.go_to_menu)
        total_lay.addWidget(self.title_new)
        row2 = QWidget()
        row2_lay = QHBoxLayout()
        but3 = QPushButton("Добавить ячейки")
        tex = QTextEdit()
        tex.setMaximumHeight(25)
        row2_lay.addWidget(but3)
        row2_lay.addWidget(tex)
        but3.clicked.connect(lambda: self.add_boxes(int(tex.toPlainText())))
        row2.setLayout(row2_lay)
        total_lay.addWidget(row2)
        groupBox = QGroupBox()
        self.group_lay = QFormLayout()
        groupBox.setLayout(self.group_lay)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        total_lay.addWidget(scroll)
        total.setLayout(total_lay)
        self.setCentralWidget(total)
        self.k=0
        self.add_boxes(4)

    def add_boxes(self, i):
        for _ in range(i):
            new1 = QWidget()
            new1_lay = QHBoxLayout()
            word = QTextEdit()
            word.setObjectName('word_' + str(self.k))
            answ = QTextEdit()
            answ.setObjectName('answ_'+str(self.k))
            self.k += 1
            new1_lay.addWidget(word)
            new1_lay.addWidget(answ)
            new1.setLayout(new1_lay)
            self.group_lay.addRow(new1)

    def save_new(self):
        self.words = []
        self.progress = []
        self.answers = []
        i=0
        for k in self.findChildren(QTextEdit)[2:]:
            if i%2 == 0:
                self.words.append(k.toPlainText())
                self.progress.append(0)
            else:
                self.answers.append(k.toPlainText())
            i+=1


        self.name = self.title_new.toPlainText()
        self.save_results()

    def reset_action(self):
        self.info.setStyleSheet("QLabel"
                                "{"
                                "border : 2px solid black;"
                                "background : lightgrey;"
                                "}")

        self.info.setText("Welcome")

    def go_to_menu(self):
        self.centralWidget().deleteLater()
        self.UiComponents()

    def closeEvent(self, *args, **kwargs):
        if self.need_save == 1:
            self.save_results()



App = QApplication(sys.argv)

window = Window()

sys.exit(App.exec())