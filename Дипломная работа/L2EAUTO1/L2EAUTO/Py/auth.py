import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
import os

# Получение абсолютного пути к проекту
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_dir = os.path.join(base_dir, '../UI_forms')

class AuthWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AuthWindow, self).__init__()
        uic.loadUi(os.path.join(ui_dir, 'auth.ui'), self)

        # Установка режима отображения пароля
        self.password_login.setEchoMode(QtWidgets.QLineEdit.Password)

        # Подключение кнопки входа к функции аутентификации
        self.enter_button.clicked.connect(self.authenticate)

    def authenticate(self):
        login = self.login_input.text()
        password = self.password_login.text()

        # Проверка жестко закодированных учетных данных администратора
        if login == "admin" and password == "admin":
            self.open_admin_window()
            return

        # Инициализация переменных
        conn = None
        cursor = None

        # Подключение к базе данных
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # замените на ваше имя пользователя
                password="",  # замените на ваш пароль
                database="l2eauto"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees WHERE Login = %s AND Password = %s", (login, password))
            user = cursor.fetchone()

            if user:
                position_id = user["PositionID"]
                if self.is_manager(position_id):
                    self.open_manager_window()
                elif self.is_mechanic(position_id):
                    self.open_autoservice_window()
                else:
                    self.show_error_message("Неизвестная позиция пользователя")
            else:
                self.show_error_message("Неверный логин или пароль")
        except mysql.connector.Error as err:
            self.show_error_message(f"Ошибка подключения к БД: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def is_manager(self, position_id):
        # Предположим, что ID позиции для менеджеров - 2 или 3
        return position_id in [2, 3]

    def is_mechanic(self, position_id):
        # Предположим, что ID позиции для механиков - 4 или 5
        return position_id in [4, 5]

    def open_admin_window(self):
        from admin_panel import AdminWindow
        self.admin_window = AdminWindow(self)
        self.admin_window.show()
        self.close()

    def open_manager_window(self):
        from manager import ManagerApp
        self.manager_window = ManagerApp(self)
        self.manager_window.show()
        self.close()

    def open_autoservice_window(self):
        from autoservice_panel import AutoserviceWindow
        self.autoservice_window = AutoserviceWindow()
        self.autoservice_window.show()
        self.close()

    def show_error_message(self, message):
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.showMessage(message)

    def clear_inputs(self):
        self.login_input.clear()
        self.password_login.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
