from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from checks import *


class AddLibrary(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = 'Adding a library'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 300
        self.connection = connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Name
        self.label_name = QLabel('Enter library name:', self)
        self.label_name.move(10, 10)
        self.label_name.setFont(QFont('Arial', 14))

        self.textbox_name = QLineEdit(self)
        self.textbox_name.move(10, 28)
        self.textbox_name.resize(280, 20)

        # Address
        self.label_address = QLabel('Enter library address:', self)
        self.label_address.move(10, 52)
        self.label_address.setFont(QFont('Arial', 14))

        self.textbox_address = QLineEdit(self)
        self.textbox_address.move(10, 70)
        self.textbox_address.resize(280, 20)

        # PostalCode
        self.label_postalcode = QLabel("Enter library's postal code:", self)
        self.label_postalcode.move(10, 94)
        self.label_postalcode.setFont(QFont('Arial', 14))

        self.textbox_postalcode = QLineEdit(self)
        self.textbox_postalcode.move(10, 112)
        self.textbox_postalcode.resize(280, 20)

        # Phone
        self.label_phone = QLabel("Enter library's phone number:", self)
        self.label_phone.move(10, 138)
        self.label_phone.setFont(QFont('Arial', 14))

        self.textbox_phone = QLineEdit(self)
        self.textbox_phone.move(10, 156)
        self.textbox_phone.resize(280, 20)

        # email
        self.label_email = QLabel("Enter library's E-mail address:", self)
        self.label_email.move(10, 180)
        self.label_email.setFont(QFont('Arial', 14))

        self.textbox_email = QLineEdit(self)
        self.textbox_email.move(10, 198)
        self.textbox_email.resize(280, 20)

        # button to add a library
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a library')
        button_add.move(97, 243)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit')
        button_exit.move(203, 243)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

    @pyqtSlot()
    def on_click_add(self):
        print('Button_addlibrary_clicked')
        name = self.textbox_name.text()
        address = self.textbox_address.text()
        postalcode = self.textbox_postalcode.text()
        phone = self.textbox_phone.text()
        email = self.textbox_email.text().lower()

        # checking all the entered data
        if not is_data_filled([name, address, postalcode, phone, email]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill all the fields, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            if len(postalcode) != 6 or not is_int(postalcode):
                QMessageBox.warning(self, 'Wrong postal code format', "Wrong postal code format, fill again, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_postalcode.setText("")
            elif not is_phone(phone):
                QMessageBox.warning(self, 'Wrong phone number format', "Wrong phone number format, fill again, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_phone.setText("")
            elif not is_email(email):
                QMessageBox.warning(self, 'Wrong email format', "An actual email address needed",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_email.setText("")
            else:
                try:
                    if self.connection.find_column_by_conditions('Library', 'LibraryID', ['Name'],
                                                                 [name], ['varchar']) is not False:
                        QMessageBox.warning(self, 'Library already exists',
                                            "Please, change library's name - it already exists",
                                            QMessageBox.Ok, QMessageBox.Ok)
                        self.textbox_name.setText("")
                    else:
                        values = tuple([name, address, int(postalcode), phone, email])

                        # защита от системных ошибок по вводу данных в базу
                        try:
                            self.connection.insert_into('Library', values)
                            buttonReply = QMessageBox.question(self, 'Want to exit?',
                                                               "Library added to database. " +
                                                               "Want to add another library?",
                                                               QMessageBox.Yes | QMessageBox.No,
                                                               QMessageBox.Yes)
                            if buttonReply == QMessageBox.No:
                                self.close()
                        except:
                            QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                                QMessageBox.Ok, QMessageBox.Ok)
                except:
                    QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                        QMessageBox.Ok, QMessageBox.Ok)
                    # self.textbox_name.setText("")

                self.textbox_name.setText("")
                self.textbox_address.setText("")
                self.textbox_postalcode.setText("")
                self.textbox_phone.setText("")
                self.textbox_email.setText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
