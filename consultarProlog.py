from pyswip import Prolog
from insertarEnProlog import *

class query_Menus:
    def __init__(self, usuario, postre, vegetariano, tipo_carne,
                 min_calorias, max_calorias,
                 incluye_ingredientes, evita_ingredientes):
        usuario_atom = usuario.replace(" ", "_") if usuario else 'anon'
        postre_atom = postre if postre in ("si", "no") else postre
        veg_atom = vegetariano if vegetariano in ("si", "no") else vegetariano
        self.crear_reglas_usuario(usuario_atom, evita_ingredientes, incluye_ingredientes)
        incluye_prolog = self.prolog_list_from(incluye_ingredientes)
        evita_prolog = self.prolog_list_from(evita_ingredientes)
        query = (
            f"recomendar({usuario_atom}, {postre_atom}, {veg_atom}, "
            f"{tipo_carne}, {min_calorias}, {max_calorias}, "
            f"{incluye_prolog}, {evita_prolog}, 10, Menus)"
        )
        self.menus = list(prolog.query(query))
        for resultado in self.menus:
            print(resultado)  # Depuración inicial
        
    def crear_reglas_usuario(self, usuario_atom, evita_ingredientes, incluye_ingredientes):

        # Guardar ingredientes que el usuario desea evitar como reglas directas
        for ingrediente in evita_ingredientes:
            safe = ingrediente.replace("'", "''")  # escapa comillas
            prolog.assertz(f"regla({usuario_atom}, evita('{safe}'))")

        # Guardar ingredientes que el usuario desea incluir como reglas directas
        for ingrediente in incluye_ingredientes:
            safe = ingrediente.replace("'", "''")
            prolog.assertz(f"regla({usuario_atom}, preferencia(incluye, '{safe}'))")


    def prolog_quote_atom(self, s: str) -> str:
        # Escapar comillas simples duplicándolas para Prolog: e.g. don' -> don''
        safe = str(s).replace("'", "''")
        return f"'{safe}'"


    def prolog_list_from(self, pylist: list) -> str:
        if not pylist:
            return '[]'
        return '[' + ','.join(self.prolog_quote_atom(s) for s in pylist) + ']'


    def parse_menu_item(self, menu_item):
        """Parsea un elemento devuelto por Prolog y devuelve una lista [E,C,X,Y,P,Cal]
        o None si la estructura es inesperada."""
        # Caso: ya es lista/tupla de 6
        if isinstance(menu_item, (list, tuple)) and len(menu_item) == 6:
            return [str(x) for x in menu_item]
        # Caso: viene como string "menu(... )"
        if isinstance(menu_item, str) and menu_item.startswith("menu(") and menu_item.endswith(")"):
            inner = menu_item[len("menu("):-1]
            parts = [p.strip() for p in inner.split(", ", 5)]
            if len(parts) == 6:
                return parts
        return None
    
    def guardar_datos_usuario_en_prolog(self, usuario, menu_elegido):
        parsed = self.parse_menu_item(menu_elegido)
        e, c, x, y, p, cal = parsed      
        usuario_atom = usuario.replace(" ", "_") if usuario else 'anon'
        # Preparar átomos Prolog con comillas para cadenas; calorías como número
        e_a = self.prolog_quote_atom(e)
        c_a = self.prolog_quote_atom(c)
        x_a = self.prolog_quote_atom(x)
        y_a = self.prolog_quote_atom(y)
        p_a = self.prolog_quote_atom(p)
        try:
            cal_val = int(str(cal).strip())
        except Exception:
            cal_val = str(cal).strip()
        menu_term = f"menu({e_a},{c_a},{x_a},{y_a},{p_a},{cal_val})"
        prolog.assertz(f"aceptado({usuario_atom}, {menu_term})")
        list(prolog.query(f"inducir_preferencias({usuario_atom})"))
        list(prolog.query("guardar_datos"))