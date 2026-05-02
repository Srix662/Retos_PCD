#!/usr/bin/env python3
"""
Perfilador de Datasets CSV
Analiza cualquier archivo CSV y genera un reporte de calidad de datos.

Uso:
    python main.py --input <archivo.csv> --output <perfil.csv>
"""

import argparse
import csv
import sys


# ─────────────────────────────────────────────
# Regla 1: Deteccion de Valores Nulos
# ─────────────────────────────────────────────

def es_valor_nulo(valor):
    """
    Determina si un valor se considera nulo.

    Nulo:    None, string vacio, string con solo espacios
    NO nulo: 0, "0", "null", "None", cualquier otro texto
    """
    if valor is None:
        return True
    if isinstance(valor, str) and valor.strip() == "":
        return True
    return False


# ─────────────────────────────────────────────
# Regla 2: Inferencia de Tipo de Dato
# ─────────────────────────────────────────────

def es_numerico(valor):
    """Verifica si un valor es numerico."""
    try:
        float(str(valor).replace(',', '').strip())
        return True
    except (ValueError, TypeError):
        return False


def es_fecha(valor):
    """Verifica si un valor parece una fecha YYYY-MM-DD."""
    v = str(valor).strip()
    if len(v) >= 10 and v[4] == '-' and v[7] == '-':
        try:
            partes = v[:10].split('-')
            anio, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
            return 1900 <= anio <= 2100 and 1 <= mes <= 12 and 1 <= dia <= 31
        except (ValueError, IndexError):
            pass
    return False


def es_booleano(valor):
    """Verifica si un valor es booleano."""
    v = str(valor).strip().lower()
    return v in ['true', 'false', 'yes', 'no', 'si', '1', '0', 't', 'f']


def inferir_tipo(valores):
    """
    Infiere el tipo de una columna basado en sus valores no nulos.

    Returns:
        str: 'numerico', 'fecha', 'booleano', o 'texto'
    """
    valores_validos = [v for v in valores if not es_valor_nulo(v)]

    if not valores_validos:
        return "texto"  # Si todo es nulo, asumimos texto

    total  = len(valores_validos)
    umbral = 0.8  # 80% para determinar el tipo

    # Contar cada tipo (fechas primero para evitar falsos numericos)
    num_fechas    = sum(1 for v in valores_validos if es_fecha(v))
    num_booleanos = sum(1 for v in valores_validos if es_booleano(v))
    num_numericos = sum(1 for v in valores_validos if es_numerico(v))

    # Determinar tipo predominante
    if num_fechas / total >= umbral:
        return "fecha"
    elif num_booleanos / total >= umbral:
        return "booleano"
    elif num_numericos / total >= umbral:
        return "numerico"
    else:
        return "texto"


# ─────────────────────────────────────────────
# Regla 3: Valores Unicos (excluye nulos, case-sensitive)
# Regla 4: Porcentajes con 2 decimales
# ─────────────────────────────────────────────

def calcular_porcentaje(parte, total):
    """Calcula porcentaje con 2 decimales."""
    if total == 0:
        return 0.00
    return round((parte / total) * 100, 2)


# ─────────────────────────────────────────────
# Perfilado
# ─────────────────────────────────────────────

def perfilar_columna(nombre, valores):
    """
    Genera el perfil completo de una columna.

    Args:
        nombre: Nombre de la columna
        valores: Lista de valores de la columna

    Returns:
        dict: Perfil de la columna con todas las metricas
    """
    total            = len(valores)
    nulos            = sum(1 for v in valores if es_valor_nulo(v))
    valores_no_nulos = [v for v in valores if not es_valor_nulo(v)]
    unicos           = len(set(valores_no_nulos))   # case-sensitive
    ejemplo          = valores_no_nulos[0] if valores_no_nulos else ""
    tipo             = inferir_tipo(valores)

    return {
        "nombre_columna"   : nombre,
        "tipo_inferido"    : tipo,
        "total_registros"  : total,
        "valores_nulos"    : nulos,
        "porcentaje_nulos" : calcular_porcentaje(nulos, total),
        "valores_unicos"   : unicos,
        "porcentaje_unicos": calcular_porcentaje(unicos, total),
        "ejemplo_valor"    : ejemplo,
    }


# ─────────────────────────────────────────────
# I/O  — usa el modulo csv para manejar correctamente:
#   - campos con comas internas  ("Garcia, Ana")
#   - comillas dobles            ("campo ""con"" comillas")
#   - strings vacios             ("") detectados como nulos
# ─────────────────────────────────────────────

def leer_csv(ruta):
    """
    Lee un archivo CSV usando el modulo csv de la biblioteca estandar.
    Soporta cualquier CSV valido: campos con comas, comillas dobles, etc.
    """
    with open(ruta, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        filas  = [fila for fila in reader]

    if not filas:
        return [], []

    encabezados = filas[0]
    datos       = filas[1:]

    return encabezados, datos


def escribir_csv(ruta, perfiles):
    """
    Escribe el CSV de perfiles usando el modulo csv estandar.
    Agrega comillas automaticamente si un campo contiene comas.
    """
    columnas = [
        "nombre_columna", "tipo_inferido", "total_registros",
        "valores_nulos", "porcentaje_nulos", "valores_unicos",
        "porcentaje_unicos", "ejemplo_valor"
    ]

    with open(ruta, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columnas)

        for p in perfiles:
            writer.writerow([
                p["nombre_columna"],
                p["tipo_inferido"],
                p["total_registros"],
                p["valores_nulos"],
                f"{p['porcentaje_nulos']:.2f}",
                p["valores_unicos"],
                f"{p['porcentaje_unicos']:.2f}",
                p["ejemplo_valor"],
            ])


# ─────────────────────────────────────────────
# Programa principal
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Perfilador de Datasets CSV"
    )
    parser.add_argument("--input",  "-i", required=True,
                        help="Ruta al CSV de entrada")
    parser.add_argument("--output", "-o", required=True,
                        help="Ruta al CSV de salida")

    args = parser.parse_args()

    print(f"Perfilando: {args.input}")

    # Leer CSV
    try:
        encabezados, filas = leer_csv(args.input)
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {args.input}")
        sys.exit(1)

    if not encabezados:
        print("Error: El archivo esta vacio")
        sys.exit(1)

    print(f"Columnas encontradas: {len(encabezados)}")
    print(f"Registros: {len(filas)}")

    # Perfilar cada columna
    perfiles = []
    for i, nombre_col in enumerate(encabezados):
        valores = [fila[i] if i < len(fila) else "" for fila in filas]
        perfil  = perfilar_columna(nombre_col, valores)
        perfiles.append(perfil)

    # Escribir resultado
    escribir_csv(args.output, perfiles)
    print(f"Perfil guardado en: {args.output}")
    print("Completado!")


if __name__ == "__main__":
    main()