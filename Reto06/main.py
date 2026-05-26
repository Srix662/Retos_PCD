import sys
import re

# Departamentos válidos para empleados
DEPARTAMENTOS_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']

# Series válidas para facturas
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']

# ── Patrones FLEXIBLES para detección de tipo ─────────────────────────────
# Aceptan mayúsculas Y minúsculas para determinar la "forma" del código.
# Se usan PRIMERO para clasificar; si no hay match → desconocido.
PATRON_TIPO_PRODUCTO = re.compile(r'^[A-Za-z]{3}-\d{4}-[A-Za-z]{2}$')
PATRON_TIPO_ENVIO    = re.compile(r'^ENV-\d{4}-\d{2}-\d{2}-\d{6}$')
PATRON_TIPO_EMPLEADO = re.compile(r'^EMP-[A-Za-z]{3}-\d{4}$')
PATRON_TIPO_FACTURA  = re.compile(r'^FAC-[A-Za-z]-\d{6}$')

# ── Patrones ESTRICTOS para validación ────────────────────────────────────
# Se usan DESPUÉS de detectar el tipo; aplican reglas de mayúsculas/rangos.
PATRON_PRODUCTO_VALIDO = re.compile(r'^([A-Z]{3})-(\d{4})-([A-Z]{2})$')
PATRON_ENVIO_VALIDO    = re.compile(r'^ENV-(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])-(\d{6})$')
PATRON_EMPLEADO_VALIDO = re.compile(r'^EMP-([A-Z]{3})-([1-9]\d{3})$')
PATRON_FACTURA_VALIDO  = re.compile(r'^FAC-([A-E])-(\d{6})$')


def detectar_tipo(codigo: str) -> str:
    """Detecta el tipo por estructura flexible (mayúsculas O minúsculas).
    El orden importa: ENV/EMP/FAC se verifican antes que producto para evitar
    que un código como 'ENV-...' sea clasificado erróneamente como producto.
    """
    if PATRON_TIPO_ENVIO.match(codigo):
        return "envio"
    if PATRON_TIPO_EMPLEADO.match(codigo):
        return "empleado"
    if PATRON_TIPO_FACTURA.match(codigo):
        return "factura"
    if PATRON_TIPO_PRODUCTO.match(codigo):
        return "producto"
    return "desconocido"


def validar_producto(codigo: str) -> bool:
    """Valida que categoría (3 letras) y país (2 letras) sean MAYÚSCULAS.
    Patron estricto: ^([A-Z]{3})-(digit x4)-([A-Z]{2})$
    """
    return bool(PATRON_PRODUCTO_VALIDO.match(codigo))


def validar_envio(codigo: str) -> bool:
    """Valida año 2020-2030, mes 01-12, día 01-31.
    El regex cubre el formato; el rango del año se verifica en Python.
    Patron: ^ENV-(year)-(01-12)-(01-31)-(6digits)$
    """
    m = PATRON_ENVIO_VALIDO.match(codigo)
    if not m:
        return False
    anio = int(m.group(1))
    return 2020 <= anio <= 2030


def validar_empleado(codigo: str) -> bool:
    """Valida departamento en lista válida y número que no empiece con 0.
    Patron estricto: ^EMP-([A-Z]{3})-([1-9]digit{3})$
    """
    m = PATRON_EMPLEADO_VALIDO.match(codigo)
    if not m:
        return False
    return m.group(1) in DEPARTAMENTOS_VALIDOS


def validar_factura(codigo: str) -> bool:
    """Valida serie A-E en mayúscula y número de 6 dígitos.
    Patron estricto: ^FAC-([A-E])-(6digits)$
    """
    return bool(PATRON_FACTURA_VALIDO.match(codigo))


def validar_codigo(codigo: str) -> tuple:
    """Detecta el tipo con patrones flexibles y valida con reglas estrictas.
    Retorna (tipo, es_valido).
    """
    tipo = detectar_tipo(codigo)

    if tipo == "producto":
        return tipo, validar_producto(codigo)
    elif tipo == "envio":
        return tipo, validar_envio(codigo)
    elif tipo == "empleado":
        return tipo, validar_empleado(codigo)
    elif tipo == "factura":
        return tipo, validar_factura(codigo)
    else:
        return "desconocido", False


def main():
    print("codigo,tipo,valido")
    for linea in sys.stdin:
        codigo = linea.strip()
        if not codigo:           # ignorar líneas vacías
            continue
        tipo, es_valido = validar_codigo(codigo)
        print(f"{codigo},{tipo},{'VALIDO' if es_valido else 'INVALIDO'}")


if __name__ == "__main__":
    main()