import os
try:
    from pyswip import Prolog
except Exception:
    # pyswip no está disponible: definimos un "shim" que produce un error claro al instanciar
    # para que el IDE/analizador no marque la importación como irresoluble y el usuario reciba
    # instrucciones sobre cómo instalarlo en tiempo de ejecución.
    Prolog = None

    class _PrologShim:
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "Biblioteca 'pyswip' no encontrada; instale pyswip y SWI-Prolog (por ejemplo:\n"
                "    pip install pyswip\n"
                "y asegúrese de que el ejecutable 'swipl' esté en su PATH).\n"
                "Si ya está instalado, verifique el entorno/interprete usado por su editor."
            )

    Prolog = _PrologShim

# =====================================================
#   Sistema de Menús Saludables Inteligente (Python)
# =====================================================

# Conexión con Prolog
prolog = Prolog()
# Construir ruta absoluta a main.pl basada en la ubicación de este archivo
pl_path = os.path.join(os.path.dirname(__file__), "main.pl")
try:
    prolog.consult(pl_path)
except Exception as e:
    # Mostrar error claro y sugerir corrección de ruta
    print(f"ERROR: source_sink '{pl_path}' does not exist or could not be consulted: {e}")
    # Intentar ruta relativa por compatibilidad
    try:
        prolog.consult("main.pl")
    except Exception:
        print("Intente ubicar 'main.pl' en el mismo directorio que 'consulta.py' o ajuste la ruta en el script.")
        raise

print("=========================================")
print("      MENÚ SALUDABLE INTELIGENTE")
print("=========================================\n")

# --------------------------
# Entradas del usuario
# --------------------------
usuario = input("Nombre de usuario: ").strip().lower()
vegetariano = input("¿Desea menú vegetariano? (si/no): ").strip().lower()
postre = input("¿Desea postre? (si/no): ").strip().lower()
tipo_carne = input("Tipo de carne (any/blanca/roja/vegetariana): ").strip().lower()

try:
    min_cal = int(input("Calorías mínimas (ej. 500): "))
    max_cal = int(input("Calorías máximas (ej. 900): "))
except ValueError:
    print("Valores no válidos, se usarán por defecto 0 y 9999.")
    min_cal, max_cal = 0, 9999

incluye = input("Ingredientes que desea incluir (separa por coma o deja vacío): ").strip()
evita = input("Ingredientes que desea evitar (separa por coma o deja vacío): ").strip()

# Conversión a formato de lista para Prolog
def lista_desde_texto(txt):
    if not txt:
        return []
    # Mantener espacios (p.ej. 'tofu al curry') porque en los hechos Prolog
    # los platos están entre comillas y contienen espacios.
    return [t.strip().lower() for t in txt.split(",")]


def prolog_quote_atom(s: str) -> str:
    # Escapar comillas simples duplicándolas para Prolog: e.g. don' -> don''
    safe = str(s).replace("'", "''")
    return f"'{safe}'"


def prolog_list_from(pylist: list) -> str:
    if not pylist:
        return '[]'
    return '[' + ','.join(prolog_quote_atom(s) for s in pylist) + ']'


def parse_menu_item(menu_item):
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

incluye_lista = lista_desde_texto(incluye)
evita_lista = lista_desde_texto(evita)

# Usuario: convertir espacios a guiones bajos para formar un átomo válido
# (Se define aquí porque se usa más abajo al asertar reglas de preferencias/evita)
usuario_atom = usuario.replace(" ", "_") if usuario else 'anon'

for ingrediente in evita_lista:
    safe = ingrediente.replace("'", "''")  # escapa comillas
    prolog.assertz(f"regla({usuario_atom}, evita('{safe}'))")

# Guardar ingredientes que el usuario desea incluir como reglas directas
for ingrediente in incluye_lista:
    safe = ingrediente.replace("'", "''")
    prolog.assertz(f"regla({usuario_atom}, preferencia(incluye, '{safe}'))")

# --------------------------
# Construir y ejecutar consulta Prolog
# --------------------------
# Preparar valores para Prolog
# postre y vegetariano se pasan como átomos 'si'/'no' sin comillas (como en filtros.pl)
postre_atom = postre if postre in ("si", "no") else postre
veg_atom = vegetariano if vegetariano in ("si", "no") else vegetariano
# tipo_carne se pasa tal cual (any/blanca/roja/vegetariana)
tipo_carne_atom = tipo_carne

# Incluye/Evita deben ser listas Prolog con elementos entre comillas simples
incluye_prolog = prolog_list_from(incluye_lista)
evita_prolog = prolog_list_from(evita_lista)

# (usuario_atom ya definido arriba)

query = (
    f"recomendar({usuario_atom}, {postre_atom}, {veg_atom}, "
    f"{tipo_carne_atom}, {min_cal}, {max_cal}, "
    f"{incluye_prolog}, {evita_prolog}, 10, Menus)"
)

# Query preparada (debug removido)

print("\n🔍 Generando menús...")

menus = list(prolog.query(query))

# --------------------------
# Mostrar resultados
# --------------------------
if menus:
    print(f"\nMenús recomendados para '{usuario}':\n")
    contador = 1
    for resultado in menus:
        # Procesar resultado sin prints de depuración

        for menu in resultado["Menus"]:
            parsed = parse_menu_item(menu)
            if not parsed:
                print("⚠️ Estructura inesperada de 'menu' (se ignora):", menu)
                continue

            e, c, x, y, p, cal = parsed
            # Normalizar textos y calorías
            e, c, x, y, p = map(lambda s: str(s).replace("_", " "), [e, c, x, y, p])
            cal = str(cal).strip()
            print(f"{contador}. Entrada: {e}\n   Plato fuerte: {c}, {x}, {y}\n   Postre: {p}\n   Calorías: {cal}\n")
            contador += 1
else:
    print("No se encontraron menús que cumplan los filtros.")

print("=========================================")
print("Fin de la consulta.\n")


if menus:
    try:
        n = int(input("Número del menú que desea aceptar (1–10): "))
        menu_elegido = menus[0]["Menus"][n-1]
        parsed = parse_menu_item(menu_elegido)
        if not parsed:
            raise ValueError("Estructura inesperada del menú elegido; no se pudo registrar.")
        e, c, x, y, p, cal = parsed
        # Preparar átomos Prolog con comillas para cadenas; calorías como número
        e_a = prolog_quote_atom(e)
        c_a = prolog_quote_atom(c)
        x_a = prolog_quote_atom(x)
        y_a = prolog_quote_atom(y)
        p_a = prolog_quote_atom(p)
        try:
            cal_val = int(str(cal).strip())
        except Exception:
            cal_val = str(cal).strip()
        menu_term = f"menu({e_a},{c_a},{x_a},{y_a},{p_a},{cal_val})"
        # Registrar elección automáticamente (usar usuario_atom como átomo)
        prolog.assertz(f"aceptado({usuario_atom}, {menu_term})")
        # En pyswip prolog.query devuelve un generador perezoso; convertir a lista
        # fuerza la ejecución de la consulta y sus efectos (inducir_preferencias/guardar_datos)
        list(prolog.query(f"inducir_preferencias({usuario_atom})"))
        list(prolog.query("guardar_datos"))
        print(f"💾 Menú aceptado registrado y aprendizaje guardado automáticamente para '{usuario}'.")
    except Exception as err:
        print("Error registrando la elección:", err)