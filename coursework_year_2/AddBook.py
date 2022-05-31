from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from checks import *
from AddIsKeptIn import *


class AddBook(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = 'Adding a book'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 440
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
        self.label_name = QLabel('Enter book name:', self)
        self.label_name.move(10, 10)
        self.label_name.setFont(QFont('Arial', 14))

        self.textbox_name = QLineEdit(self)
        self.textbox_name.move(10, 28)
        self.textbox_name.resize(280, 20)

        # ISBN
        self.label_isbn = QLabel('Enter ISBN-code (if exists):', self)
        self.label_isbn.move(10, 52)
        self.label_isbn.setFont(QFont('Arial', 14))

        self.textbox_isbn = QLineEdit(self)
        self.textbox_isbn.move(10, 70)
        self.textbox_isbn.resize(280, 20)

        # Year
        self.label_year = QLabel("Enter year of publishing:", self)
        self.label_year.move(10, 94)
        self.label_year.setFont(QFont('Arial', 14))

        self.textbox_year = QLineEdit(self)
        self.textbox_year.move(10, 112)
        self.textbox_year.resize(280, 20)

        # Description
        self.label_description = QLabel("Enter book's description (optional):", self)
        self.label_description.move(10, 138)
        self.label_description.setFont(QFont('Arial', 14))

        self.textbox_description = QLineEdit(self)
        self.textbox_description.move(10, 156)
        self.textbox_description.resize(280, 20)

        # Author
        self.label_author = QLabel("Choose book's author:", self)
        self.label_author.move(10, 180)
        self.label_author.setFont(QFont('Arial', 14))

        self.combo_author = QComboBox(self)
        self.combo_author.move(10, 198)
        self.combo_author.resize(280, 20)
        author_name = self.connection.choose_table_columns('Author', ['FirstName', 'LastName'])
        self.combo_author.addItem('other')
        for el in author_name:
            self.combo_author.addItem(f"{el[1]}, {el[0]}")

        # Publisher
        self.label_publisher = QLabel("Choose book's publisher:", self)
        self.label_publisher.move(10, 224)
        self.label_publisher.setFont(QFont('Arial', 14))

        self.combo_publisher = QComboBox(self)
        self.combo_publisher.move(10, 242)
        self.combo_publisher.resize(280, 20)
        publisher_name = self.connection.choose_table_columns('Publisher', ['Name'])
        self.combo_publisher.addItem('other')
        for el in publisher_name:
            self.combo_publisher.addItem(f"{el[0]}")

        # CanBeBorrowed
        self.label_status = QLabel("Choose book's status:", self)
        self.label_status.move(10, 268)
        self.label_status.setFont(QFont('Arial', 14))

        self.combo_status = QComboBox(self)
        self.combo_status.move(10, 286)
        self.combo_status.resize(280, 20)
        status = self.connection.choose_table_columns('CanBeBorrowed', ['Name'])
        self.combo_status.addItem('')
        for el in status:
            self.combo_status.addItem(f"{el[0]}")

        # Genre
        self.label_genre = QLabel("Choose book's genre:", self)
        self.label_genre.move(10, 312)
        self.label_genre.setFont(QFont('Arial', 14))

        self.combo_genre = QComboBox(self)
        self.combo_genre.move(10, 330)
        self.combo_genre.resize(280, 20)
        genre = self.connection.choose_table_columns('Genre', ['Name'])
        self.combo_genre.addItem('')
        for el in genre:
            self.combo_genre.addItem(f"{el[0]}")

        # Language
        self.label_language = QLabel("Choose book's language:", self)
        self.label_language.move(10, 356)
        self.label_language.setFont(QFont('Arial', 14))

        self.combo_language = QComboBox(self)
        self.combo_language.move(10, 374)
        self.combo_language.resize(280, 20)
        language = self.connection.choose_table_columns('Language', ['Name'])
        self.combo_language.addItem('other')
        for el in language:
            self.combo_language.addItem(f"{el[0]}")

        # button to add a book
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a library')
        button_add.move(10, 400)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit')
        button_exit.move(120, 400)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

        # update data button
        button_update = QPushButton('Update Database', self)
        button_update.setToolTip('Click to update')
        button_update.move(260, 400)
        button_update.resize(130, 35)
        button_update.clicked.connect(self.on_click_update)

    @pyqtSlot()
    def on_click_add(self):
        print('Button_addlibrary_clicked')
        isbn = self.textbox_isbn.text()
        name = self.textbox_name.text()
        year = self.textbox_year.text()
        description = self.textbox_description.text()
        author = self.combo_author.currentText()
        publisher = self.combo_publisher.currentText()
        status = self.combo_status.currentText()
        genre = self.combo_genre.currentText()
        language = self.combo_language.currentText()

        # checking all the entered data
        if not is_data_filled([name, year, status, genre]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill all the fields, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            if len(year) != 4 or not is_int(year):
                QMessageBox.warning(self, 'Wrong year format', "Wrong year format, fill again, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_year.setText("")
            elif isbn != '' and (len(isbn) > 13 or not is_int(isbn)):
                QMessageBox.warning(self, 'Wrong ISBN format', "ISBN should contain 13 numbers or less!",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_isbn.setText("")
            elif author == 'other':
                self.addauthor = AddAuthor(self.connection)
                self.addauthor.show()
            elif publisher == 'other':
                self.addpublisher = AddItem(self.connection, "publisher")
                self.addpublisher.show()
            elif language == 'other':
                self.addlanguage = AddItem(self.connection, "language")
                self.addlanguage.show()
            else:
                surname, name_ = author.split(', ')
                year = int(year)
                authorid = self.connection.find_column_by_conditions('Author', 'AuthorID', ['FirstName', 'LastName'],
                                                                     [name_, surname], ['str', 'str'])
                genreid = self.connection.find_column_by_conditions('Genre', 'GenreID', ['Name'], [genre], ['varchar'])
                languageid = self.connection.find_column_by_conditions('Language', 'LanguageID', ['Name'],
                                                                     [language], ['varchar'])
                publisherid = self.connection.find_column_by_conditions('Publisher', 'PublisherID', ['Name'],
                                                                      [publisher], ['varchar'])
                statusid = self.connection.find_column_by_conditions('CanBeBorrowed', 'Status',
                                                                   ['Name'], [status], ['varchar'])
                values = tuple([isbn, name, year, description, authorid, publisherid, statusid, genreid, languageid])
                # защита от системных ошибок по вводу данных в базу
                try:
                    self.connection.insert_into('Book', values)
                    buttonReply = QMessageBox.question(self, 'Want to exit?',
                                                       "Book added to database. Want to add it to a library?",
                                                       QMessageBox.Yes | QMessageBox.No,
                                                       QMessageBox.Yes)
                    if buttonReply == QMessageBox.No:
                        self.close()
                    else:
                        self.addiskeptin = AddIsKeptIn(self.connection, values)
                        self.addiskeptin.show()
                except:
                    QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                        QMessageBox.Ok, QMessageBox.Ok)

                self.textbox_name.setText("")
                self.textbox_year.setText("")
                self.textbox_isbn.setText("")
                self.textbox_description.setText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()

    @pyqtSlot()
    def on_click_update(self):
        print('Button_update_clicked')
        if self.combo_author.currentText() == 'other':
            self.combo_author.clear()
            author_name = self.connection.choose_table_columns('Author', ['FirstName', 'LastName'])
            self.combo_author.addItem('other')
            for el in author_name:
                self.combo_author.addItem(f"{el[1]}, {el[0]}")

        if self.combo_publisher.currentText() == 'other':
            self.combo_publisher.clear()
            publisher_name = self.connection.choose_table_columns('Publisher', ['Name'])
            self.combo_publisher.addItem('other')
            for el in publisher_name:
                self.combo_publisher.addItem(f"{el[0]}")

        if self.combo_language.currentText() == 'other':
            self.combo_language.clear()
            language = self.connection.choose_table_columns('Language', ['Name'])
            self.combo_language.addItem('other')
            for el in language:
                self.combo_language.addItem(f"{el[0]}")


class AddAuthor(QWidget):

    def __init__(self, connection):
        super().__init__()
        self.title = f'Adding an author'
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 230
        self.connection = connection
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # FirstName
        self.label_name = QLabel("Enter author's first name:", self)
        self.label_name.move(10, 10)
        self.label_name.setFont(QFont('Arial', 14))

        self.textbox_name = QLineEdit(self)
        self.textbox_name.move(10, 28)
        self.textbox_name.resize(280, 20)

        # LastName
        self.label_surname = QLabel("Enter author's last name:", self)
        self.label_surname.move(10, 54)
        self.label_surname.setFont(QFont('Arial', 14))

        self.textbox_surname = QLineEdit(self)
        self.textbox_surname.move(10, 72)
        self.textbox_surname.resize(280, 20)

        # DateOfBirth
        self.label_dob = QLabel("Enter author's date of birth:", self)
        self.label_dob.move(10, 98)
        self.label_dob.setFont(QFont('Arial', 14))

        self.textbox_dob = QLineEdit(self)
        self.textbox_dob.move(10, 116)
        self.textbox_dob.resize(280, 20)

        # Country
        self.label_country = QLabel("Choose author's country:", self)
        self.label_country.move(10, 142)
        self.label_country.setFont(QFont('Arial', 14))

        self.combo_country = QComboBox(self)
        self.combo_country.move(10, 160)
        self.combo_country.resize(280, 20)
        country = self.connection.choose_table_columns('Country', ['Name'])
        self.combo_country.addItem('other')
        for el in country:
            self.combo_country.addItem(f"{el[0]}")

        # add an author button
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add an author')
        button_add.move(18, 186)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit to previous page')
        button_exit.move(135, 186)
        button_exit.resize(100, 35)
        button_exit.clicked.connect(self.on_click_exit)

        # update data button
        button_update = QPushButton('Update Database', self)
        button_update.setToolTip('Click to update')
        button_update.move(252, 186)
        button_update.resize(130, 35)
        button_update.clicked.connect(self.on_click_update)

    @pyqtSlot()
    def on_click_add(self):
        print('Button_addauthor_clicked')
        name = self.textbox_name.text().lower()
        dob = self.textbox_dob.text()
        surname = self.textbox_surname.text().lower()
        country = self.combo_country.currentText()

        # checking all the entered data
        if not is_data_filled([name, dob, surname]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill all the fields, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            if not is_date(dob):
                QMessageBox.warning(self, 'Date should be formatted', "Wrong date format, fill again, please",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_dob.setText("")
            elif country == 'other':
                self.addcountry = AddItem(self.connection, "country")
                self.addcountry.show()
            else:
                countryid = self.connection.find_column_by_conditions('Country', 'CountryID', ['Name'], [country],
                                                                    ['varchar'])
                values = tuple([name, dob, surname, int(countryid)])
                # защита от системных ошибок по вводу данных в базу
                try:
                    self.connection.insert_into('Author', values)
                    buttonReply = QMessageBox.information(self, 'Author added to database',
                                                        "Author added to database.",
                                                        QMessageBox.Ok, QMessageBox.Ok)
                    self.close()
                except:
                    QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                        QMessageBox.Ok, QMessageBox.Ok)
                    self.textbox_name.setText("")
                    self.textbox_dob.setText("")
                    self.textbox_surname.setText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()

    @pyqtSlot()
    def on_click_update(self):
        print('Button_update_clicked')
        self.combo_country.clear()
        country = self.connection.choose_table_columns('Country', ['Name'])
        self.combo_country.addItem('other')
        for el in country:
            self.combo_country.addItem(f"{el[0]}")


class AddItem(QWidget):

    def __init__(self, connection, label):
        super().__init__()
        self.title = f'Adding a {label}'
        self.label = label
        self.left = 350
        self.top = 350
        self.width = 400
        self.height = 93
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
        self.label_name = QLabel(f"Enter {self.label} name:", self)
        self.label_name.move(10, 10)
        self.label_name.setFont(QFont('Arial', 14))

        self.textbox_name = QLineEdit(self)
        self.textbox_name.move(10, 28)
        self.textbox_name.resize(280, 20)

        # add button
        button_add = QPushButton('Add', self)
        button_add.setToolTip('Click to add a library')
        button_add.move(97, 54)
        button_add.resize(100, 35)
        button_add.clicked.connect(self.on_click_add)

        # exit page button
        button_exit = QPushButton('Exit', self)
        button_exit.setToolTip('Click to exit to previous page')
        button_exit.move(203, 54)
        button_exit.resize(130, 35)
        button_exit.clicked.connect(self.on_click_exit)

    @pyqtSlot()
    def on_click_add(self):
        print(f'Button_add{self.label}_clicked')
        name = self.textbox_name.text().lower()

        # checking all the entered data
        if not is_data_filled([name]):
            QMessageBox.warning(self, 'Not enough data entered', "Fill the field, please",
                                QMessageBox.Ok, QMessageBox.Ok)
        else:
            values = f"('{name}')"
            # защита от системных ошибок по вводу данных в базу
            try:
                label = self.label[0].upper() + self.label[1:]
                self.connection.insert_into(f'{label}', values)
                buttonReply = QMessageBox.information(self, f'{label} added to database',
                                                            f"{label} added to database.",
                                                            QMessageBox.Ok, QMessageBox.Ok)
                self.close()
            except:
                QMessageBox.warning(self, 'Check your data', "An error occured: check your data!",
                                    QMessageBox.Ok, QMessageBox.Ok)
                self.textbox_name.setText("")

    @pyqtSlot()
    def on_click_exit(self):
        print('Button_exit_clicked')
        buttonReply = QMessageBox.question(self, 'Are you sure?', "Are you sure you want to exit?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.close()
