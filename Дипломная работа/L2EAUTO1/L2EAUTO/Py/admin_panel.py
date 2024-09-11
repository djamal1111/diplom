import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import mysql.connector
import os

# Получение абсолютного пути к проекту
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(base_dir, '../UI_forms')


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, auth_window=None):
        super(AdminWindow, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'admin.ui'), self)
        self.auth_window = auth_window

        # Connect buttons to their functions
        self.auto_button.clicked.connect(self.open_adminauto_window)
        self.emp_button.clicked.connect(self.open_adminemp_window)
        self.exit_button.clicked.connect(self.logout)

    def open_adminauto_window(self):
        self.adminauto_window = AdminAutoWindow(self)
        self.adminauto_window.show()
        self.close()

    def open_adminemp_window(self):
        self.adminemp_window = AdminEmpWindow(self)
        self.adminemp_window.show()
        self.close()

    def logout(self):
        if self.auth_window:
            self.auth_window.show()
        self.close()


class AdminAutoWindow(QtWidgets.QMainWindow):
    def __init__(self, admin_window):
        super(AdminAutoWindow, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'adminauto.ui'), self)
        self.admin_window = admin_window

        # Connect buttons to their functions
        self.back_button.clicked.connect(self.go_back)
        self.add_auto_button.clicked.connect(self.add_auto)
        self.edit_auto_button.clicked.connect(self.edit_auto)
        self.delete_auto_button.clicked.connect(self.delete_auto)

        # Load data from database
        self.load_data()

    def load_data(self):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT cars.ID, brands.BrandName, models.ModelName, cars.Color, cars.Price, cars.SeatCount, 
                   cars.Length, cars.Width, cars.Height, cars.MaxSpeed, cars.FuelConsumption, cars.StockCount, engines.EngineName
            FROM cars
            LEFT JOIN brands ON cars.BrandID = brands.ID
            LEFT JOIN models ON cars.ModelID = models.ID
            LEFT JOIN engines ON cars.EngineID = engines.ID
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Set up the model
            model = QtGui.QStandardItemModel()
            self.tableView.setModel(model)

            # Set up the table headers in Russian
            model.setHorizontalHeaderLabels(
                ['ID', 'Бренд', 'Модель', 'Цвет', 'Цена', 'Кол-во мест', 'Длина', 'Ширина', 'Высота', 'Макс. скорость',
                 'Расход топлива', 'В наличии', 'Двигатель'])

            # Populate the table
            for row in result:
                items = [QtGui.QStandardItem(str(value)) for value in row.values()]
                model.appendRow(items)

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_auto(self):
        self.auto_form = AutoForm(self)
        self.auto_form.show()

    def edit_auto(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.tableView.model()
            data = [model.item(row, col).text() for col in range(model.columnCount())]
            self.auto_form = AutoForm(self, data)
            self.auto_form.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите автомобиль для редактирования")

    def delete_auto(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.tableView.model()
            car_id = model.item(row, 0).text()

            reply = QtWidgets.QMessageBox.question(self, 'Подтверждение удаления',
                                                   f"Вы уверены, что хотите удалить автомобиль с ID {car_id}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="l2eauto"
                    )
                    cursor = conn.cursor()

                    # Удаляем все связанные записи в таблице salescontract
                    cursor.execute("DELETE FROM salescontract WHERE CarID = %s", (car_id,))

                    # Удаляем все связанные записи в таблице technicalservice
                    cursor.execute("DELETE FROM technicalservice WHERE CarID = %s", (car_id,))

                    # Удаляем запись в таблице cars
                    cursor.execute("DELETE FROM cars WHERE ID = %s", (car_id,))
                    conn.commit()
                    model.removeRow(row)
                except mysql.connector.Error as err:
                    QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите автомобиль для удаления")

    def go_back(self):
        self.admin_window.show()
        self.close()


class AdminEmpWindow(QtWidgets.QMainWindow):
    def __init__(self, admin_window):
        super(AdminEmpWindow, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'adminemp.ui'), self)
        self.admin_window = admin_window

        # Connect buttons to their functions
        self.back_button.clicked.connect(self.go_back)
        self.add_emp_button.clicked.connect(self.add_emp)
        self.edit_emp_button.clicked.connect(self.edit_emp)
        self.delete_emp_button.clicked.connect(self.delete_emp)

        # Load data from database
        self.load_data()

    def load_data(self):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT employees.ID, positions.Name AS PositionName, employees.LastName, employees.FirstName, 
                   employees.MiddleName, employees.DateOfBirth, employees.PassportSeries, employees.PassportNumber, 
                   employees.Email, employees.Phone, employees.Login, employees.Password, employees.Education
            FROM employees
            LEFT JOIN positions ON employees.PositionID = positions.ID
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Set up the model
            model = QtGui.QStandardItemModel()
            self.tableView.setModel(model)

            # Set up the table headers in Russian
            model.setHorizontalHeaderLabels(
                ['ID', 'Должность', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Серия паспорта', 'Номер паспорта',
                 'Email', 'Телефон', 'Логин', 'Пароль', 'Образование'])

            # Populate the table
            for row in result:
                items = [QtGui.QStandardItem(str(value)) for value in row.values()]
                model.appendRow(items)

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_emp(self):
        self.emp_form = EmpForm(self)
        self.emp_form.show()

    def edit_emp(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.tableView.model()
            data = [model.item(row, col).text() for col in range(model.columnCount())]
            self.emp_form = EmpForm(self, data)
            self.emp_form.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите сотрудника для редактирования")

    def delete_emp(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.tableView.model()
            emp_id = model.item(row, 0).text()

            reply = QtWidgets.QMessageBox.question(self, 'Подтверждение удаления',
                                                   f"Вы уверены, что хотите удалить сотрудника с ID {emp_id}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="l2eauto"
                    )
                    cursor = conn.cursor()

                    # Удаляем все связанные записи в таблице technicalservice
                    cursor.execute("DELETE FROM technicalservice WHERE EmployeeID = %s", (emp_id,))

                    # Удаляем запись в таблице employees
                    cursor.execute("DELETE FROM employees WHERE ID = %s", (emp_id,))
                    conn.commit()
                    model.removeRow(row)
                except mysql.connector.Error as err:
                    QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите сотрудника для удаления")

    def go_back(self):
        self.admin_window.show()
        self.close()


class AutoForm(QtWidgets.QDialog):
    def __init__(self, parent, data=None):
        super(AutoForm, self).__init__(parent)
        uic.loadUi(os.path.join(ui_dir, 'auto_form.ui'), self)
        self.parent = parent

        self.load_combo_data()

        if data:
            self.setWindowTitle("Редактировать Автомобиль")
            self.populate_fields(data)
            self.submit_button.clicked.connect(lambda: self.submit(data[0]))
        else:
            self.setWindowTitle("Добавить Автомобиль")
            self.submit_button.clicked.connect(self.submit)

    def load_combo_data(self):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT ID, BrandName FROM brands")
            brands = cursor.fetchall()
            for brand in brands:
                self.brand_combo.addItem(brand['BrandName'], brand['ID'])

            cursor.execute("SELECT ID, ModelName FROM models")
            models = cursor.fetchall()
            for model in models:
                self.model_combo.addItem(model['ModelName'], model['ID'])

            cursor.execute("SELECT ID, EngineName FROM engines")
            engines = cursor.fetchall()
            for engine in engines:
                self.engine_combo.addItem(engine['EngineName'], engine['ID'])

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def populate_fields(self, data):
        brand_index = self.brand_combo.findData(data[1])
        self.brand_combo.setCurrentIndex(brand_index)

        model_index = self.model_combo.findData(data[2])
        self.model_combo.setCurrentIndex(model_index)

        self.color.setText(data[3])
        self.price.setText(data[4])
        self.seat_count.setText(data[5])
        self.length.setText(data[6])
        self.width.setText(data[7])
        self.height.setText(data[8])
        self.max_speed.setText(data[9])
        self.fuel_consumption.setText(data[10])
        self.stock_count.setText(data[11])

        engine_index = self.engine_combo.findData(data[12])
        self.engine_combo.setCurrentIndex(engine_index)

    def submit(self, car_id=None):
        brand_id = self.brand_combo.currentData()
        model_id = self.model_combo.currentData()
        color = self.color.text()
        price = self.price.text()
        seat_count = self.seat_count.text()
        length = self.length.text()
        width = self.width.text()
        height = self.height.text()
        max_speed = self.max_speed.text()
        fuel_consumption = self.fuel_consumption.text()
        stock_count = self.stock_count.text()
        engine_id = self.engine_combo.currentData()

        # Проверка наличия всех данных
        if not all([brand_id, model_id, color, price, seat_count, length, width, height, max_speed, fuel_consumption, stock_count, engine_id]):
            QtWidgets.QMessageBox.warning(self, "Недостаточно данных", "Пожалуйста, заполните все поля.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor()

            if car_id:
                cursor.execute("""
                    UPDATE cars
                    SET BrandID=%s, ModelID=%s, Color=%s, Price=%s, SeatCount=%s, Length=%s, Width=%s, Height=%s, MaxSpeed=%s, FuelConsumption=%s, StockCount=%s, EngineID=%s
                    WHERE ID=%s
                """, (brand_id, model_id, color, price, seat_count, length, width, height, max_speed, fuel_consumption,
                      stock_count, engine_id, car_id))
            else:
                cursor.execute("""
                    INSERT INTO cars (BrandID, ModelID, Color, Price, SeatCount, Length, Width, Height, MaxSpeed, FuelConsumption, StockCount, EngineID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (brand_id, model_id, color, price, seat_count, length, width, height, max_speed, fuel_consumption,
                      stock_count, engine_id))

            conn.commit()
            self.parent.load_data()
            self.close()

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class EmpForm(QtWidgets.QDialog):
    def __init__(self, parent, data=None):
        super(EmpForm, self).__init__(parent)
        uic.loadUi(os.path.join(ui_dir, 'emp_form.ui'), self)
        self.parent = parent

        self.load_combo_data()

        if data:
            self.setWindowTitle("Редактировать Сотрудника")
            self.populate_fields(data)
            self.submit_button.clicked.connect(lambda: self.submit(data[0]))
        else:
            self.setWindowTitle("Добавить Сотрудника")
            self.submit_button.clicked.connect(self.submit)

    def load_combo_data(self):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT ID, Name FROM positions")
            positions = cursor.fetchall()
            for position in positions:
                self.position_combo.addItem(position['Name'], position['ID'])

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def populate_fields(self, data):
        position_index = self.position_combo.findData(data[1])
        self.position_combo.setCurrentIndex(position_index)

        self.last_name.setText(data[2])
        self.first_name.setText(data[3])
        self.middle_name.setText(data[4])
        self.date_of_birth.setDate(QtCore.QDate.fromString(data[5], "yyyy-MM-dd"))
        self.passport_series.setText(data[6])
        self.passport_number.setText(data[7])
        self.email.setText(data[8])
        self.phone.setText(data[9])
        self.login.setText(data[10])
        self.password.setText(data[11])
        self.education.setText(data[12])

    def submit(self, emp_id=None):
        position_id = self.position_combo.currentData()
        last_name = self.last_name.text()
        first_name = self.first_name.text()
        middle_name = self.middle_name.text()
        date_of_birth = self.date_of_birth.date().toString("yyyy-MM-dd")
        passport_series = self.passport_series.text()
        passport_number = self.passport_number.text()
        email = self.email.text()
        phone = self.phone.text()
        login = self.login.text()
        password = self.password.text()
        education = self.education.text()

        # Проверка наличия всех данных
        if not all([position_id, last_name, first_name, middle_name, date_of_birth, passport_series, passport_number, email, phone, login, password, education]):
            QtWidgets.QMessageBox.warning(self, "Недостаточно данных", "Пожалуйста, заполните все поля.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor()

            if emp_id:
                cursor.execute("""
                    UPDATE employees
                    SET PositionID=%s, LastName=%s, FirstName=%s, MiddleName=%s, DateOfBirth=%s, PassportSeries=%s, PassportNumber=%s, Email=%s, Phone=%s, Login=%s, Password=%s, Education=%s
                    WHERE ID=%s
                """, (position_id, last_name, first_name, middle_name, date_of_birth, passport_series, passport_number, email, phone, login, password, education, emp_id))
            else:
                cursor.execute("""
                    INSERT INTO employees (PositionID, LastName, FirstName, MiddleName, DateOfBirth, PassportSeries, PassportNumber, Email, Phone, Login, Password, Education)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (position_id, last_name, first_name, middle_name, date_of_birth, passport_series, passport_number, email, phone, login, password, education))

            conn.commit()
            self.parent.load_data()
            self.close()

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AdminWindow()
    main_window.show()
    sys.exit(app.exec_())
