import sys

def fahrenheit_a_celsius(f):
    """Convierte Fahrenheit a Celsius."""
    return (f - 32) * 5 / 9

def clasificar_temperatura(celsius):
    """Clasifica la temperatura en Celsius según los rangos establecidos."""
    if celsius < 0:
        return "Congelante"
    elif celsius <= 15:
        return "Frio"
    elif celsius <= 25:
        return "Templado"
    elif celsius <= 35:
        return "Calido"
    else:
        return "Extremo"

def main():
    print("ciudad,temperatura_celsius,clasificacion")
    primera_linea = True
    for linea in sys.stdin:
        linea = linea.strip()
        
        if not linea:
            continue
            
        if primera_linea:
            primera_linea = False
            continue
            
        partes = linea.split(',')
        
        if len(partes) != 3:
            continue
            
        ciudad = partes[0].strip()
        temp_str = partes[1].strip()
        unidad = partes[2].strip().upper() 
        
        if unidad not in ['C', 'F']:
            continue
            
        try:
            temperatura = float(temp_str)
        except ValueError:
            continue
            
        if unidad == 'F':
            celsius = fahrenheit_a_celsius(temperatura)
        else:
            celsius = temperatura
            
        clasificacion = clasificar_temperatura(celsius)
        
        print(f"{ciudad},{celsius:.1f},{clasificacion}")

if __name__ == "__main__":
    main()