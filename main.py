import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from tipoAlimento import crearTipos
import sqlite3



def verificar_usuario(nombre, password, window):
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    cursor.execute('''
        select * from usuarios
    ''')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        if usuario[1] == nombre and usuario[2] == password:
            return QMessageBox.information(window, "Inicio de sesión", "¡Inicio de sesión exitoso!")
    return QMessageBox.warning(window, "Inicio de sesión", "Nombre de usuario o contraseña incorrectos.")

def crear_usuario(nombre, password, window):
    try:
        conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
        cursor = conexion.cursor()
        cursor.execute('''
            insert into usuarios (nombre, contraseña) values (?, ?)
        ''', (nombre, password))
        conexion.commit()
        QMessageBox.information(window, "Registro", "¡Usuario registrado exitosamente!")
    except sqlite3.IntegrityError:
        QMessageBox.warning(window, "Registro", "El nombre de usuario ya existe.")

def main():
    app = QApplication(sys.argv)
    loader = QUiLoader()
    file = QFile("main_ui.ui")
    file.open(QFile.ReadOnly)
    window = loader.load(file)
    file.close()
    
    #Botones iniciar sesión y crear usuario
    window.iniciarSesion.clicked.connect(
        lambda: verificar_usuario(window.nombreUsuario.text(), window.passwordUsuario.text(), window))
    window.crearUsuario.clicked.connect(
        lambda: crear_usuario(window.nombreUsuario.text(), window.passwordUsuario.text(), window))
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()