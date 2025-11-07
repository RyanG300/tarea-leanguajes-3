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

class gusto:
    def __init__(self, nombre, ingredientes, total_calorias, gusto):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.total_calorias = total_calorias
        self.gusto = gusto

class regla:
    def __init__(self, nombre, tipo_regla, categoria, valor, valor_numerico, condicion):
        self.nombre = nombre
        self.tipo_regla = tipo_regla
        self.categoria = categoria
        self.valor = valor
        self.valor_numerico = valor_numerico
        self.condicion = condicion

def insert_alimento_into_prolog(data):
    if(not data):
        return
    for alimento in data:
        match alimento.tipo:
            case "carbohidrato":
                prolog.assertz(f"carbohidrato('{alimento.nombre}', {alimento.calorias}, '{alimento.imagen}')")
            case "carne":
                prolog.assertz(f"carne('{alimento.nombre}', {alimento.calorias}, {alimento.tipoDetalle}, '{alimento.imagen}')")
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

def fetch_gustos_from_sqlite(db_path,vista):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT usuario,ingredientes_ordenados,calorias_total FROM "+vista)
    rows = cursor.fetchall()
    gustos = []
    for row in rows:
        nombre, ingredientes, total_calorias = row
        gustos.append(gusto(nombre, ingredientes, total_calorias, True if vista=="gustos_usuario" else False))
    conn.close()
    return gustos

def insert_gustos_into_prolog(data):
    if(not data):
        return
    for gusto in data:
        try:
            entrada, carbohidrato, carne, vegetal, postre = gusto.ingredientes.split(',')
        except ValueError:
            entrada, carbohidrato, carne, vegetal = gusto.ingredientes.split(',')
            postre = "none"
        if(gusto.gusto):
            prolog.assertz(f"aceptado('{gusto.nombre}', menu('{entrada}', '{carbohidrato}', '{carne}', '{vegetal}', '{postre}', {gusto.total_calorias}))")
        else:
            prolog.assertz(f"rechazado('{gusto.nombre}', menu('{entrada}', '{carbohidrato}', '{carne}', '{vegetal}', '{postre}', {gusto.total_calorias}))")

def fetch_reglas_from_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, tipo_regla, categoria, valor, valor_numerico, condicion FROM regla_usuarios")
    rows = cursor.fetchall()
    reglas = []
    for row in rows:
        nombre, tipo_regla, categoria, valor, valor_numerico, condicion = row
        reglas.append(regla(nombre, tipo_regla, categoria, valor, valor_numerico, condicion))
    conn.close()
    return reglas

def insert_reglas_into_prolog(data):
    if(not data):
        return
    for regla in data:
        match regla.tipo_regla:
            case "preferencia":
                if regla.categoria == "combinacion":
                    valor1, valor2 = regla.valor.split(',')
                    prolog.assertz(f"regla('{regla.nombre}', preferencia(combinacion, ('{valor1}', '{valor2}')))")
                    continue
                if regla.valor_numerico is not None:
                    prolog.assertz(f"regla('{regla.nombre}', preferencia({regla.categoria}, {regla.valor_numerico}))")
                else:
                    prolog.assertz(f"regla('{regla.nombre}', preferencia({regla.categoria}, '{regla.valor}'))")
            case "preferencia_condicional":
                prolog.assertz(f"regla('{regla.nombre}', preferencia_condicional({regla.categoria}, '{regla.condicion}', '{regla.valor}'))")

def limpiar_hechos_dinamicos():
    list(prolog.query("retractall(carne(_, _, _, _))"))
    list(prolog.query("retractall(carbohidrato(_, _, _))"))
    list(prolog.query("retractall(vegetal(_, _, _))"))
    list(prolog.query("retractall(entrada(_, _, _, _))"))
    list(prolog.query("retractall(postre(_, _, _))"))
    list(prolog.query("retractall(aceptado(_, _))"))
    list(prolog.query("retractall(rechazado(_, _))"))
    list(prolog.query("retractall(regla(_, _))"))

if __name__ == "__main__":
    limpiar_hechos_dinamicos()
    data = fetch_data_from_sqlite('dataBase/menu_inteligente_base.db')
    insert_alimento_into_prolog(data)
    gustos_usuario = fetch_gustos_from_sqlite('dataBase/menu_inteligente_base.db','gustos_usuario')
    insert_gustos_into_prolog(gustos_usuario)
    gustos_no_usuario = fetch_gustos_from_sqlite('dataBase/menu_inteligente_base.db','disgustos_usuario')
    insert_gustos_into_prolog(gustos_no_usuario)
    reglas = fetch_reglas_from_sqlite('dataBase/menu_inteligente_base.db')
    insert_reglas_into_prolog(reglas)
    #for gusto in prolog.query("aceptado(Usuario, Menu)"):
    #    print(gusto)
    for result in prolog.query("carne(Name, Calories, Type, Image)"):
        print(result)
    #for result in prolog.query("regla(Name, Rule)"):
    #    print(result)
