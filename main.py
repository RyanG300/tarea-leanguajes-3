import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from insertarEnProlog import *
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
            layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "carne")
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
            buttonAgregar.clicked.connect(lambda checked, a=alimento: (QMessageBox.information(user_window, "Agregar Alimento", f"{a.nombre} agregado al plan de comidas."), 
                                            a.establecer_deseado(True),
                                            layoutPlatillos(a.nombre, user_window)))
            buttonRechazar = QPushButton("Rechazar")
            buttonRechazar.clicked.connect(lambda checked, a=alimento: (QMessageBox.information(user_window, "Rechazar Alimento", f"{a.nombre} rechazado."), 
                                            a.establecer_deseado(False),
                                            layoutPlatillos(a.nombre, user_window)))

            grid_layout.addWidget(QLabel(f"<img src='{alimento.imagen}' width='100' height='100'>"), row, col)
            grid_layout.addWidget(QLabel(label), row, col + 1)
            grid_layout.addWidget(buttonAgregar, row, col + 2)
            grid_layout.addWidget(buttonRechazar, row, col + 3)
            col += 4
            if col >= 4:
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
    cursor.execute('''
        SELECT platillo, ingredientes, total_calorias from vista_platillos_ingredientes_resumen  
    ''')
    platillos = cursor.fetchall()
    row = 0
    col = 0
    for platillo in platillos:
        nombre_platillo, ingredientes, total_calorias = platillo
        if alimento in ingredientes.split(', '):
            label = f"{nombre_platillo} - Ingredientes: {ingredientes} - Total Calorías: {total_calorias} kcal"
            grid_layout.addWidget(QLabel(label), row, col)
            col += 1
            if col >= 1:
                col = 0
                row += 1
    container_widget.setLayout(grid_layout)
    user_window.scrollAreaPlatillos.setWidget(container_widget)

def habilitarBotonesAlimentos(user_window, cualDesabilitar):
    botones = { "vegetales": user_window.vegetalesButton,
                "carbohidratos": user_window.carbohidratosButton,
                "carnes": user_window.carnesButton,
                "postres": user_window.postresButton,
                "entradas": user_window.entradasButton}
    for key, boton in botones.items():
        boton.setEnabled(key != cualDesabilitar)
    


def main():
    app = QApplication(sys.argv)
    tipos_alimentos = fetch_data_from_sqlite('dataBase/menu_inteligente_base.db')
    
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
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "vegetal"),
        habilitarBotonesAlimentos(user_window, "vegetales")))
    user_window.carbohidratosButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "carbohidrato"),
        habilitarBotonesAlimentos(user_window, "carbohidratos")))
    user_window.carnesButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "carne"),
        habilitarBotonesAlimentos(user_window, "carnes")))
    user_window.postresButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "postre"),
        habilitarBotonesAlimentos(user_window, "postres")))
    user_window.entradasButton.clicked.connect(
        lambda: (layoutAlimentos(tipos_alimentos, user_window, "entrada"),
        habilitarBotonesAlimentos(user_window, "entradas")))


    sys.exit(app.exec())

            
    


if __name__ == "__main__":
    main()