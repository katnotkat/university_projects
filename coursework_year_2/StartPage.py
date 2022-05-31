from AddReader import *
from AddWorker import *
from AddLibrary import *
from AddBook import *
from AddIsKeptIn import *
from AddBorrow import *
from dbconnection import Connection


class StartPage(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'StartPage'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 315
        self.connection = Connection()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.connection.execute_statement(f'exec find_frozen_readers;', False)

        self.label = QLabel('Choose whatever activity you want:', self)
        self.label.move(10, 10)
        self.label.setFont(QFont('Arial', 15))

        # button to add a reader
        button_reader = QPushButton('Add a reader', self)  # name
        button_reader.setToolTip('This button adds a reader to database')  # tooltip
        button_reader.move(60, 30)  # where
        button_reader.resize(280, 33)
        button_reader.clicked.connect(self.on_click_reader)  # what happens if clicked

        # button to add a worker
        button_worker = QPushButton('Add a worker', self)
        button_worker.setToolTip('This button adds a worker to database')
        button_worker.move(60, 65)
        button_worker.resize(280, 33)
        button_worker.clicked.connect(self.on_click_worker)

        # button to add a book
        button_book = QPushButton('Add a book', self)
        button_book.setToolTip('This button adds a book to database')
        button_book.move(60, 100)
        button_book.resize(280, 33)
        button_book.clicked.connect(self.on_click_book)

        # button to add a library
        button_library = QPushButton('Add a library', self)
        button_library.setToolTip('This button adds a library to database')
        button_library.move(60, 135)
        button_library.resize(280, 33)
        button_library.clicked.connect(self.on_click_library)

        # button to add a book to library
        button_iskeptin = QPushButton('Add a book to library', self)
        button_iskeptin.setToolTip('This button adds a book to library')
        button_iskeptin.move(60, 170)
        button_iskeptin.resize(280, 33)
        button_iskeptin.clicked.connect(self.on_click_iskeptin)

        # button to arrange a new borrow
        button_borrow = QPushButton('Add a borrow', self)
        button_borrow.setToolTip('This button adds a borrow to database')
        button_borrow.move(60, 205)
        button_borrow.resize(280, 33)
        button_borrow.clicked.connect(self.on_click_borrow)

        # button to close an existing borrow
        button_updborrow = QPushButton('Update a borrow', self)
        button_updborrow.setToolTip('This button ends an existing borrow')
        button_updborrow.move(60, 240)
        button_updborrow.resize(280, 33)
        button_updborrow.clicked.connect(self.on_click_updateborrow)

        # exit page button
        button_exit = QPushButton('Exit page', self)
        button_exit.setToolTip('Click to exit')
        button_exit.move(150, 275)
        button_exit.resize(100, 35)
        button_exit.clicked.connect(self.on_click_exit)

        self.show()

    @pyqtSlot()
    def on_click_reader(self):
        print('Button_reader_clicked')
        self.addreader = AddReader(self.connection)
        self.addreader.show()

    @pyqtSlot()
    def on_click_worker(self):
        print('Button_worker_clicked')
        self.addworker = AddWorker(self.connection)
        self.addworker.show()

    @pyqtSlot()
    def on_click_book(self):
        print('Button_book_clicked')
        self.addbook = AddBook(self.connection)
        self.addbook.show()

    @pyqtSlot()
    def on_click_library(self):
        print('Button_library_clicked')
        self.addlibrary = AddLibrary(self.connection)
        self.addlibrary.show()

    @pyqtSlot()
    def on_click_iskeptin(self):
        print('Button_iskeptin_clicked')
        self.addiskeptin = AddIsKeptIn(self.connection, [])
        self.addiskeptin.show()

    @pyqtSlot()
    def on_click_borrow(self):
        print('Button_borrow_clicked')
        self.addborow = AddBorrow(self.connection)
        self.addborow.show()

    @pyqtSlot()
    def on_click_updateborrow(self):
        print('Button_updateborrow_clicked')
        self.updateborow = UpdateBorrow(self.connection)
        self.updateborow.show()

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
