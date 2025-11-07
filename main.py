import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from consultarProlog import *
import sqlite3


class conexion_actual:
    def __init__(self, nombre, alimentos_deseados = None, alimentos_rechazados = None, postre = 'si', vegetariano = 'no', tipo_carne = 'any', min_cal = 0, max_cal = 9999):
        self.nombre = nombre
        self.alimentos_deseados = alimentos_deseados if alimentos_deseados is not None else []
        self.alimentos_rechazados = alimentos_rechazados if alimentos_rechazados is not None else []
        self.postre = postre
        self.vegetariano = vegetariano
        self.tipo_carne = tipo_carne
        self.min_cal = min_cal
        self.max_cal = max_cal

class AlimentoWidget:
    def __init__(self, alimento, user_window):
        global usuario_global
        self.alimento = alimento
        self.user_window = user_window
        self.estado = "neutro"  # neutro, agregado, rechazado
        
        self.buttonAgregar = QPushButton("Agregar")
        self.buttonRechazar = QPushButton("Rechazar")
        
        self.buttonAgregar.clicked.connect(self.agregar_alimento)
        self.buttonRechazar.clicked.connect(self.rechazar_alimento)
        if self.alimento.nombre in usuario_global.alimentos_deseados:
            self.estado = "agregado"
            self.buttonAgregar.setEnabled(False)
            self.buttonAgregar.setText("Agregado ✓")
        elif self.alimento.nombre in usuario_global.alimentos_rechazados:
            self.estado = "rechazado"
            self.buttonRechazar.setEnabled(False)
            self.buttonRechazar.setText("Rechazado ✗")
    
    def agregar_alimento(self):
        global usuario_global
        if self.estado != "agregado":
            # CORRECCIÓN: Remover de rechazados si existe
            if self.alimento.nombre in usuario_global.alimentos_rechazados:
                usuario_global.alimentos_rechazados.remove(self.alimento.nombre)
            
            # CORRECCIÓN: Agregar a DESEADOS, no a rechazados
            if self.alimento.nombre not in usuario_global.alimentos_deseados:
                usuario_global.alimentos_deseados.append(self.alimento.nombre)

            QMessageBox.information(self.user_window, "Agregar Alimento", 
                                  f"{self.alimento.nombre} agregado al plan de comidas.")
            self.estado = "agregado"
            self.buttonAgregar.setEnabled(False)
            self.buttonAgregar.setText("Agregado ✓")
            self.buttonRechazar.setEnabled(True)
            self.buttonRechazar.setText("Rechazar")
    
    def rechazar_alimento(self):
        global usuario_global
        if self.estado != "rechazado":
            # Remover de deseados si existe
            if self.alimento.nombre in usuario_global.alimentos_deseados:
                usuario_global.alimentos_deseados.remove(self.alimento.nombre)
            
            # Agregar a rechazados si no existe
            if self.alimento.nombre not in usuario_global.alimentos_rechazados:
                usuario_global.alimentos_rechazados.append(self.alimento.nombre)
            
            QMessageBox.information(self.user_window, "Rechazar Alimento", 
                                  f"{self.alimento.nombre} rechazado.")
            self.estado = "rechazado"
            self.buttonRechazar.setEnabled(False)
            self.buttonRechazar.setText("Rechazado ✗")
            self.buttonAgregar.setEnabled(True)
            self.buttonAgregar.setText("Agregar")

usuario_global = None

def verificar_usuario(nombre, password, window, user_window):
    global usuario_global
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    cursor.execute('''
        select * from usuarios
    ''')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        if usuario[0] == nombre and usuario[1] == password:
            usuario_global = conexion_actual(nombre)
            QMessageBox.information(window, "Inicio de sesión", "¡Inicio de sesión exitoso!")
            window.close()
            user_window.show()
            layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "carne")
            return

    QMessageBox.warning(window, "Inicio de sesión", "Nombre de usuario o contraseña incorrectos.")
    return 

def crear_usuario(nombre, password, window, user_window):
    global usuario_global
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
        return 
    usuario_global = conexion_actual(nombre)
    layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "carne")

def layoutAlimentos(alimentos, user_window, tipo):
    global usuario_global
    if user_window.scrollAreaAlimentos.widget():
        user_window.scrollAreaAlimentos.widget().deleteLater()
    container_widget = QWidget()
    grid_layout = QGridLayout()
    row = 0
    col = 0
    alimento_widgets = []
    for alimento in alimentos:
        if alimento.tipo == tipo:
            label = f"{alimento.nombre} ({alimento.tipo}) - {alimento.calorias} kcal"
            alimento_widget = AlimentoWidget(alimento, user_window)
            alimento_widgets.append(alimento_widget)
            grid_layout.addWidget(QLabel(f"<img src='{alimento.imagen}' width='100' height='100'>"), row, col)
            grid_layout.addWidget(QLabel(label), row, col + 1)
            grid_layout.addWidget(alimento_widget.buttonAgregar, row, col + 2)
            grid_layout.addWidget(alimento_widget.buttonRechazar, row, col + 3)
            col += 4
            if col >= 4:
                col = 0
                row += 1
    container_widget.setLayout(grid_layout)
    container_widget.alimento_widgets = alimento_widgets
    user_window.scrollAreaAlimentos.setWidget(container_widget)


def habilitarBotonesAlimentos(user_window, cualDesabilitar):
    botones = { "vegetales": user_window.vegetalesButton,
                "carbohidratos": user_window.carbohidratosButton,
                "carnes": user_window.carnesButton,
                "postres": user_window.postresButton,
                "entradas": user_window.entradasButton}
    for key, boton in botones.items():
        boton.setEnabled(key != cualDesabilitar)


def cambiar_estado_vegetariano(nuevo_estado, user_window):
    global usuario_global
    if usuario_global is None:
        return
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    cursor.execute('''
        select nombre,tipoDetalle from vista_alimentos_detalle_filas where tipo='carne' or tipo='entrada'
    ''')
    carnes = cursor.fetchall()
    if nuevo_estado == "si":
        eliminar_tipo_alimento_lista("carne", carnes)
        for carne in carnes:
            if carne[1] != "vegetariana":
                usuario_global.alimentos_rechazados.append(carne[0])
        layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "carne")
        habilitarBotonesAlimentos(user_window, "carnes")
    elif nuevo_estado == "no":
        # Revertir
        eliminar_tipo_alimento_lista("carne", carnes)
        layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "carne")
        habilitarBotonesAlimentos(user_window, "carnes")

def cambiar_estado_postre(nuevo_estado, user_window):
    global usuario_global
    if usuario_global is None:
        return
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    cursor.execute('''
        select nombre from vista_alimentos_detalle_filas where tipo='postre'
    ''')
    postres = cursor.fetchall()
    if nuevo_estado == "no":
        eliminar_tipo_alimento_lista("postre", postres)
        for postre in postres:
            usuario_global.alimentos_rechazados.append(postre[0])
        layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "postre")
        habilitarBotonesAlimentos(user_window, "postres")  
    elif nuevo_estado == "si":
        # Revertir
        eliminar_tipo_alimento_lista("postre", postres)
        layoutAlimentos(fetch_data_from_sqlite('dataBase/menu_inteligente_base.db'), user_window, "postre")
        habilitarBotonesAlimentos(user_window, "postres") 



def eliminar_tipo_alimento_lista(tipo, lista):
    global usuario_global
    for alimento in usuario_global.alimentos_deseados:
        for item in lista:
            if alimento == item[0]:
                usuario_global.alimentos_deseados.remove(alimento)
    for alimento in usuario_global.alimentos_rechazados:
        for item in lista:
            if alimento == item[0]:
                usuario_global.alimentos_rechazados.remove(alimento)


def main():
    global usuario_global
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

    # Funciones para sincronizar los SpinBox
    def on_min_changed(value):
        if usuario_global:
            usuario_global.min_cal = value
        # Asegurar que el máximo del minSpinBox sea el valor actual del maxSpinBox
        user_window.minSpinBox.setMaximum(user_window.maxSpinBox.value())
        # Si el valor mínimo es mayor que el máximo, ajustar el máximo
        if value >= user_window.maxSpinBox.value():
            user_window.maxSpinBox.setValue(value + 1)
            usuario_global.max_cal = value + 1

    def on_max_changed(value):
        if usuario_global:
            usuario_global.max_cal = value
        # Asegurar que el mínimo del maxSpinBox sea el valor actual del minSpinBox
        user_window.maxSpinBox.setMinimum(user_window.minSpinBox.value())
        # Si el valor máximo es menor que el mínimo, ajustar el mínimo
        if value <= user_window.minSpinBox.value():
            user_window.minSpinBox.setValue(value - 1)
            usuario_global.min_cal = value - 1

    def generic_RadioButton_handler(radio_button, attribute_name, true_value, false_value):
        if usuario_global:
            if radio_button.isChecked():
                setattr(usuario_global, attribute_name, true_value)
            else:
                setattr(usuario_global, attribute_name, false_value)



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
    user_window.minSpinBox.valueChanged.connect(
        lambda value: on_min_changed(value))
    user_window.maxSpinBox.valueChanged.connect(
        lambda value: on_max_changed(value))
    user_window.sinPostreRadioButton.toggled.connect(
        lambda: (generic_RadioButton_handler(user_window.sinPostreRadioButton, 'postre', 'no', 'si'),
               cambiar_estado_postre('no' if user_window.sinPostreRadioButton.isChecked() else 'si', user_window)))
    user_window.vegetarianoRadioButton.toggled.connect(
        lambda: (generic_RadioButton_handler(user_window.vegetarianoRadioButton, 'vegetariano', 'si', 'no'),
               cambiar_estado_vegetariano('si' if user_window.vegetarianoRadioButton.isChecked() else 'no', user_window)))
    user_window.anyCarneRadioButton.toggled.connect(
        lambda: generic_RadioButton_handler(user_window.anyCarneRadioButton, 'tipo_carne', 'any', usuario_global.tipo_carne))
    user_window.carneBlancaRadioButton.toggled.connect(
        lambda: generic_RadioButton_handler(user_window.carneBlancaRadioButton, 'tipo_carne', 'blanca', usuario_global.tipo_carne))
    user_window.carneRojaRadioButton.toggled.connect(
        lambda: generic_RadioButton_handler(user_window.carneRojaRadioButton, 'tipo_carne', 'roja', usuario_global.tipo_carne))
    user_window.carneVegetarianaRadioButton.toggled.connect(
        lambda: generic_RadioButton_handler(user_window.carneVegetarianaRadioButton, 'tipo_carne', 'vegetariana', usuario_global.tipo_carne))

    user_window.generarMenusButton.clicked.connect(
        lambda: query_Menus(
            usuario_global.nombre,
            usuario_global.postre,
            usuario_global.vegetariano,
            usuario_global.tipo_carne,
            usuario_global.min_cal,
            usuario_global.max_cal,
            usuario_global.alimentos_deseados,
            usuario_global.alimentos_rechazados
        )
    )

    sys.exit(app.exec())

            
    


if __name__ == "__main__":
    main()