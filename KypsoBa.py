# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import traceback
import sqlite3 as lite
style = ('''
QMenu {
    background-color: white;
    margin: 2px; /* some spacing around the menu */
}

QMenu::item {
    padding: 2px 25px 2px 20px;
    border: 1px solid transparent; /* reserve space for selection border */
}

QMenu::item:selected {
    border-color: darkblue;
    background: rgba(100, 100, 100, 150);
}

QMenu::icon:checked { /* appearance of a 'checked' icon */
    background: gray;
    border: 1px inset gray;
    position: absolute;
    top: 1px;
    right: 1px;
    bottom: 1px;
    left: 1px;
}

QMenu::separator {
    height: 2px;
    background: lightblue;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::indicator {
    width: 13px;
    height: 13px;
}


QMenuBar {
    font: bold;
    color: black;
    background-color:  rgba(255,255,255,0.7);
}
QMenuBar::item {
    spacing: 3px; /* spacing between menu bar items */
    padding: 1px 4px;
    background: transparent;
    border-radius: 4px;
}

QMenuBar::item:selected { /* when selected using mouse or keyboard */
    background: white;
}

QMenuBar::item:pressed {
    background: white;
}
QLabel{
    font: bold 16px;
    color: black;
    background-color: rgba(255,255,255,0.7);
    border: 1px solid darkblue;
    border-radius: 10px;
    padding: 2px;
}
QLineEdit {
    border: 2px solid black;
    border-radius: 10px;
    padding: 0 8px;
    background: white;
    selection-background-color: darkgray;
}   

QPushButton {
    background-color: lightblue;
    border-style: outset;
    border-width: 4px;
    border-radius: 10px;
    border-color: blue;
    font: bold 12px;
    min-width: 5em;
    padding: 6px;
}
QPushButton:pressed {
    background-color: rgb(148, 148, 148);
    border-style: inset;
}
QComboBox {
    font: bold;
    border: 2px solid gray;
    border-radius: 8px;
    border-color: black;
    padding: 2px 18px 2px 3px;
    min-width: 6em;
}


QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
    image: url(downarrow1.png); width: 20px; hight: 20px; 
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
QComboBox QAbstractItemView {
    border: 2px solid darkgray;
    selection-background-color: lightgray;
}
}''')
def calculations(k, b, d1, text):
    bb = 'Розрахунок припусків для циліндричної повехні ' + str(d1) + b + str(k)
    bb = bb + '\n\n   Розрахунок мінімального симетричного припуску:\n2 ∙ 𝑍𝑚𝑖𝑛 = 2 ∙ (𝑅𝑧𝑖−1 + 𝑇𝑖−1 + √𝜌𝑖−1^2 + e𝑖^2)\n\n'
    r = []
    t = []
    p = []
    e = []
    z = []
    kvalitet = []
    dopusk = []
    promezutki = [[0, 3], [3, 6], [6, 10], [10, 18], [18, 30], [30, 50], [50, 80], [80, 120], [120, 180],
                  [180, 250], [250, 315], [315, 400], [400, 500]]
    promezutok = []
    con = lite.connect('database.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM zagotovka WHERE name = '{}'".format(text))
        row = cur.fetchone()
        r.append(row[1])
        t.append(row[2])
        p.append(row[3])
        e.append(row[4])
        kvalitet.append(row[5])
        for i in promezutki:
            if i[0] < d1 <= i[1]:
                promezutok.append(i[0])
                promezutok.append(i[1])
        cur.execute("SELECT * FROM kvalitet WHERE d = {} and d1 = {}".format(promezutok[0], promezutok[1]))
        row = cur.fetchone()
        dopusk.append(row[kvalitet[0] + 2])
    if k in [5, 6]:
            operations = ["Точіння чорнове", "Точіння напівчистове","Точіння чистове","Полірування"]
    elif k == 7:
            operations = ["Точіння чорнове", "Точіння напівчистове","Точіння чистове","Шліфування"]
    elif k in [8, 9]:
            operations = ["Точіння чорнове", "Точіння напівчистове","Точіння чистове"]
    elif k in [10, 11]:
            operations = ["Точіння чорнове", "Точіння напівчистове"]
    elif k == 12:
            operations = ["Точіння чорнове"]
    with con:
        cur = con.cursor()
        for operation in operations:
            cur.execute("SELECT * FROM operations WHERE name = '{}'".format(operation))
            row = cur.fetchone()
            r.append(row[1])
            t.append(row[2])
            p.append(row[3])
            e.append(row[4])
            kvalitet.append(row[5])
    for i in range(1, len(r)):
        cur.execute("SELECT * FROM kvalitet WHERE d = {} and d1 = {}".format(promezutok[0], promezutok[1]))
        row = cur.fetchone()
        dopusk.append(row[kvalitet[i] + 2])
        z1 = r[i - 1] + t[i - 1] + (p[i - 1] ** 2 + e[i] ** 2) ** (1 / 2)
        z.append(round(z1, 2))
        bb = bb + operations[i - 1] + ":  2 ∙ Zmin = 2*("+str(r[i-1])+"+"+str(t[i-1]) + "+√("+ str(p[i-1])+"^2+"+str(e[i])+ "^2)) = 2 ∙ " + str(z[i - 1]) + " (мкм)\n"
    bb = bb + '\n                     Розрахунок проміжного розміру:\nМінімальний:   Anmin = Amin - 2 ∙ Zmin - δ\n\n'
    operations = ['Заготівка'] + operations
    Amin = d1
    for i in range(len(dopusk) - 2, -1, -1):
        Anmin = Amin - 2 * 0.001 * z[i - 1] - dopusk[i] * 0.001  #
        bb = bb + operations[i] + ":   Anmin = " + str(round(Amin,2))+"+"+str(round(0.001*z[i-1],2))+"-"+str(round(dopusk[i]*0.001,2))+" = " +str(round(Anmin, 2)) + ' (мм)\n'
        Amin = Anmin
    Amax = d1
    bb = bb + '\nМаксимальний:   Anmax = Anmax + δ\n\n'
    for i in range(len(dopusk) - 1, -1, -1):
        Anmax = Amax + dopusk[i] * 0.001  
        bb = bb + operations[i] + ":   Anmax = " + str(round(Amax,2))+"+"+str(round(dopusk[i]*0.001,2))+" = "+str(round(Anmax, 2)) + ' (мм)\n'
        Amax = Anmax
    bb = bb + '\n                     Максимальний симетричний припуск\n2 ∙ Zmax = 2 ∙ Zmin + δi-1 - δi\n\n'
    z2 = []
    for i in range(1, len(dopusk)):
        Zmax = 2 * z[i - 1] + dopusk[i - 1] - dopusk[i]
        z2.append(round(Zmax, 2))
        bb = bb + operations[i] + ":   2 ∙ Zmax = "+str(z[i-1])+"+"+str(dopusk[i-1])+"-"+str(dopusk[i])+" = " + str(round(Zmax, 2)) + ' (мкм)\n'
    dop = round(dopusk[0] - dopusk[len(dopusk) - 1], 2)
    bb = bb + '\n                                           Перевірка:\nδз - δд = '+ str(dopusk[0])+"-" + str(dopusk[len(dopusk) - 1])+" = " + str(dop) + '(мкм)'
    bb = bb + '\nΣ2 ∙ Zmax - Σ2 ∙ Zmin = '
    sumz2 = 0
    for i in range(len(z2)):
        sumz2 = sumz2 + z2[i]
    sumz = 0
    for i in range(len(z)):
        sumz = sumz + 2 * z[i]
    zz = round(sumz2 - sumz, 2)
    bb = bb + str(round(sumz2,2))+"-"+str(round(sumz,2)) + " = "
    bb = bb + str(zz) + '(мкм)\n'
    if zz == dop:
        bb = bb + 'Отже, розрахунки були проведено правильно.'
    else:
        bb = bb + 'Отже, отже десь в розрахунках була похибка.'

    return [bb,750,400]
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
def input_check(diametr,zagotovka,bukwa,kvalitet):
    try:
        if diametr == '':
            return ["Ви нічого не ввели.",191,50]
        elif isint(diametr):
                    diametr = int(diametr)
                    if diametr < 1 or diametr > 200:
                        return ["Введіть діаметр отвору в межах від 1 до 200.",420,50]
                    else:
                        return calculations(kvalitet,bukwa,diametr,zagotovka)
        elif isfloat(diametr):
                    diametr = float(diametr)
                    if diametr < 1 or diametr > 200:
                        return ["Введіть діаметр отвору в межах від 1 до 200.",500,50]
                    else:
                        return calculations(kvalitet,bukwa,diametr,zagotovka)
        else:
            return ["Ви неправильно ввели дані.\nСпробуйте ще раз.",265,72]          
    except Exception:
        kek = str(traceback.format_exc())
        print(kek)
        return ["Ви неправильно ввели дані.\nСпробуйте ще раз.",265,72]
class main_menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tx = ["Матеріал"]
        self.initUI()
        self.lbl1 = None

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('')
        exitAction = QAction(QIcon('exit.png'), '&Вийти', self)
        exitAction.setShortcut('Ctrl+X')
        exitAction.triggered.connect(qApp.quit)
        Action = QAction(QIcon('help.png'), '&Допомога', self)
        Action.setShortcut('Ctrl+H')
        Action.triggered.connect(self.help)
        Action1 = QAction(QIcon('info.png'), '&Інформація', self)
        Action1.setShortcut('Ctrl+A')
        Action1.triggered.connect(self.info)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu1 = menubar.addMenu('&Довідка')
        fileMenu.addAction(Action)
        fileMenu.addAction(exitAction)
        fileMenu1.addAction(Action1)
        font = QFont()
        font.setFamily("Helvetica")
        self.qbtn = QPushButton('Вийти', self)
        self.qbtn.setFont(font)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        self.qbtn.move(400, 300)

        self.btn = QPushButton('Розрахувати', self)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.on_click)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(25, 300)
#Кватитет
        self.lbl1 = QLabel('Бажаний квалітет точності', self)
        self.lbl1.setFont(font)
        self.lbl1.move(25, 150)
        self.lbl1.adjustSize()
#Размер детали
        self.lbl2 = QLabel('Кінцевий розмір деталі', self)
        self.lbl2.setFont(font)
        self.lbl2.setToolTip('В межах 1-200')
        self.lbl2.move(25, 250)
        self.lbl2.adjustSize()
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setPlaceholderText("Наприклад: 40")
        self.lineEdit1.setGeometry(QRect(300, 248, 150, 30))
        self.setFixedSize(510, 350)
        self.center()
#способ получения
        self.exPopup1 = ComboWidget(self)
        self.exPopup2 = ComboWidget1(self)
        self.lb3 = QLabel('Спосіб отримання заготовки', self)
        self.lb3.setFont(font)
        self.lb3.move(25, 50)
        self.lb3.adjustSize()
#материал
        self.lbl2 = QLabel('Матеріал', self)
        self.lbl2.setFont(font)
        self.lbl2.move(25, 100)
        self.lbl2.adjustSize()
        self.setWindowIcon(QIcon('web1.png'))
        oImage = QImage("fon.png")
        sImage = oImage.scaled(QSize(500, 350))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.setWindowTitle("Розрахунок припусків на обробку та міжопераційних розмірів циліндричних поверхонь")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def help(self):
        QMessageBox.question(self, 'Допомога:',
                             'Для виконання необхідних розрахунків виберіть варінти із вже представлених та введіть правильно дані у комірку, що відповідає розміру (діаметру) деталі',
                             QMessageBox.Ok,
                             QMessageBox.Ok)

    @pyqtSlot()
    def info(self):
        QMessageBox.question(self, 'Інформація про програму:',
                             'Курсова робота \n3 курс (2 семестр) ІП-з72\n©Третяк О.В.', QMessageBox.Ok,
                             QMessageBox.Ok)

    @pyqtSlot()
    def on_click(self):
        diametr = self.lineEdit1.text()
        try:
            zagotovka = str(self.exPopup1.comboA.currentText())
            bukwa = str(self.exPopup2.comboA.currentText())
            kvalitet = int(self.exPopup2.comboB.currentText())
            inpu = input_check(diametr,zagotovka,bukwa,kvalitet)
            exPopup = answer_menu(inpu[0],self)
            exPopup.setFixedSize(inpu[1], inpu[2])
            exPopup.setWindowTitle("Отримані результати")
            exPopup.show()
            self.lineEdit1.setText("")
        except Exception:
            print(str(traceback.format_exc()))

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Ви впевнені?',
                                     "Ви впевнені?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
class answer_menu(QMainWindow):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.initUI()

    def initUI(self):
        self.label = QLabel(self.name, self)
        self.label.move(95, 22)
        self.label.setStyleSheet("""
                                                    font: bold;
                                                    font-size: 17px;
                                                    color: black;
                                                    background-color: white;
                                                """)
        # self.label.adjustSize()
        exitAction = QAction(QIcon('exit.png'), '&Вийти', self)
        exitAction.setShortcut('Ctrl+X')
        exitAction.triggered.connect(qApp.quit)
        Action = QAction(QIcon('help.png'), '&Допомога', self)
        Action.setShortcut('Ctrl+H')
        Action.triggered.connect(self.help)
        Action1 = QAction(QIcon('info.png'), '&Інформація', self)
        Action1.setShortcut('Ctrl+A')
        Action1.triggered.connect(self.info)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu1 = menubar.addMenu('&Довідка')
        fileMenu.addAction(Action)
        fileMenu.addAction(exitAction)

        fileMenu1.addAction(Action1)

        self.scroll = QScrollArea(self)
        self.scroll.setGeometry(0, 22, 750, 380)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidget(self.label)

        self.setWindowIcon(QIcon('web2.png'))

        oImage = QImage("image.jpg")
        sImage = oImage.scaled(QSize(600, 400))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    @pyqtSlot()
    def help(self):
        QMessageBox.question(self, 'Допомога',
                             'Побачили помилку в підрахунках - повідомне автору(info).',
                             QMessageBox.Ok,
                             QMessageBox.Ok)

    @pyqtSlot()
    def info(self):
        QMessageBox.question(self, 'Інформація про програму',
                             'Курсова робота\n4 курс (1 семестр)\n©Третяк О.В.', QMessageBox.Ok,
                             QMessageBox.Ok)
class ComboWidget(QWidget):

    def __init__(self, parent=None):
        super(ComboWidget, self).__init__(parent)
        self.setGeometry(300, 24, 200, 130)
        self.var = ["Лиття в кокіль", "Лиття відцентрове", "Лиття за виплавленими моделями", "Лиття під тиском", "Лиття в оболонкові форми", "Гаряча штамповка", "Холодна штамповка", "Прокат"]
        self.litio = ['АЛ2 ГОСТ 21488-76', 'АЛ9 ГОСТ 1583-93', 'АЛ9 ГОСТ 21488-76', 'Сталь 08ГДНФЛ ГОСТ 977-75',
                      'Сталь 10Х18H9Л ГОСТ 977-75', 'Сталь 12ДН2ФЛ ГОСТ 977-75', 'Сталь 15Л ГОСТ 977-75',
                      'Сталь 20Г1ФЛ ГОСТ 977-75', 'Сталь 20ГЛ ГОСТ 977-75', 'Сталь 20ГНМФЛ ГОСТ 977-75',
                      'Сталь 20ДХЛ ГосТ 977-75', 'Сталь 20Л ГОСТ 977-75', 'Сталь 20ФЛ ГОСТ 977-75',
                      'Сталь 20ХМЛ гоСТ 977-75', 'Сталь 25Л ГОСТ 977-75', 'Сталь 30ГСЛ ГосТ 977-75',
                      'Сталь 30Л ГОСТ 977-75', 'Сталь 3СХГСФЛ ГОСТ 977-75', 'Сталь 3СХНМЛ ГОСТ 977-75',
                      'Сталь 32X06Л госТ 977-75', 'Сталь 35ГЛ ГОст 977-75', 'Сталь 35Л ГОСТ 977-75',
                      'Сталь 35НГМЛ ГосТ 977-75', 'Сталь 35ХГСЛ ГОСТ 977-75', 'Сталь 35ХМЛ ГосТ 977-75',
                      'Сталь 40Л ГОСТ 977-75', 'Сталь 40НМА ГосТ 977-75', 'Сталь 40НМЛ гоСТ 977-75',
                      'Сталь 4024H12CЛ ГОСТ 977-75', 'Сталь 40ХЛ ГОст 97-75', 'Сталь 45ГЛ ГОСТ 977-75',
                      'Сталь 45Л ГОСТ 977-75', 'Сталь 45ФЛ ГОСТ 977-75', 'Сталь 50Л ГОСТ 977-75',
                      'Сталь 55Л ГОСТ 977-75']
        self.shtamp1 = ['Сталь 5XB2C ГОсТ 5950-73', 'Сталь БXВ2С ГОсТ 5950-73', 'Сталь 6ХВГ ГОСТ 5950-73',
                        'Сталь X12 ГОСТ 5950-73', 'Сталь X12BM ГОСТ 5950-73', 'Сталь X12МФ ГОСТ 5950-73',
                        'Сталь X12Ф1 ГОСТ 5950-73']
        self.shtamp2 = ['Сталь Ст5сп2 ГОсТ 10884-81', 'Сталь 35ГС ГОсТ 10884-81', 'Сталь 25Г2С ГОсТ 10884-81',
                        'Сталь 18Г2С ГОсТ 10884-81', 'Сталь 80С ГОсТ 10884-81', 'Сталь 20Х2Г2СР ГОсТ 10884-81',
                        'Сталь 23Х3Г2Ц ГОсТ 10884-81']
        self.prokat = ['Сталь Ст0 ГОсТ 380-71', 'Сталь Ст1 ГОсТ 380-71', 'Сталь Ст2 ГОсТ 380-71',
                      'Сталь Ст3 ГОсТ 380-71']
        layout = QVBoxLayout(self)

        self.comboA = QComboBox()
        # The second addItem parameter is itemData, which we will retrieve later
        self.comboA.addItem(self.var[0], self.litio)
        self.comboA.addItem(self.var[1], self.litio)
        self.comboA.addItem(self.var[2], self.litio)
        self.comboA.addItem(self.var[3], self.litio)
        self.comboA.addItem(self.var[4], self.litio)
        self.comboA.addItem(self.var[5], self.shtamp1)
        self.comboA.addItem(self.var[6], self.shtamp2)
        self.comboA.addItem(self.var[7], self.prokat)
        self.comboA.currentIndexChanged.connect(self.indexChanged)
        font = QFont()
        font.setFamily("Helvetica")
        self.comboA.setFont(font)
        layout.addWidget(self.comboA)

        self.comboB = QComboBox()
        self.comboB.setFont(font)
        self.comboB.adjustSize()
        self.indexChanged(self.comboA.currentIndex())
        layout.addWidget(self.comboB)
        self.show()

    def indexChanged(self, index):
        self.comboB.clear()
        data = self.comboA.itemData(index)
        if data is not None:
            self.comboB.addItems(data)
class ComboWidget1(QWidget):

    def __init__(self, parent=None):
        super(ComboWidget1, self).__init__(parent)
        self.setGeometry(300, 132, 130, 100)
        self.var = ["b", "d", "e", "f", "g", "h", "js", "k", "n", "r", "s", "u"]
        self.b = ["12"]
        self.d = ['9', '10', '11']
        self.e = ['8', '9']
        self.f = ['7', '9']
        self.g = ['6']
        self.h = ['5', '6', '7', '8', '9', '11', '12']
        self.js = ['6']
        self.k = ['6']
        self.n = ['6']
        self.r = ['6']
        self.s = ['7']
        self.u = ['8']
        layout = QVBoxLayout(self)

        self.comboA = QComboBox()
        # The second addItem parameter is itemData, which we will retrieve later
        self.comboA.addItem(self.var[0], self.b)
        self.comboA.addItem(self.var[1], self.d)
        self.comboA.addItem(self.var[2], self.e)
        self.comboA.addItem(self.var[3], self.f)
        self.comboA.addItem(self.var[4], self.g)
        self.comboA.addItem(self.var[5], self.h)
        self.comboA.addItem(self.var[6], self.js)
        self.comboA.addItem(self.var[7], self.k)
        self.comboA.addItem(self.var[8], self.n)
        self.comboA.addItem(self.var[9], self.r)
        self.comboA.addItem(self.var[10], self.s)
        self.comboA.addItem(self.var[11], self.u)
        self.comboA.currentIndexChanged.connect(self.indexChanged)
        font = QFont()
        font.setFamily("Helvetica")
        self.comboA.setFont(font)
        layout.addWidget(self.comboA)

        self.comboB = QComboBox()
        self.comboB.setFont(font)
        self.comboB.adjustSize()
        self.indexChanged(self.comboA.currentIndex())
        layout.addWidget(self.comboB)
        self.show()

    def indexChanged(self, index):
        self.comboB.clear()
        data = self.comboA.itemData(index)
        if data is not None:
            self.comboB.addItems(data)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    ex = main_menu()
    sys.exit(app.exec_())
