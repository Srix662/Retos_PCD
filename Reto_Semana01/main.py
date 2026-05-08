import sys

def limpiar_valor(valor):
    """
    Limpia un valor individual:
    - Quita espacios (Regla 6)
    - Elimina caracteres no válidos (Regla 5)
    - Retorna el número limpio como string
    """
    
    noespacios = valor.strip()
    validos = set("0123456789.-")
    valor_limpio = ""
    for c in noespacios:
        if c in validos:
            valor_limpio += c
    
    return valor_limpio

def truncar_a_entero(valor_limpio):
    """
    Convierte el string limpio a float y luego a int para truncar.
    Maneja excepciones de conversión.
    """
    if not valor_limpio:
        return 0
        
    try:
        return int(float(valor_limpio))
    except ValueError:
        return 0

def procesar_linea(linea):
    """
    Procesa una línea completa:
    - Separa por comas
    - Limpia cada valor
    - Trunca a entero
    - Suma todos
    - Retorna el resultado
    """
    if not linea.strip():
        return 0
    
    valores = linea.split(',')
    suma_total = 0
    for valor in valores:
        valor_limpio = limpiar_valor(valor)
        numero = truncar_a_entero(valor_limpio)
        suma_total += numero
        
    return suma_total

def main():
    """
    Lee de stdin línea por línea
    Procesa cada línea
    Imprime el resultado en stdout
    """
    for linea in sys.stdin:
        resultado = procesar_linea(linea)
        print(resultado)

if __name__ == "__main__":
    main()