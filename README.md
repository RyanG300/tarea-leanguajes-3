# 🍽️ Menú Saludable Inteligente

## Descripción

Sistema inteligente de recomendación de menús saludables que utiliza Prolog para la lógica de recomendaciones y PySide6 para una interfaz gráfica moderna y atractiva.

## ✨ Características principales

### 🎨 Interfaz Mejorada

- **Diseño moderno**: Interface actualizada con colores atractivos y elementos visuales mejorados
- **Íconos intuitivos**: Emojis y símbolos que facilitan la navegación
- **Gradientes y sombras**: Efectos visuales que dan profundidad a la aplicación
- **Responsive**: Mejor distribución de elementos en pantalla

### 🍎 Funcionalidades

- **Categorización de alimentos**: Carnes, vegetales, carbohidratos, entradas y postres
- **Filtros personalizados**: Rango de calorías, preferencias vegetarianas, tipos de carne
- **Generación inteligente**: Menús basados en preferencias del usuario
- **Sistema de usuarios**: Login y registro con persistencia de preferencias

### 🧠 Tecnologías

- **Frontend**: PySide6 (Qt6) con estilos CSS personalizados
- **Backend**: Python con integración a Prolog
- **Base de datos**: SQLite para persistencia de datos
- **Lógica**: SWI-Prolog para recomendaciones inteligentes

## 🚀 Mejoras Visuales Implementadas

### Pantalla de Login

- Gradiente de fondo azul suave
- Campos de entrada con bordes redondeados y efectos de enfoque
- Botones con gradientes y efectos hover
- Íconos representativos (👤 para usuario, 🔒 para contraseña)
- Título prominente con emoji 🍽️

### Pantalla Principal

- Botones de categoría con colores temáticos:
  - 🥩 Carnes: Rojo
  - 🥬 Vegetales: Verde
  - 🍞 Carbohidratos: Naranja
  - 🥗 Entradas: Morado
  - 🍰 Postres: Rosa
- Secciones organizadas en grupos con bordes y títulos
- Áreas de desplazamiento mejoradas
- Menú superior estilizado

### Elementos de UI

- **Campos de entrada**: Bordes suaves, efectos de enfoque
- **Botones**: Gradientes, sombras y animaciones hover
- **Radio buttons**: Indicadores circulares personalizados
- **Spin boxes**: Estilos coherentes con el resto de la aplicación
- **Scroll areas**: Bordes redondeados y fondos suaves

## 📋 Instalación y Uso

### Prerrequisitos

```bash
pip install PySide6
pip install sqlite3
# SWI-Prolog instalado en el sistema
```

### Ejecución

```bash
python main.py
```

## 🎯 Funcionalidades del Sistema

### Gestión de Usuarios

- Registro de nuevos usuarios
- Inicio de sesión
- Persistencia de preferencias personalizadas

### Recomendaciones Inteligentes

- Algoritmos en Prolog para sugerir combinaciones
- Filtrado por calorías
- Consideración de restricciones dietéticas
- Aprendizaje de preferencias del usuario

### Categorías de Alimentos

- **Proteínas**: Diferentes tipos de carne y opciones vegetarianas
- **Vegetales**: Variedad de opciones verdes y coloridas
- **Carbohidratos**: Fuentes de energía balanceadas
- **Entradas**: Aperitivos y acompañamientos
- **Postres**: Opciones dulces opcionales

## 🛠️ Estructura del Proyecto

```
├── ui/
│   ├── main_ui.ui          # Interfaz de login mejorada
│   ├── vista_usuario.ui    # Interfaz principal mejorada
│   └── styles.qss          # Estilos CSS personalizados
├── prolog_logic/           # Lógica de recomendaciones
├── dataBase/               # Base de datos SQLite
├── imagenes/               # Recursos visuales
└── main.py                 # Punto de entrada de la aplicación
```

## 🎨 Detalles de Diseño

### Paleta de Colores

- **Azul principal**: #3498db (botones principales)
- **Verde**: #27ae60 (vegetales, crear usuario)
- **Rojo**: #e74c3c (carnes)
- **Naranja**: #f39c12 (carbohidratos, generar)
- **Morado**: #9b59b6 (entradas)
- **Rosa**: #e91e63 (postres)
- **Gris oscuro**: #2c3e50 (texto, menú)

### Tipografía

- **Familia**: Segoe UI, Helvetica, Arial
- **Pesos**: Regular (500), Bold (700)
- **Tamaños**: 11px-18px según jerarquía

## 📝 Notas de Desarrollo

Las mejoras visuales se implementaron manteniendo la funcionalidad original del sistema. Se priorizó:

- **Usabilidad**: Mejor experiencia de usuario
- **Accesibilidad**: Contraste adecuado y tamaños legibles
- **Consistencia**: Estilo unificado en toda la aplicación
- **Modernidad**: Tendencias actuales de UI/UX

## 🤝 Contribuciones

El sistema está listo para futuras mejoras y extensiones. Las áreas de oportunidad incluyen:

- Animaciones más fluidas
- Modo oscuro/claro
- Responsive design para diferentes tamaños de pantalla
- Más categorías de alimentos
- Exportación de menús a PDF

---

_Proyecto desarrollado como parte del curso de Lenguajes de Programación_
