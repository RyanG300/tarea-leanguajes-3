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
        try:
            match regla.tipo_regla:
                case "preferencia":
                    if regla.categoria == "combinacion":
                        partes = regla.valor.split(',', 1)  # Solo dividir en 2 partes máximo
                        if len(partes) == 2:
                            valor1, valor2 = partes
                            prolog.assertz(f"regla('{regla.nombre}', preferencia(combinacion, ('{valor1.strip()}', '{valor2.strip()}')))")
                        continue
                    if regla.valor_numerico is not None:
                        prolog.assertz(f"regla('{regla.nombre}', preferencia({regla.categoria}, {regla.valor_numerico}))")
                    else:
                        prolog.assertz(f"regla('{regla.nombre}', preferencia({regla.categoria}, '{regla.valor}'))")
                case "preferencia_condicional":
                    prolog.assertz(f"regla('{regla.nombre}', preferencia_condicional({regla.categoria}, '{regla.condicion}', '{regla.valor}'))")
        except Exception as e:
            print(f"⚠️  Error insertando regla {regla.tipo_regla}: {e}")
            continue

def limpiar_hechos_dinamicos():
    list(prolog.query("retractall(carne(_, _, _, _))"))
    list(prolog.query("retractall(carbohidrato(_, _, _))"))
    list(prolog.query("retractall(vegetal(_, _, _))"))
    list(prolog.query("retractall(entrada(_, _, _, _))"))
    list(prolog.query("retractall(postre(_, _, _))"))
    list(prolog.query("retractall(aceptado(_, _))"))
    list(prolog.query("retractall(rechazado(_, _))"))
    list(prolog.query("retractall(regla(_, _))"))

def realizar_carga():
    limpiar_hechos_dinamicos()
    data = fetch_data_from_sqlite('dataBase/menu_inteligente_base.db')
    insert_alimento_into_prolog(data)
    gustos_usuario = fetch_gustos_from_sqlite('dataBase/menu_inteligente_base.db','gustos_usuario')
    insert_gustos_into_prolog(gustos_usuario)
    gustos_no_usuario = fetch_gustos_from_sqlite('dataBase/menu_inteligente_base.db','disgustos_usuario')
    insert_gustos_into_prolog(gustos_no_usuario)
    reglas = fetch_reglas_from_sqlite('dataBase/menu_inteligente_base.db')
    insert_reglas_into_prolog(reglas)

def guardar_reglas_en_bd(usuario):
    """
    Extrae las reglas generadas por inducir_preferencias de Prolog
    y las guarda en la base de datos SQLite
    """
    conexion = sqlite3.connect('dataBase/menu_inteligente_base.db')
    cursor = conexion.cursor()
    
    try:
        # Primero eliminar reglas existentes del usuario
        cursor.execute('DELETE FROM regla_usuarios WHERE nombre = ?', (usuario,))
        
        # Consultar todas las reglas del usuario en Prolog
        reglas_prolog = list(prolog.query(f"regla('{usuario}', Regla)"))
        
        for regla_data in reglas_prolog:
            regla = regla_data['Regla']
            
            # Parsear diferentes tipos de reglas
            if regla.startswith('preferencia('):
                tipo_regla = 'preferencia'
                contenido = regla[12:-1]  # Remover 'preferencia(' y ')'
                categoria, valor = parse_preferencia(contenido)
                
                cursor.execute('''
                    INSERT INTO regla_usuarios (nombre, tipo_regla, categoria, valor, valor_numerico, condicion)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (usuario, tipo_regla, categoria, valor[0] if isinstance(valor, tuple) else valor, 
                      valor if isinstance(valor, (int, float)) else None, None))
                      
            elif regla.startswith('evita('):
                tipo_regla = 'evita'
                ingrediente = regla[6:-1].replace("'", "")
                
                cursor.execute('''
                    INSERT INTO regla_usuarios (nombre, tipo_regla, categoria, valor, valor_numerico, condicion)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (usuario, tipo_regla, 'ingrediente', ingrediente, None, None))
                
            elif regla.startswith('evita_combinacion('):
                tipo_regla = 'evita_combinacion'
                contenido = regla[18:-1]  # Remover 'evita_combinacion(' y ')'
                ing1, ing2 = contenido.split(',')
                valor_combinado = f"{ing1.strip().replace("'", "")},{ing2.strip().replace("'", "")}"
                
                cursor.execute('''
                    INSERT INTO regla_usuarios (nombre, tipo_regla, categoria, valor, valor_numerico, condicion)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (usuario, tipo_regla, 'combinacion', valor_combinado, None, None))
                
            elif regla.startswith('preferencia_condicional('):
                tipo_regla = 'preferencia_condicional'
                contenido = regla[24:-1]  # Remover 'preferencia_condicional(' y ')'
                categoria, condicion, valor = parse_condicional(contenido)
                
                cursor.execute('''
                    INSERT INTO regla_usuarios (nombre, tipo_regla, categoria, valor, valor_numerico, condicion)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (usuario, tipo_regla, categoria, valor.replace("'", ""), None, condicion.replace("'", "")))
        
        conexion.commit()
        print(f"✅ Reglas de {usuario} guardadas en la base de datos")
        
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error guardando reglas: {e}")
    finally:
        conexion.close()

def parse_preferencia(contenido):
    """Helper para parsear preferencias"""
    if ',' in contenido:
        partes = contenido.split(',', 1)
        categoria = partes[0].strip()
        valor_str = partes[1].strip()
        
        # Manejar combinaciones (tuplas)
        if valor_str.startswith('(') and valor_str.endswith(')'):
            tupla_contenido = valor_str[1:-1]
            valores = [v.strip().replace("'", "") for v in tupla_contenido.split(',')]
            return categoria, ','.join(valores)
        
        # Manejar números
        try:
            valor_num = float(valor_str)
            return categoria, valor_num
        except:
            return categoria, valor_str.replace("'", "")
    
    return contenido, None

def parse_condicional(contenido):
    """Helper para parsear reglas condicionales"""
    partes = contenido.split(',', 2)
    if len(partes) == 3:
        return partes[0].strip(), partes[1].strip(), partes[2].strip()
    return contenido, None, None

def guardar_menus_en_bd(usuario):
    """
    Extrae los menús aceptados y rechazados de Prolog
    y los guarda en las tablas menu e ingredientes_Menu
    """
    import traceback
    
    conexion = sqlite3.connect('dataBase/menu_inteligente_base.db')
    cursor = conexion.cursor()
    
    try:
        # Primero eliminar menús existentes del usuario
        cursor.execute('DELETE FROM menu WHERE nombre = ?', (usuario,))
        
        # Obtener menús aceptados
        menus_aceptados = list(prolog.query(f"aceptado('{usuario}', Menu)"))
        
        for menu_data in menus_aceptados:
            insertar_menu_completo(cursor, usuario, menu_data['Menu'], True)
        
        # Obtener menús rechazados
        menus_rechazados = list(prolog.query(f"rechazado('{usuario}', Menu)"))
        
        for menu_data in menus_rechazados:
            insertar_menu_completo(cursor, usuario, menu_data['Menu'], False)
        
        conexion.commit()
        print(f"✅ {len(menus_aceptados)} menús aceptados y {len(menus_rechazados)} rechazados de {usuario} guardados en la base de datos")
        
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error guardando menús: {e}")
        traceback.print_exc()
    finally:
        conexion.close()

def insertar_menu_completo(cursor, usuario, menu_prolog, aceptado):
    """
    Inserta un menú completo en las tablas menu e ingredientes_Menu
    """
    import traceback
    
    try:
        # Parsear el objeto menu de Prolog
        menu_str = str(menu_prolog)
        
        # Extraer componentes del menú
        # Formato: menu('entrada', 'carbohidrato', 'carne', 'vegetal', 'postre', calorias)
        if menu_str.startswith('menu('):
            # Remover 'menu(' del inicio y ')' del final
            contenido = menu_str[5:-1]
            
            # Dividir por comas, pero cuidando las comillas
            componentes = parsear_componentes_menu(contenido)
            
            if len(componentes) >= 6:
                entrada = limpiar_comillas(componentes[0])
                carbohidrato = limpiar_comillas(componentes[1])
                carne = limpiar_comillas(componentes[2])
                vegetal = limpiar_comillas(componentes[3])
                postre = limpiar_comillas(componentes[4])
                calorias = float(componentes[5].strip())
                
                # Insertar en tabla menu
                cursor.execute('''
                    INSERT INTO menu (nombre, aceptado)
                    VALUES (?, ?)
                ''', (usuario, aceptado))
                
                menu_id = cursor.lastrowid
                
                # Insertar ingredientes en ingredientes_Menu
                ingredientes = []
                if entrada != 'none' and entrada:
                    id_alimento = obtener_id_alimento(cursor, entrada)
                    if id_alimento:
                        ingredientes.append((menu_id, id_alimento))
                if carbohidrato != 'none' and carbohidrato:
                    id_alimento = obtener_id_alimento(cursor, carbohidrato)
                    if id_alimento:
                        ingredientes.append((menu_id, id_alimento))
                if carne != 'none' and carne:
                    id_alimento = obtener_id_alimento(cursor, carne)
                    if id_alimento:
                        ingredientes.append((menu_id, id_alimento))
                if vegetal != 'none' and vegetal:
                    id_alimento = obtener_id_alimento(cursor, vegetal)
                    if id_alimento:
                        ingredientes.append((menu_id, id_alimento))
                if postre != 'none' and postre:
                    id_alimento = obtener_id_alimento(cursor, postre)
                    if id_alimento:
                        ingredientes.append((menu_id, id_alimento))
                
                for ingrediente in ingredientes:
                    cursor.execute('''
                        INSERT INTO ingredientes_Menu (idMenu, idAlimento)
                        VALUES (?, ?)
                    ''', ingrediente)
                
    except Exception as e:
        print(f"❌ Error insertando menú: {e}")
        traceback.print_exc()
        raise

def parsear_componentes_menu(contenido):
    """
    Parsea los componentes de un menú manejando comillas correctamente
    """
    componentes = []
    componente_actual = ""
    dentro_comillas = False
    
    for char in contenido:
        if char == "'" and not dentro_comillas:
            dentro_comillas = True
            componente_actual += char
        elif char == "'" and dentro_comillas:
            dentro_comillas = False
            componente_actual += char
        elif char == "," and not dentro_comillas:
            componentes.append(componente_actual.strip())
            componente_actual = ""
        else:
            componente_actual += char
    
    # Agregar el último componente
    if componente_actual.strip():
        componentes.append(componente_actual.strip())
    
    return componentes

def limpiar_comillas(texto):
    """
    Remueve comillas del inicio y final del texto
    """
    texto = texto.strip()
    if texto.startswith("'") and texto.endswith("'"):
        return texto[1:-1]
    return texto

def obtener_id_alimento(cursor, nombre_alimento):
    """
    Obtiene el ID de un alimento por su nombre
    """
    try:
        cursor.execute('SELECT idAlimento FROM alimentos WHERE nombre = ?', (nombre_alimento,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except Exception as e:
        return None

def guardar_todo_aprendizaje_en_bd(usuario):
    """
    Guarda tanto las reglas como los menús del usuario en la base de datos
    """
    try:
        print(f"💾 Guardando aprendizaje completo de {usuario}...")
        
        # Guardar reglas de preferencias
        guardar_reglas_en_bd(usuario)
        
        # Guardar menús aceptados y rechazados
        guardar_menus_en_bd(usuario)
        
        print(f"✅ Aprendizaje completo de {usuario} guardado exitosamente")
        
    except Exception as e:
        print(f"❌ Error guardando aprendizaje: {e}")

if __name__ == "__main__":
    realizar_carga()