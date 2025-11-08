import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from consultarProlog import *
from insertarEnProlog import guardar_todo_aprendizaje_en_bd
import sqlite3

def cargar_preferencias_usuario(nombre_usuario):
    """
    Carga las preferencias guardadas del usuario desde la base de datos
    """
    conexion = sqlite3.connect("dataBase/menu_inteligente_base.db")
    cursor = conexion.cursor()
    
    preferencias = {
        'calorias_min': 0,
        'calorias_max': 9999,
        'tipo_carne': 'any',
        'postre': 'si',
        'vegetariano': 'no',
        'alimentos_deseados': [],
        'alimentos_rechazados': []
    }
    
    try:
        # Cargar reglas de preferencias
        cursor.execute('''
            SELECT tipo_regla, categoria, valor, valor_numerico 
            FROM regla_usuarios 
            WHERE nombre = ?
        ''', (nombre_usuario,))
        
        reglas = cursor.fetchall()
        
        for regla in reglas:
            tipo_regla, categoria, valor, valor_numerico = regla
            
            if tipo_regla == 'preferencia':
                if categoria == 'calorias_promedio' and valor_numerico:
                    # Usar el promedio como base para el rango
                    promedio = valor_numerico
                    preferencias['calorias_min'] = max(0, int(promedio - 200))
                    preferencias['calorias_max'] = int(promedio + 200)
                
                elif categoria == 'carne' and valor:
                    if valor == 'vegetariana':
                        preferencias['vegetariano'] = 'si'
                        preferencias['tipo_carne'] = 'vegetariana'
                    elif valor in ['blanca', 'roja']:
                        preferencias['tipo_carne'] = valor
                
                elif categoria == 'postre' and valor:
                    preferencias['postre'] = 'si' if valor != 'none' else 'no'
        
        # Cargar menús aceptados para inferir preferencias adicionales
        cursor.execute('''
            SELECT m.idMenu
            FROM menu m
            WHERE m.nombre = ? AND m.aceptado = 1
            ORDER BY m.idMenu DESC
            LIMIT 5
        ''', (nombre_usuario,))
        
        menus_recientes = cursor.fetchall()
        
        # Analizar patrones en menús recientes
        if menus_recientes:
            # Obtener ingredientes más frecuentes
            menu_ids = [str(menu[0]) for menu in menus_recientes]
            if menu_ids:
                cursor.execute(f'''
                    SELECT a.nombre, COUNT(*) as frecuencia
                    FROM ingredientes_Menu im
                    JOIN alimentos a ON im.idAlimento = a.idAlimento
                    WHERE im.idMenu IN ({','.join(['?' for _ in menu_ids])})
                    GROUP BY a.nombre
                    ORDER BY frecuencia DESC
                    LIMIT 3
                ''', menu_ids)
                
                ingredientes_frecuentes = cursor.fetchall()
                preferencias['alimentos_deseados'] = [ing[0] for ing in ingredientes_frecuentes]
        
    except Exception as e:
        print(f"Error cargando preferencias: {e}")
    finally:
        conexion.close()
    
    return preferencias

def aplicar_preferencias_interfaz(user_window, preferencias):
    """
    Aplica las preferencias cargadas a la interfaz de usuario
    """
    try:
        # Aplicar configuración de postre
        if preferencias['postre'] == 'no':
            if hasattr(user_window, 'sinPostreRadioButton'):
                user_window.sinPostreRadioButton.setChecked(True)
        
        # Aplicar configuración de vegetariano
        if preferencias['vegetariano'] == 'si':
            if hasattr(user_window, 'vegetarianoRadioButton'):
                user_window.vegetarianoRadioButton.setChecked(True)
        
        # Aplicar rango de calorías
        if hasattr(user_window, 'minSpinBox'):
            user_window.minSpinBox.setValue(preferencias['calorias_min'])
        
        if hasattr(user_window, 'maxSpinBox'):
            user_window.maxSpinBox.setValue(preferencias['calorias_max'])
        
        # Aplicar tipo de carne
        tipo_carne = preferencias['tipo_carne']
        if tipo_carne == 'any' and hasattr(user_window, 'anyCarneRadioButton'):
            user_window.anyCarneRadioButton.setChecked(True)
        elif tipo_carne == 'blanca' and hasattr(user_window, 'carneBlancaRadioButton'):
            user_window.carneBlancaRadioButton.setChecked(True)
        elif tipo_carne == 'roja' and hasattr(user_window, 'carneRojaRadioButton'):
            user_window.carneRojaRadioButton.setChecked(True)
        elif tipo_carne == 'vegetariana' and hasattr(user_window, 'carneVegetarianaRadioButton'):
            user_window.carneVegetarianaRadioButton.setChecked(True)
        
        # Mostrar alimentos deseados sugeridos
        if preferencias['alimentos_deseados']:
            alimentos_texto = ", ".join(preferencias['alimentos_deseados'][:3])  # Solo mostrar los 3 más frecuentes
            QMessageBox.information(user_window, "Preferencias cargadas", 
                                  f"🎯 Basándome en tus menús anteriores, te sugiero incluir:\n\n{alimentos_texto}\n\n" +
                                  f"📊 Configuración aplicada:\n• Calorías: {preferencias['calorias_min']}-{preferencias['calorias_max']}\n" +
                                  f"• Tipo de carne: {preferencias['tipo_carne']}\n• Postre: {preferencias['postre']}")
        
        print(f"✅ Preferencias aplicadas: Calorías {preferencias['calorias_min']}-{preferencias['calorias_max']}, "
              f"Carne: {preferencias['tipo_carne']}, Postre: {preferencias['postre']}")
    
    except Exception as e:
        print(f"Error aplicando preferencias a la interfaz: {e}")


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
menus_actuales = None

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
            # Cargar preferencias del usuario
            preferencias = cargar_preferencias_usuario(nombre)
            
            # Crear conexión actual con preferencias cargadas
            usuario_global = conexion_actual(
                nombre, 
                alimentos_deseados=preferencias['alimentos_deseados'],
                alimentos_rechazados=preferencias['alimentos_rechazados'],
                postre=preferencias['postre'],
                vegetariano=preferencias['vegetariano'],
                tipo_carne=preferencias['tipo_carne'],
                min_cal=preferencias['calorias_min'],
                max_cal=preferencias['calorias_max']
            )
            
            QMessageBox.information(window, "Inicio de sesión", "¡Inicio de sesión exitoso!")
            window.close()
            user_window.show()
            
            # Aplicar preferencias a la interfaz
            aplicar_preferencias_interfaz(user_window, preferencias)
            
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
            label = f"{alimento.nombre} ({alimento.tipo} {alimento.tipoDetalle if alimento.tipoDetalle else ''}) - {alimento.calorias} kcal"
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

def seleccionar_menu_con_opciones(user_window, item, menu_label):
    """
    Maneja la selección de un menú y ofrece opciones al usuario para continuar o salir
    """
    global usuario_global, menus_actuales
    
    # Mostrar el menú seleccionado
    QMessageBox.information(user_window, "Menú Seleccionado", f"Ha seleccionado el menú:\n\n{menu_label}")
    
    # Guardar los datos del menú seleccionado
    menus_actuales.guardar_datos_usuario_en_prolog(usuario_global.nombre, item)
    guardar_todo_aprendizaje_en_bd(usuario_global.nombre)
    
    # Crear diálogo con opciones
    dialog = QMessageBox(user_window)
    dialog.setWindowTitle("¿Qué desea hacer ahora?")
    dialog.setText("Su menú ha sido seleccionado y guardado exitosamente.")
    dialog.setInformativeText("¿Desea elegir otro menú o salir de la aplicación?")
    
    # Agregar botones personalizados
    boton_otro_menu = dialog.addButton("Elegir otro menú", QMessageBox.ActionRole)
    boton_salir = dialog.addButton("Salir", QMessageBox.RejectRole)
    
    dialog.exec()
    
    # Manejar la respuesta del usuario
    if dialog.clickedButton() == boton_otro_menu:
        # Limpiar el área de menús para generar nuevos
        if user_window.scrollAreaMenus.widget():
            user_window.scrollAreaMenus.widget().deleteLater()
        # No hacer nada más, el usuario puede configurar nuevas preferencias y generar más menús
        QMessageBox.information(user_window, "Continuar", "Puede ajustar sus preferencias y generar nuevos menús cuando guste.")
    elif dialog.clickedButton() == boton_salir:
        # Cerrar la aplicación completamente
        user_window.close()
        QApplication.quit()

def generar_menus(user_window):
    global usuario_global
    global menus_actuales
    if usuario_global is None:
        QMessageBox.warning(user_window, "Generar Menús", "Debe iniciar sesión primero.")
        return
    menus_actuales = query_Menus(
        usuario_global.nombre,
        usuario_global.postre,
        usuario_global.vegetariano,
        usuario_global.tipo_carne,
        usuario_global.min_cal,
        usuario_global.max_cal,
        usuario_global.alimentos_deseados,
        usuario_global.alimentos_rechazados
    )
    if not menus_actuales.menus:
        QMessageBox.information(user_window, "Generar Menús", "No se encontraron menús que coincidan con sus preferencias.")
        return
    if user_window.scrollAreaMenus.widget():
        user_window.scrollAreaMenus.widget().deleteLater()
    container_widget = QWidget()
    grid_layout = QGridLayout()
    row = 0
    col = 0 
    for resultado in menus_actuales.menus:
        for item in resultado['Menus']:
            parsed = menus_actuales.parse_menu_item(item)
            e, c, x, y, p, cal = parsed
            e, c, x, y, p = map(lambda s: str(s).replace("_", " "), [e, c, x, y, p])
            cal = str(cal).strip()
            label = (f"Entrada: {e}\n"
                     f"Plato fuerte: {c}, {x}, {y}\n"
                     f"Postre: {p}\n"
                     f"Calorías: {cal}")
            button = QPushButton("Seleccionar")
            button.clicked.connect(lambda checked, item=item, menu_label=label: seleccionar_menu_con_opciones(user_window, item, menu_label))
            grid_layout.addWidget(QLabel(label), row, col)
            grid_layout.addWidget(button, row + 1, col)
            col += 1
    container_widget.setLayout(grid_layout)
    user_window.scrollAreaMenus.setWidget(container_widget)

def main():
    global usuario_global
    app = QApplication(sys.argv)
    tipos_alimentos = fetch_data_from_sqlite('dataBase/menu_inteligente_base.db')
    realizar_carga()
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
        lambda: generar_menus(user_window)
    )

    sys.exit(app.exec())

            
    


if __name__ == "__main__":
    main()