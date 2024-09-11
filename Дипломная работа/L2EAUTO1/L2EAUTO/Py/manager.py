import sys
import os
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import mysql.connector
from fpdf import FPDF

# Получение абсолютного пути к проекту
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(base_dir, '../UI_forms')
font_path = os.path.join(base_dir, 'DejaVuSansCondensed.ttf')


class ManagerApp(QtWidgets.QMainWindow):
    def __init__(self, auth_window):
        super(ManagerApp, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'manager.ui'), self)
        self.auth_window = auth_window

        # Подключение кнопок к соответствующим функциям
        self.sales_button = self.findChild(QtWidgets.QPushButton, 'sales_button')
        self.records_button = self.findChild(QtWidgets.QPushButton, 'records_button')
        self.clients_button = self.findChild(QtWidgets.QPushButton, 'clients_button')
        self.analytics_button = self.findChild(QtWidgets.QPushButton, 'analytics_button')
        self.exit_button = self.findChild(QtWidgets.QPushButton, 'exit_button')

        # Проверка наличия элементов
        if self.sales_button is None:
            raise ValueError("sales_button не найден в UI")
        if self.records_button is None:
            raise ValueError("custrecord_button не найден в UI")  # Проверьте это имя
        if self.clients_button is None:
            raise ValueError("customer_button не найден в UI")
        if self.analytics_button is None:
            raise ValueError("analitic_button не найден в UI")
        if self.exit_button is None:
            raise ValueError("exit_button не найден в UI")

        self.sales_button.clicked.connect(self.open_sales_form)
        self.records_button.clicked.connect(self.open_records_form)
        self.clients_button.clicked.connect(self.open_clients_form)
        self.analytics_button.clicked.connect(self.show_sales_analytics)
        self.exit_button.clicked.connect(self.return_to_auth)


    def open_sales_form(self):
        self.sales_ui = SalesForm(self)
        self.sales_ui.show()
        self.hide()

    def open_records_form(self):
        self.records_ui = RecordsForm(self)
        self.records_ui.show()
        self.hide()

    def open_clients_form(self):
        self.clients_ui = CustomerForm(self)
        self.clients_ui.show()
        self.hide()

    def show_sales_analytics(self):
        self.analytics_ui = SalesAnalyticsForm(self)
        self.analytics_ui.show()
        self.hide()

    def return_to_auth(self):
        self.auth_window.clear_inputs()
        self.auth_window.show()
        self.close()


class SalesForm(QtWidgets.QMainWindow):
    def __init__(self, manager_window):
        super(SalesForm, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'manager_sales.ui'), self)
        self.manager_window = manager_window
        self.back_button = self.findChild(QtWidgets.QPushButton, 'back_button')
        self.back_button.clicked.connect(self.go_back)

        # Подключение кнопок к соответствующим функциям
        self.add_button = self.findChild(QtWidgets.QPushButton, 'add_button')
        self.edit_button = self.findChild(QtWidgets.QPushButton, 'edit_button')
        self.delete_button = self.findChild(QtWidgets.QPushButton, 'delete_button')
        self.chek_button = self.findChild(QtWidgets.QPushButton, 'chek_button')

        # Проверка наличия элементов
        if self.add_button is None:
            raise ValueError("add_button не найден в UI")
        if self.edit_button is None:
            raise ValueError("edit_button не найден в UI")
        if self.delete_button is None:
            raise ValueError("delete_button не найден в UI")
        if self.chek_button is None:
            raise ValueError("chek_button не найден в UI")

        self.add_button.clicked.connect(self.add_sale)
        self.edit_button.clicked.connect(self.edit_sale)
        self.delete_button.clicked.connect(self.delete_sale)
        self.chek_button.clicked.connect(self.export_check)

        # Инициализация таблицы
        self.table = self.findChild(QtWidgets.QTableView, 'tableView')
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
            SELECT salescontract.ID, customers.LastName, cars.ModelID, salescontract.DateTime, salescontract.Status, salescontract.EmployeeID
            FROM salescontract
            JOIN customers ON salescontract.CustomerID = customers.ID
            JOIN cars ON salescontract.CarID = cars.ID
            """
            cursor.execute(query)
            results = cursor.fetchall()

            model = QtGui.QStandardItemModel()
            self.table.setModel(model)
            model.setHorizontalHeaderLabels(['ID', 'Покупатель', 'Модель', 'Дата', 'Статус', 'Менеджер'])

            for row in results:
                items = [QtGui.QStandardItem(str(value)) for value in row.values()]
                model.appendRow(items)

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_sale(self):
        self.sale_form = SaleForm(self)
        self.sale_form.show()

    def edit_sale(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.table.model()
            data = [model.item(row, col).text() for col in range(model.columnCount())]
            self.sale_form = SaleForm(self, data)
            self.sale_form.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите продажу для редактирования")

    def delete_sale(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.table.model()
            sale_id = model.item(row, 0).text()

            reply = QtWidgets.QMessageBox.question(self, 'Подтверждение удаления',
                                                   f"Вы уверены, что хотите удалить продажу с ID {sale_id}?",
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
                    cursor.execute("DELETE FROM salescontract WHERE ID = %s", (sale_id,))
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
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите продажу для удаления")

    def export_check(self):
        selected = self.table.selection

    def export_check(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.table.model()
            sale_id = model.item(row, 0).text()

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
                SELECT salescontract.ID, customers.LastName, customers.FirstName, cars.ModelID, cars.Price, brands.BrandName, models.ModelName, salescontract.DateTime, salescontract.Status, employees.LastName AS EmployeeLastName, employees.FirstName AS EmployeeFirstName
                FROM salescontract
                JOIN customers ON salescontract.CustomerID = customers.ID
                JOIN cars ON salescontract.CarID = cars.ID
                JOIN models ON cars.ModelID = models.ID
                JOIN brands ON cars.BrandID = brands.ID
                JOIN employees ON salescontract.EmployeeID = employees.ID
                WHERE salescontract.ID = %s
                """
                cursor.execute(query, (sale_id,))
                sale_data = cursor.fetchone()

                if sale_data:
                    pdf = FPDF()
                    pdf.add_page()

                    # Путь к файлу шрифта
                    font_path = r'C:\Users\Chalk\PycharmProjects\L2EAUTO\Py\DejaVuSansCondensed.ttf'
                    pdf.add_font('DejaVu', '', font_path, uni=True)
                    pdf.set_font('DejaVu', '', 14)

                    pdf.cell(200, 10, txt=f"Чек продажи #{sale_data['ID']}", ln=True, align='C')
                    pdf.ln(10)
                    pdf.cell(100, 10, txt=f"Покупатель: {sale_data['LastName']} {sale_data['FirstName']}", ln=True)
                    pdf.cell(100, 10, txt=f"Модель автомобиля: {sale_data['BrandName']} {sale_data['ModelName']}",
                             ln=True)
                    pdf.cell(100, 10, txt=f"Дата и время продажи: {sale_data['DateTime']}", ln=True)
                    pdf.cell(100, 10, txt=f"Статус: {sale_data['Status']}", ln=True)
                    pdf.cell(100, 10, txt=f"Менеджер: {sale_data['EmployeeLastName']} {sale_data['EmployeeFirstName']}",
                             ln=True)
                    pdf.cell(100, 10, txt=f"Сумма продажи: {sale_data['Price']} руб.", ln=True)

                    pdf.output(f"check_{sale_data['ID']}.pdf")

                    QtWidgets.QMessageBox.information(self, "Успех", "Чек успешно выгружен!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Данные о продаже не найдены.")
            except mysql.connector.Error as err:
                QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите продажу для выгрузки чека")

    def go_back(self):
        self.manager_window.show()
        self.close()


class SaleForm(QtWidgets.QDialog):
    def __init__(self, parent, data=None):
        super(SaleForm, self).__init__(parent)
        uic.loadUi(os.path.join(ui_dir, 'sale_form.ui'), self)
        self.parent = parent

        # Инициализация элементов
        self.customer_combo = self.findChild(QtWidgets.QComboBox, 'customer_combo')
        self.car_combo = self.findChild(QtWidgets.QComboBox, 'car_combo')
        self.datetime_input = self.findChild(QtWidgets.QDateTimeEdit, 'datetime_input')
        self.status_input = self.findChild(QtWidgets.QLineEdit, 'status_input')
        self.employee_combo = self.findChild(QtWidgets.QComboBox, 'employee_combo')
        self.submit_button = self.findChild(QtWidgets.QPushButton, 'submit_button')

        if self.customer_combo is None:
            raise ValueError("customer_combo не найден в UI")
        if self.car_combo is None:
            raise ValueError("car_combo не найден в UI")
        if self.datetime_input is None:
            raise ValueError("datetime_input не найден в UI")
        if self.status_input is None:
            raise ValueError("status_input не найден в UI")
        if self.employee_combo is None:
            raise ValueError("employee_combo не найден в UI")
        if self.submit_button is None:
            raise ValueError("submit_button не найден в UI")

        self.load_combo_data()

        if data:
            self.setWindowTitle("Редактировать продажу")
            self.populate_fields(data)
            self.submit_button.clicked.connect(lambda: self.submit(data[0]))
        else:
            self.setWindowTitle("Добавить продажу")
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

            cursor.execute("SELECT ID, CONCAT(LastName, ' ', FirstName) as FullName FROM customers")
            customers = cursor.fetchall()
            for customer in customers:
                self.customer_combo.addItem(customer['FullName'], customer['ID'])

            cursor.execute(
                "SELECT cars.ID, CONCAT(brands.BrandName, ' ', models.ModelName) as CarModel FROM cars JOIN models ON cars.ModelID = models.ID JOIN brands ON cars.BrandID = brands.ID")
            cars = cursor.fetchall()
            for car in cars:
                self.car_combo.addItem(car['CarModel'], car['ID'])

            cursor.execute("SELECT ID, CONCAT(LastName, ' ', FirstName) as FullName FROM employees")
            employees = cursor.fetchall()
            for employee in employees:
                self.employee_combo.addItem(employee['FullName'], employee['ID'])

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def populate_fields(self, data):
        customer_index = self.customer_combo.findData(data[1])
        self.customer_combo.setCurrentIndex(customer_index)
        car_index = self.car_combo.findData(data[2])
        self.car_combo.setCurrentIndex(car_index)
        self.datetime_input.setDateTime(QtCore.QDateTime.fromString(data[3], "yyyy-MM-dd HH:mm:ss"))
        self.status_input.setText(data[4])
        employee_index = self.employee_combo.findData(data[5])
        self.employee_combo.setCurrentIndex(employee_index)

    def submit(self, sale_id=None):
        customer_id = self.customer_combo.currentData()
        car_id = self.car_combo.currentData()
        datetime = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        status = self.status_input.text()
        employee_id = self.employee_combo.currentData()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor()

            if sale_id:
                cursor.execute("""
                    UPDATE salescontract
                    SET CustomerID=%s, CarID=%s, DateTime=%s, Status=%s, EmployeeID=%s
                    WHERE ID=%s
                """, (customer_id, car_id, datetime, status, employee_id, sale_id))
            else:
                cursor.execute("""
                    INSERT INTO salescontract (CustomerID, CarID, DateTime, Status, EmployeeID)
                    VALUES (%s, %s, %s, %s, %s)
                """, (customer_id, car_id, datetime, status, employee_id))

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


class CustomerForm(QtWidgets.QMainWindow):
    def __init__(self, manager_window):
        super(CustomerForm, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'manager_castomer.ui'), self)
        self.manager_window = manager_window
        self.back_button = self.findChild(QtWidgets.QPushButton, 'back_button')
        self.back_button.clicked.connect(self.go_back)

        self.table = self.findChild(QtWidgets.QTableView, 'tableView')
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
            SELECT ID, LastName, FirstName, MiddleName, Email, Phone
            FROM customers
            """
            cursor.execute(query)
            results = cursor.fetchall()

            model = QtGui.QStandardItemModel()
            self.table.setModel(model)
            model.setHorizontalHeaderLabels(['ID', 'Фамилия', 'Имя', 'Отчество', 'Email', 'Телефон'])

            for row in results:
                items = [QtGui.QStandardItem(str(value)) for value in row.values()]
                model.appendRow(items)

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def go_back(self):
        self.manager_window.show()
        self.close()


class SalesAnalyticsForm(QtWidgets.QMainWindow):
    def __init__(self, manager_window):
        super(SalesAnalyticsForm, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'sales_analytics.ui'), self)
        self.manager_window = manager_window
        self.back_button = self.findChild(QtWidgets.QPushButton, 'back_button')
        self.back_button.clicked.connect(self.go_back)

        self.table = self.findChild(QtWidgets.QTableView, 'tableView')
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
            SELECT m.ModelName, COUNT(sc.ID) as SalesCount
            FROM salescontract sc
            JOIN cars c ON sc.CarID = c.ID
            JOIN models m ON c.ModelID = m.ID
            GROUP BY m.ModelName
            """
            cursor.execute(query)
            results = cursor.fetchall()

            model = QtGui.QStandardItemModel()
            self.table.setModel(model)
            model.setHorizontalHeaderLabels(['Модель', 'Количество продаж'])

            for row in results:
                items = [QtGui.QStandardItem(str(value)) for value in row.values()]
                model.appendRow(items)

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def go_back(self):
        self.manager_window.show()
        self.close()


class RecordsForm(QtWidgets.QMainWindow):
    def __init__(self, manager_window):
        super(RecordsForm, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'manager_record_testdive.ui'), self)
        self.manager_window = manager_window
        self.back_button = self.findChild(QtWidgets.QPushButton, 'back_button')
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        self.manager_window.show()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec_())
