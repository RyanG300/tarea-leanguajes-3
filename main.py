import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from tipoAlimento import crearTipos
import sqlite3


def verificar_usuario(nombre, password, window, user_window):
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    cursor.execute('''
        select * from usuarios
    ''')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        if usuario[0] == nombre and usuario[1] == password:
            QMessageBox.information(window, "Inicio de sesión", "¡Inicio de sesión exitoso!")
            window.close()
            user_window.show()
            layoutAlimentos(crearTipos(), user_window, "Carne")
            return

    return QMessageBox.warning(window, "Inicio de sesión", "Nombre de usuario o contraseña incorrectos.")

def crear_usuario(nombre, password, window, user_window):
    try:
        if(not nombre or not password):
            QMessageBox.warning(window, "Registro", "El nombre de usuario y la contraseña no pueden estar vacíos.")
            return
        conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
        cursor = conexion.cursor()
        cursor.execute('''
            insert into usuarios (nombre, contraseña) values (?, ?)
        ''', (nombre, password))
        conexion.commit()
        QMessageBox.information(window, "Registro", "¡Usuario registrado exitosamente!")
        window.close()
        user_window.show()
    except sqlite3.IntegrityError:
        QMessageBox.warning(window, "Registro", "El nombre de usuario ya existe.")

def layoutAlimentos(alimentos, user_window, tipo):
    if user_window.scrollAreaAlimentos.widget():
        user_window.scrollAreaAlimentos.widget().deleteLater()
    container_widget = QWidget()
    grid_layout = QGridLayout()
    row = 0
    col = 0
    for alimento in alimentos:
        if alimento.tipo == tipo:
            label = f"{alimento.nombre} ({alimento.tipo}) - {alimento.calorias} kcal"
            buttonAgregar = QPushButton("Agregar")
            buttonAgregar.clicked.connect(lambda checked, a=alimento: (QMessageBox.information(user_window, "Agregar Alimento", f"{a.nombre} agregado al plan de comidas."), a.establecer_deseado(True)))
            buttonRechazar = QPushButton("Rechazar")
            buttonRechazar.clicked.connect(lambda checked, a=alimento: (QMessageBox.information(user_window, "Rechazar Alimento", f"{a.nombre} rechazado."), a.establecer_deseado(False)))

            grid_layout.addWidget(QLabel(label), row, col)
            grid_layout.addWidget(buttonAgregar, row, col + 1)
            grid_layout.addWidget(buttonRechazar, row, col + 2)
            col += 3
            if col >= 3:
                col = 0
                row += 1
    container_widget.setLayout(grid_layout)
    user_window.scrollAreaAlimentos.setWidget(container_widget)

def layoutPlatillos(alimento, user_window):
    if user_window.scrollAreaPlatillos.widget():
        user_window.scrollAreaPlatillos.widget().deleteLater()
    container_widget = QWidget()
    grid_layout = QGridLayout()
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    
    
    row = 0
    col = 0

def habilitarBotonesAlimentos(user_window, cualDesabilitar):
    botones = { "vegetales": user_window.vegetalesButton,
                "frutas": user_window.frutasButton,
                "carnes": user_window.carnesButton,
                "bebidas_frias": user_window.bebidasFriasButton,
                "bebidas_calientes": user_window.bebidasCalientesButton,
                "nose": user_window.pushButton}
    for key, boton in botones.items():
        boton.setEnabled(key != cualDesabilitar)
    


def main():
    app = QApplication(sys.argv)
    tipos_alimentos = crearTipos()
    
    # Cargar ventana principal
    loader = QUiLoader()
    file = QFile("ui/main_ui.ui")
    file.open(QFile.ReadOnly)
    window = loader.load(file)
    file.close()
    
    # Cargar ventana de usuario
    file = QFile("ui/vista_usuario.ui")
    file.open(QFile.ReadOnly)
    user_window = loader.load(file)
    file.close()

    #Botones iniciar sesión y crear usuario (ventana principal)
    window.iniciarSesion.clicked.connect(
        lambda: verificar_usuario(window.nombreUsuario.text(), window.passwordUsuario.text(), window, user_window))
    window.crearUsuario.clicked.connect(
        lambda: crear_usuario(window.nombreUsuario.text(), window.passwordUsuario.text(), window, user_window))
    window.show()

    #Botones de la ventana de usuario 
    user_window.actionSobre.triggered.connect(
        lambda: QMessageBox.information(user_window, "Sobre", "Aplicación de Menú Saludable Inteligente"))
    user_window.actionSalir.triggered.connect(
        lambda: (user_window.close(), window.show(),window.nombreUsuario.clear(), 
                 window.passwordUsuario.clear()))
    user_window.vegetalesButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "Vegetal"),
        habilitarBotonesAlimentos(user_window, "vegetales")))
    user_window.frutasButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "Fruta"),
        habilitarBotonesAlimentos(user_window, "frutas")))
    user_window.carnesButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "Carne"),
        habilitarBotonesAlimentos(user_window, "carnes")))
    user_window.bebidasFriasButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "Bebidas frías"),
        habilitarBotonesAlimentos(user_window, "bebidas_frias")))
    user_window.bebidasCalientesButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "Bebidas calientes"),
        habilitarBotonesAlimentos(user_window, "bebidas_calientes")))


    sys.exit(app.exec())

            
    


if __name__ == "__main__":
    main()