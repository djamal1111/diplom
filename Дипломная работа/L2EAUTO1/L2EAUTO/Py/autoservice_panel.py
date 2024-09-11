import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import mysql.connector
import os

# Получение абсолютного пути к проекту
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(base_dir, '../UI_forms')


class AutoserviceWindow(QtWidgets.QMainWindow):
    def __init__(self, auth_window=None):
        super(AutoserviceWindow, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'autoservice.ui'), self)
        self.auth_window = auth_window

        # Connect buttons to their functions
        self.records_button.clicked.connect(self.open_records_window)
        self.exit_button.clicked.connect(self.logout)

    def open_records_window(self):
        self.records_window = RecordsWindow(self)
        self.records_window.show()
        self.close()

    def logout(self):
        self.close()
        from auth import AuthWindow
        self.authform = AuthWindow()
        self.authform.show()


class RecordsWindow(QtWidgets.QMainWindow):
    def __init__(self, autoservice_window):
        super(RecordsWindow, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'rec_autoservice.ui'), self)
        self.autoservice_window = autoservice_window

        # Connect buttons to their functions
        self.back_button.clicked.connect(self.go_back)
        self.add_record_button.clicked.connect(self.add_record)
        self.edit_record_button.clicked.connect(self.edit_record)
        self.delete_record_button.clicked.connect(self.delete_record)

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
            SELECT ts.ID, ts.ServiceDateTime, cars.ModelID, employees.LastName, s.ServiceName, s.ServicePrice, s.ExecutionTime
            FROM technicalservice ts
            LEFT JOIN cars ON ts.CarID = cars.ID
            LEFT JOIN employees ON ts.EmployeeID = employees.ID
            LEFT JOIN services s ON ts.ServiceID = s.ID
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Set up the model
            model = QtGui.QStandardItemModel()
            self.tableView.setModel(model)

            # Set up the table headers in Russian
            model.setHorizontalHeaderLabels(
                ['ID', 'Дата и время', 'Модель автомобиля', 'Механик', 'Название услуги', 'Стоимость', 'Время выполнения'])

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

    def add_record(self):

        self.record_form = RecordForm(self)
        self.record_form.show()

    def edit_record(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.tableView.model()
            data = [model.item(row, col).text() for col in range(model.columnCount())]
            self.record_form = RecordForm(self, data)
            self.record_form.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования")

    def delete_record(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            model = self.tableView.model()
            record_id = model.item(row, 0).text()

            reply = QtWidgets.QMessageBox.question(self, 'Подтверждение удаления',
                                                   f"Вы уверены, что хотите удалить запись с ID {record_id}?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                conn = None
                cursor = None
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="l2eauto"
                    )
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM technicalservice WHERE ID = %s", (record_id,))
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
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите запись для удаления")

    def go_back(self):
        self.autoservice_window.show()
        self.close()


class RecordForm(QtWidgets.QDialog):
    def __init__(self, parent, data=None):
        super(RecordForm, self).__init__(parent)
        uic.loadUi(os.path.join(ui_dir, 'record_form.ui'), self)
        self.parent = parent

        self.load_combo_data()

        if data:
            self.setWindowTitle("Редактировать Запись")
            self.populate_fields(data)
            self.submit_button.clicked.connect(lambda: self.submit(data[0]))
        else:
            self.setWindowTitle("Добавить Запись")
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

            cursor.execute("SELECT ID, ModelID FROM cars")
            cars = cursor.fetchall()
            for car in cars:
                self.car_combo.addItem(str(car['ModelID']), car['ID'])

            cursor.execute("SELECT ID, CONCAT(LastName, ' ', FirstName) AS FullName FROM employees")
            employees = cursor.fetchall()
            for employee in employees:
                self.employee_combo.addItem(employee['FullName'], employee['ID'])

            cursor.execute("SELECT ID, ServiceName FROM services")
            services = cursor.fetchall()
            for service in services:
                self.service_combo.addItem(service['ServiceName'], service['ID'])

        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Ошибка подключения к БД", f"Ошибка: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def populate_fields(self, data):
        self.service_date_time.setDateTime(QtCore.QDateTime.fromString(data[1], "yyyy-MM-dd HH:mm:ss"))

        car_index = self.car_combo.findData(data[2])
        self.car_combo.setCurrentIndex(car_index)

        employee_index = self.employee_combo.findData(data[3])
        self.employee_combo.setCurrentIndex(employee_index)

        service_index = self.service_combo.findData(data[4])
        self.service_combo.setCurrentIndex(service_index)

    def submit(self, record_id=None):
        service_date_time = self.service_date_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        car_id = self.car_combo.currentData()
        employee_id = self.employee_combo.currentData()
        service_id = self.service_combo.currentData()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="l2eauto"
            )
            cursor = conn.cursor()

            if record_id:
                cursor.execute("""
                    UPDATE technicalservice
                    SET ServiceDateTime=%s, CarID=%s, EmployeeID=%s, ServiceID=%s
                    WHERE ID=%s
                """, (service_date_time, car_id, employee_id, service_id, record_id))
            else:
                cursor.execute("""
                    INSERT INTO technicalservice (ServiceDateTime, CarID, EmployeeID, ServiceID)
                    VALUES (%s, %s, %s, %s)
                """, (service_date_time, car_id, employee_id, service_id))

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
    main_window = AutoserviceWindow()
    main_window.show()
    sys.exit(app.exec_())
