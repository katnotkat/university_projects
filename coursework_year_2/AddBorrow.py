from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date
from checks import *


class AddBorrow(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = f'Adding a borrow of a book'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 226
        self.connection = connection
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
        self.combo_book.currentIndexChanged.connect(self.selectionchange)

        # Library
        self.label_library = QLabel('Choose a library:', self)
        self.label_library.move(10, 54)
        self.label_library.setFont(QFont('Arial', 14))

        self.combo_library = QComboBox(self)
        self.combo_library.move(10, 72)
        self.combo_library.resize(280, 20)
        libraries = self.connection.choose_table_columns('Library', ['Name'])
        self.combo_library.addItem('')
        for el in libraries:
            self.combo_library.addItem(el[0])

        # Reader
        self.label_reader = QLabel('Choose a reader:', self)
        self.label_reader.move(10, 98)
        self.label_reader.setFont(QFont('Arial', 14))

        self.combo_reader = QComboBox(self)
        self.combo_reader.move(10, 116)
        self.combo_reader.resize(280, 20)
        reader = self.connection.choose_table_columns('Reader', ['ReaderID', 'FirstName', 'LastName'])
        self.combo_reader.addItem('')
        for el in reader:
            self.combo_reader.addItem(f"{el[0]}; {el[1]} {el[2]}")

        # Duration
        self.label_duration = QLabel("Enter duration of the borrow:", self)
        self.label_duration.move(10, 142)
        self.label_duration.setFont(QFont('Arial', 14))

        self.textbox_duration = QLineEdit(self)
        self.textbox_duration.move(10, 160)
        self.textbox_duration.resize(280, 20)
        self.textbox_duration.setText('14')

        # add button
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a library')
        button_add.move(97, 186)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit to previous page')
        button_exit.move(203, 186)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

    @pyqtSlot()
    def selectionchange(self):
        # книга выбрана
        book = self.combo_book.currentText()
        if book != '':
            bookid = int(book.split('; ')[0])  # id книги
            self.combo_library.clear()
            # id библиотек с помощью процедуры
            libraries = self.connection.execute_statement(f'EXEC dbo.search_book @BookID = {bookid};', True)
            libids = [str(el[0]) for el in libraries]
            self.combo_library.addItem('')

            # по номерам библиотек найдем названия, для удобства
            for el in libids:
                number = self.connection.execute_statement(f'select dbo.book_in_library_now({el}, {bookid});', True)[0][0]
                # проверка на наличие книги в библиотеке в данный момент
                if number > 0:
                    name = self.connection.find_column_by_conditions('Library', 'Name', ['LibraryID'], [int(el)], ['int'])
                    self.combo_library.addItem(f'{el}; {name}')

    @pyqtSlot()
    def on_click_add(self):
        print(f'Button_addborrow_clicked')
        book = self.combo_book.currentText()
        library = self.combo_library.currentText()
        reader = self.combo_reader.currentText()
        duration = self.textbox_duration.text()
        datestarted = date.today().strftime("%Y/%m/%d")

        # checking all the entered data
        if not is_data_filled([book, library, reader, duration]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill the field, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        elif not is_int(duration):
            QMessageBox.warning(self, 'Wrong number format!', "Number should be an integer",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            duration = int(duration)
            libid = self.connection.find_column_by_conditions('Library', 'LibraryID', ['Name'], [library], ['varchar'])
            bookid = int(book.split('; ')[0])
            readerid = int(reader.split('; ')[0])
            statusid = self.connection.find_column_by_conditions('Book', 'Status', ['BookID'], [bookid], ['int'])

            if libid is False:
                libid = int(library.split('; ')[0])

            # if the reader was banned more than a month ago, trying to de-ban them
            self.connection.execute_statement(f"exec dbo.try_deban_reader @ReaderID = {readerid};", False)

            rstatus = self.connection.execute_statement(f"exec dbo.check_reader_status @ReaderID = {readerid};",
                                                        True)[0][0]
            if rstatus == 'banned':
                QMessageBox.warning(self, "Can't give a book", "Reader is currently banned",
                                    QMessageBox.Ok, QMessageBox.Ok)
            elif statusid == 2:
                QMessageBox.warning(self, "Can't give a book", "Book to read in hall only!",
                                    QMessageBox.Ok, QMessageBox.Ok)
            elif statusid == 3:
                QMessageBox.warning(self, "Can't give a book", "Book to read in archive only!",
                                    QMessageBox.Ok, QMessageBox.Ok)
            else:
                values = f"('{datestarted}', NULL, {duration}, {libid}, {readerid}, {bookid})"

                # защита от системных ошибок по вводу данных в базу
                try:
                    # statement = f'insert into Borrow  values {values}'
                    self.connection.insert_into(f'Borrow', values)
                    buttonReply = QMessageBox.information(self, f'Added successfully',
                                                                f"Borrow created successfully",
                                                                QMessageBox.Ok, QMessageBox.Ok)
                    self.close()
                except:
                    QMessageBox.warning(self, 'Check your data', "An error occured: book should be in the library!",
                                        QMessageBox.Ok, QMessageBox.Ok)
                    # self.textbox_name.setText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()


class UpdateBorrow(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = f'Updating a borrow'
        self.left = 350
        self.top = 350
        self.width = 600
        self.height = 94
        self.connection = connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Borrow
        self.label_borrow = QLabel("Choose a borrow:", self)
        self.label_borrow.move(10, 10)
        self.label_borrow.setFont(QFont('Arial', 14))

        self.combo_borrow = QComboBox(self)
        self.combo_borrow.move(10, 28)
        self.combo_borrow.resize(580, 20)
        borrow = self.connection.choose_table_columns('borrow_info', ['*'])
        self.combo_borrow.addItem('')
        for el in borrow:
            self.combo_borrow.addItem(f"{el[0]}; {el[1]}, {el[2]}, {el[3]}, {el[4]}")

        # update button
        button_add = QPushButton('Update', self)
        button_add.setToolTip('Click to add a library')
        button_add.move(124, 54)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit to previous page')
        button_exit.move(346, 54)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

    @pyqtSlot()
    def on_click_add(self):
        print('Button_update_clicked')
        dateend = date.today().strftime("%Y/%m/%d")
        borrow = self.combo_borrow.currentText()

        if borrow == '':
            QMessageBox.warning(self, 'Not enough data entered', "Fill the field, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            borrowid = int(borrow.split('; ')[0])
            statement = f"update Borrow set DateEnd = '{dateend}' where BorrowID = {borrowid};"
            # защита от системных ошибок по вводу данных в базу
            try:
                exec = self.connection.execute_statement(statement, False)
                buttonReply = QMessageBox.information(self, f'Added successfully',
                                                        f"Borrow updated successfully",
                                                        QMessageBox.Ok, QMessageBox.Ok)
                self.close()
            except:
                QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.combo_borrow.setCurrentText('')

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
