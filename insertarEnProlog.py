from pyswip import Prolog
import sqlite3

prolog = Prolog()
prolog.consult("prolog_logic/main.pl")

class alimento:
    def __init__(self, nombre, tipo, calorias, tipoDetalle="", imagen=""):
        self.nombre = nombre
        self.tipo = tipo
        self.calorias = calorias
        self.tipoDetalle = tipoDetalle
        self.imagen = imagen


def insert_data_into_prolog(data):
    for alimento in data:
        match alimento.tipo:
            case "carbohidrato":
                prolog.assertz(f"carbohidrato('{alimento.nombre}', {alimento.calorias}, '{alimento.imagen}')")
            case "carne":
                prolog.assertz(f"carne('{alimento.nombre}', {alimento.calorias}, '{alimento.tipoDetalle}', '{alimento.imagen}')")
            case "vegetal":
                prolog.assertz(f"vegetal('{alimento.nombre}', {alimento.calorias}, '{alimento.imagen}')")
            case "postre":
                prolog.assertz(f"postre('{alimento.nombre}', {alimento.calorias}, '{alimento.imagen}')")
            case "entrada":
                prolog.assertz(f"entrada('{alimento.nombre}', {alimento.calorias}, '{alimento.tipoDetalle}', '{alimento.imagen}')")

def fetch_data_from_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, tipo, calorias, tipoDetalle, imagen FROM vista_alimentos_detalle_filas")
    rows = cursor.fetchall()
    alimentos = []
    for row in rows:
        nombre, tipo, calorias, tipoDetalle, imagen = row
        alimentos.append(alimento(nombre, tipo, calorias, tipoDetalle, imagen))
    conn.close()
    return alimentos

if __name__ == "__main__":
    data = fetch_data_from_sqlite('dataBase/menu_inteligente_base.db')
    insert_data_into_prolog(data)
    for result in prolog.query("carbohidrato(Name, Calories, Image)"):
        print(result)
