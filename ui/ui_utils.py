"""
Utilidades para mejorar la presentación de la aplicación
"""
import os
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase

def load_stylesheet(app, theme_file="ui/styles.qss"):
    """
    Carga y aplica el archivo de estilos CSS a la aplicación
    """
    try:
        style_path = os.path.join(os.path.dirname(__file__), theme_file)
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
            print("✅ Estilos CSS cargados exitosamente")
        else:
            print("⚠️ Archivo de estilos no encontrado, usando estilos por defecto")
    except Exception as e:
        print(f"❌ Error al cargar estilos: {e}")

def setup_fonts(app):
    """
    Configura las fuentes preferidas para la aplicación
    """
    try:
        # Fuentes preferidas en orden de prioridad
        preferred_fonts = [
            "Segoe UI",
            "Helvetica Neue", 
            "Arial",
            "Liberation Sans",
            "DejaVu Sans"
        ]
        
        font_db = QFontDatabase()
        available_fonts = font_db.families()
        
        # Buscar la primera fuente disponible
        selected_font = "Arial"  # Fallback
        for font_name in preferred_fonts:
            if font_name in available_fonts:
                selected_font = font_name
                break
        
        # Aplicar la fuente seleccionada
        font = QFont(selected_font, 10)
        app.setFont(font)
        print(f"✅ Fuente configurada: {selected_font}")
        
    except Exception as e:
        print(f"❌ Error al configurar fuentes: {e}")

def center_window(window):
    """
    Centra una ventana en la pantalla
    """
    try:
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = window.frameGeometry()
        
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        window.move(window_geometry.topLeft())
        
    except Exception as e:
        print(f"❌ Error al centrar ventana: {e}")

def apply_window_properties(window, title="Menú Saludable Inteligente", icon_path=None):
    """
    Aplica propiedades comunes a las ventanas
    """
    try:
        window.setWindowTitle(f"🍽️ {title}")
        
        # Configurar flags de ventana para mejor apariencia
        window.setWindowFlags(
            Qt.Window | 
            Qt.WindowTitleHint | 
            Qt.WindowCloseButtonHint | 
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint
        )
        
        # Centrar la ventana
        center_window(window)
        
        print(f"✅ Propiedades de ventana aplicadas: {title}")
        
    except Exception as e:
        print(f"❌ Error al aplicar propiedades de ventana: {e}")

def add_tooltips(widget_dict):
    """
    Agrega tooltips informativos a los widgets
    """
    tooltips = {
        'minSpinBox': 'Cantidad mínima de calorías por platillo',
        'maxSpinBox': 'Cantidad máxima de calorías por platillo',
        'vegetarianoRadioButton': 'Excluir productos de origen animal',
        'sinPostreRadioButton': 'No incluir postres en las recomendaciones',
        'generarMenusButton': 'Crear menú basado en tus preferencias actuales',
        'anyCarneRadioButton': 'Cualquier tipo de carne',
        'carneBlancaRadioButton': 'Pollo, pavo, pescado',
        'carneRojaRadioButton': 'Res, cerdo, cordero',
        'carneVegetarianaRadioButton': 'Sustitutos vegetales de carne',
        'nombreUsuario': 'Ingrese su nombre de usuario',
        'passwordUsuario': 'Ingrese su contraseña'
    }
    
    try:
        for widget_name, tooltip_text in tooltips.items():
            if widget_name in widget_dict:
                widget_dict[widget_name].setToolTip(tooltip_text)
        
        print("✅ Tooltips agregados exitosamente")
        
    except Exception as e:
        print(f"❌ Error al agregar tooltips: {e}")

def setup_enhanced_ui(app, window, widget_dict=None):
    """
    Función principal para configurar toda la UI mejorada
    """
    print("🎨 Configurando interfaz mejorada...")
    
    # Cargar estilos CSS
    load_stylesheet(app)
    
    # Configurar fuentes
    setup_fonts(app)
    
    # Aplicar propiedades de ventana
    apply_window_properties(window)
    
    # Agregar tooltips si se proporcionan widgets
    if widget_dict:
        add_tooltips(widget_dict)
    
    print("✨ Configuración de UI completada")

def get_category_style(category):
    """
    Retorna el estilo CSS específico para cada categoría de alimento
    """
    styles = {
        'carnes': """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #e74c3c, stop: 1 #c0392b);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #c0392b, stop: 1 #a93226);
            }
        """,
        'vegetales': """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #27ae60, stop: 1 #229954);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #229954, stop: 1 #1e8449);
            }
        """,
        'carbohidratos': """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #f39c12, stop: 1 #e67e22);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #e67e22, stop: 1 #d35400);
            }
        """,
        'entradas': """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #9b59b6, stop: 1 #8e44ad);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #8e44ad, stop: 1 #7d3c98);
            }
        """,
        'postres': """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #e91e63, stop: 1 #c2185b);
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0 #c2185b, stop: 1 #ad1457);
            }
        """
    }
    
    return styles.get(category, "")

def show_status_message(status_bar, message, timeout=3000):
    """
    Muestra un mensaje en la barra de estado con timeout
    """
    try:
        if status_bar:
            status_bar.showMessage(f"ℹ️ {message}", timeout)
    except Exception as e:
        print(f"❌ Error al mostrar mensaje de estado: {e}")

# Función de prueba para verificar que todo funciona
def test_ui_utilities():
    """
    Función de prueba para las utilidades de UI
    """
    print("🧪 Probando utilidades de UI...")
    
    app = QApplication([])
    test_widget = QWidget()
    
    # Probar cada función
    setup_fonts(app)
    apply_window_properties(test_widget, "Prueba")
    center_window(test_widget)
    
    print("✅ Todas las utilidades funcionan correctamente")
    app.quit()

if __name__ == "__main__":
    test_ui_utilities()