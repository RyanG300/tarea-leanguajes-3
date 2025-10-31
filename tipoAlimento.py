import sqlite3

class TipoAlimento:
    def __init__(self, nombre: str, tipo: str, calorias: int, deseado = True):
        self.nombre = nombre
        self.tipo = tipo
        self.calorias = calorias
        self.deseado = deseado
    
    def establecer_deseado(self, deseado: bool):
        self.deseado = deseado

# De momento
def crearTipos():
    lista_tipos = []
    
    conexion = sqlite3.connect('dataBase/menu_inteligente_base.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT nombre, tipo, calorias FROM alimentos')
    filas = cursor.fetchall()
    for fila in filas:
        nombre, tipo, calorias = fila
        tipo_alimento = TipoAlimento(nombre, tipo, calorias)
        lista_tipos.append(tipo_alimento)
    return lista_tipos

# Frutas
    #lista_tipos.append(TipoAlimento("Manzana", "Fruta", 52))
    #lista_tipos.append(TipoAlimento("Banana", "Fruta", 89))
    #lista_tipos.append(TipoAlimento("Naranja", "Fruta", 47))
    #lista_tipos.append(TipoAlimento("Fresa", "Fruta", 32))
    #lista_tipos.append(TipoAlimento("Uva", "Fruta", 67))
    
    # Carnes
    #lista_tipos.append(TipoAlimento("Pollo", "Carne", 165))
    #lista_tipos.append(TipoAlimento("Res", "Carne", 250))
    #lista_tipos.append(TipoAlimento("Cerdo", "Carne", 242))
    #lista_tipos.append(TipoAlimento("Pescado", "Carne", 206))
    #lista_tipos.append(TipoAlimento("Pavo", "Carne", 135))
    
    # Vegetales
    #lista_tipos.append(TipoAlimento("Brócoli", "Vegetal", 34))
    #lista_tipos.append(TipoAlimento("Zanahoria", "Vegetal", 41))
    #lista_tipos.append(TipoAlimento("Espinaca", "Vegetal", 23))
    #lista_tipos.append(TipoAlimento("Tomate", "Vegetal", 18))
    #lista_tipos.append(TipoAlimento("Lechuga", "Vegetal", 15))

    # Bebidas frías
    #lista_tipos.append(TipoAlimento("Agua", "Bebidas frías", 0))
    #lista_tipos.append(TipoAlimento("Jugo de naranja", "Bebidas frías", 112))
    #lista_tipos.append(TipoAlimento("Refresco", "Bebidas frías", 140))
    #lista_tipos.append(TipoAlimento("Agua con gas", "Bebidas frías", 0))
    #lista_tipos.append(TipoAlimento("Smoothie", "Bebidas frías", 150))
    
    # Bebidas calientes
    #lista_tipos.append(TipoAlimento("Café", "Bebidas calientes", 2))
    #lista_tipos.append(TipoAlimento("Té verde", "Bebidas calientes", 2))
    #lista_tipos.append(TipoAlimento("Chocolate caliente", "Bebidas calientes", 193))
    #lista_tipos.append(TipoAlimento("Té de manzanilla", "Bebidas calientes", 1))
    #lista_tipos.append(TipoAlimento("Cappuccino", "Bebidas calientes", 74))
