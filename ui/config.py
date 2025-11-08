# Configuración para mejorar la presentación de la aplicación

## Fuentes recomendadas (si están disponibles en el sistema)
FONTS = [
    "Segoe UI",
    "Helvetica Neue", 
    "Arial",
    "Liberation Sans",
    "DejaVu Sans",
    "sans-serif"
]

## Colores del tema
COLORS = {
    # Colores principales
    'primary': '#3498db',
    'primary_dark': '#2980b9',
    'primary_darker': '#2471a3',
    
    # Colores de categorías
    'carnes': '#e74c3c',
    'vegetales': '#27ae60', 
    'carbohidratos': '#f39c12',
    'entradas': '#9b59b6',
    'postres': '#e91e63',
    
    # Colores de UI
    'background': '#f8f9fa',
    'background_gradient_end': '#e9ecef',
    'text': '#2c3e50',
    'text_secondary': '#34495e',
    'border': '#bdc3c7',
    'white': '#ffffff',
    
    # Estados
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db'
}

## Tamaños y dimensiones
SIZES = {
    'border_radius': 8,
    'border_radius_small': 5,
    'border_radius_large': 10,
    'padding_small': 5,
    'padding_medium': 8,
    'padding_large': 12,
    'button_min_height': 30,
    'button_large_height': 40,
    'input_height': 30
}

## Configuración de ventanas
WINDOW_CONFIG = {
    'login': {
        'width': 450,
        'height': 350,
        'resizable': True,
        'center': True
    },
    'main': {
        'width': 800,
        'height': 600, 
        'resizable': True,
        'center': True
    }
}

## Íconos y emojis para categorías
CATEGORY_ICONS = {
    'carnes': '🥩',
    'vegetales': '🥬', 
    'carbohidratos': '🍞',
    'entradas': '🥗',
    'postres': '🍰',
    'usuario': '👤',
    'password': '🔒',
    'menu': '🍽️',
    'configuracion': '⚙️',
    'calorias': '📊',
    'especiales': '🌱',
    'generar': '✨',
    'ayuda': '📚',
    'info': 'ℹ️',
    'salir': '🚪',
    'vegetariano': '🥕',
    'sin_postre': '🚫'
}

## Efectos y animaciones
EFFECTS = {
    'shadow_light': 'box-shadow: 0 2px 4px rgba(0,0,0,0.1);',
    'shadow_medium': 'box-shadow: 0 4px 8px rgba(0,0,0,0.2);',
    'shadow_heavy': 'box-shadow: 0 8px 16px rgba(0,0,0,0.3);',
    'focus_glow': 'box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);',
    'transition': 'transition: all 0.3s ease;'
}

## Mensajes de la aplicación
MESSAGES = {
    'welcome': '¡Bienvenido al sistema de menús saludables!',
    'login_success': 'Inicio de sesión exitoso',
    'login_error': 'Credenciales incorrectas',
    'user_created': 'Usuario creado exitosamente',
    'menu_generated': 'Menú generado según tus preferencias',
    'no_results': 'No se encontraron resultados con los criterios especificados',
    'loading': 'Generando recomendaciones...'
}

## Tooltips informativos
TOOLTIPS = {
    'calorias_min': 'Cantidad mínima de calorías por platillo',
    'calorias_max': 'Cantidad máxima de calorías por platillo', 
    'vegetariano': 'Excluir productos de origen animal',
    'sin_postre': 'No incluir postres en las recomendaciones',
    'generar_menu': 'Crear menú basado en tus preferencias actuales',
    'carne_any': 'Cualquier tipo de carne',
    'carne_blanca': 'Pollo, pavo, pescado',
    'carne_roja': 'Res, cerdo, cordero',
    'carne_vegetariana': 'Sustitutos vegetales de carne'
}