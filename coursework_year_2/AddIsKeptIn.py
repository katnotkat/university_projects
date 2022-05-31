from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from checks import *


class AddIsKeptIn(QWidget):

    def __init__(self, connection, values):
        super().__init__()
        self.title = f'Adding a book to a library'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 270
        self.connection = connection
        self.values = values
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Book
        self.label_book = QLabel("Choose book:", self)
        self.label_book.move(10, 10)
        self.label_book.setFont(QFont('Arial', 14))

        self.combo_book = QComboBox(self)
        self.combo_book.move(10, 28)
        self.combo_book.resize(280, 20)
        book = self.connection.choose_table_columns('Book', ['BookID', 'Name'])
        self.combo_book.addItem('')
        for el in book:
            self.combo_book.addItem(f"{el[0]}; {el[1]}")

        # Library
        self.label_library = QLabel('Choose library:', self)
        self.label_library.move(10, 54)
        self.label_library.setFont(QFont('Arial', 14))

        self.combo_library = QComboBox(self)
        self.combo_library.move(10, 72)
        self.combo_library.resize(280, 20)
        libraries = self.connection.choose_table_columns('Library', ['Name'])
        self.combo_library.addItem('')
        for el in libraries:
            self.combo_library.addItem(el[0])

        # Number
        self.label_num = QLabel("Enter the number of books you want to add:", self)
        self.label_num.move(10, 98)
        self.label_num.setFont(QFont('Arial', 14))

        self.textbox_num = QLineEdit(self)
        self.textbox_num.move(10, 116)
        self.textbox_num.resize(280, 20)

        # Zone
        self.label_zone = QLabel("Choose zone to place a book:", self)
        self.label_zone.move(10, 142)
        self.label_zone.setFont(QFont('Arial', 14))

        self.combo_zone = QComboBox(self)
        self.combo_zone.move(10, 160)
        self.combo_zone.resize(280, 20)
        zone = self.connection.choose_table_columns('Zone', ['ZoneID', 'Name'])
        self.combo_zone.addItem('')
        for el in zone:
            self.combo_zone.addItem(f"{el[0]}; {el[1]}")

        # Bookcase
        self.label_case = QLabel("Enter the number of the bookcase where the book is located:", self)
        self.label_case.move(10, 186)
        self.label_case.setFont(QFont('Arial', 14))

        self.textbox_case = QLineEdit(self)
        self.textbox_case.move(10, 204)
        self.textbox_case.resize(280, 20)

        # add button
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a library')
        button_add.move(97, 230)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit to previous page')
        button_exit.move(203, 230)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

        if len(self.values) != 0:
            incolumns = ['ISBN', 'Name', 'Year', 'Description', 'AuthorID',
                         'PublisherID', 'Status', 'GenreID', 'LanguageID']
            valuetypes = ['str', 'str', 'int', 'str', 'int', 'int', 'int', 'int', 'int']

            bookid = self.connection.find_column_by_conditions('Book', 'BookID', incolumns, self.values, valuetypes)
            self.combo_book.clear()
            self.combo_book.addItem(f"{bookid}; {self.values[1]}")
            self.combo_book.setCurrentText(f"{bookid}; {self.values[1]}")

            if self.values[-3] == 3:
                self.combo_zone.clear()
                self.combo_zone.addItem(f"3; archive")


    @pyqtSlot()
    def on_click_add(self):
        print(f'Button_addiskeptin_clicked')
        book = self.combo_book.currentText()
        library = self.combo_library.currentText()
        number = self.textbox_num.text()
        case = self.textbox_case.text()
        zone = self.combo_zone.currentText()

        # checking all the entered data
        if not is_data_filled([book, library, number, zone]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill the field, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        elif not is_int(number):
            QMessageBox.warning(self, 'Wrong number format!', "Number should be an integer",
                                QMessageBox.Ok, QMessageBox.Ok)
        elif not is_int(case):
            QMessageBox.warning(self, 'Wrong number format!', "Bookcase number should be an integer",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            number = int(number)
            libid = self.connection.find_column_by_conditions('Library', 'LibraryID', ['Name'], [library], ['varchar'])
            bookid = int(book.split('; ')[0])
            zoneid = int(zone.split('; ')[0])
            statusid = self.connection.find_column_by_conditions('Book', 'Status', ['BookID'], [bookid], ['int'])

            values = tuple([libid, bookid, number, case, zoneid])

            if statusid == 3 and zoneid != 3 or statusid != 3 and zoneid == 3:
                QMessageBox.warning(self, "Book's status doesn't match its zone", "Change book's zone, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
            else:
                # защита от системных ошибок по вводу данных в базу
                try:
                    self.connection.insert_into(f'IsKeptIn', values)
                    buttonReply = QMessageBox.information(self, f'Added successfully',
                                                                f"Books successfully placed in the library",
                                                                QMessageBox.Ok, QMessageBox.Ok)
                    self.close()
                except:
                    QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                        QMessageBox.Ok, QMessageBox.Ok)
                    self.textbox_number.setText("")
                    self.textbox_case.setText("")


    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
