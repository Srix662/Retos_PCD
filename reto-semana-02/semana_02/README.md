# Reto Semana 2: Clasificador de Temperaturas 

Este programa procesa un reporte diario de temperaturas de diversas ciudades alrededor del mundo. Unifica todas las temperaturas a grados Celsius, las clasifica según su clima y genera un reporte limpio en formato CSV.

## Requisitos
- Python 3.x
- No requiere librerías externas (utiliza `sys` de la biblioteca estándar).

## Instrucciones de Uso

El programa lee los datos de entrada a través de la entrada estándar (`stdin`) y arroja el resultado en la salida estándar (`stdout`).

### 1. Preparar datos de entrada
Crea un archivo de texto llamado `entrada.txt` con el siguiente formato:
```csv
ciudad,temperatura,unidad
CDMX,22,C
Nueva York,50,F
Miami,95,F
Cancun,30,C
Chicago,14,F
Phoenix,104,F
Error,abc,C
Lima,25,C
Bangkok,36,C

### 2. Salida Esperada: 
ciudad,temperatura_celsius,clasificacion
CDMX,22.0,Templado
Nueva York,10.0,Frio
Moscu,-10.0,Congelante
Miami,35.0,Calido
Cancun,30.0,Calido
Chicago,-10.0,Congelante
Phoenix,40.0,Extremo
Lima,25.0,Templado
Bangkok,36.0,Extremo

### Instrucciones para correrlo: 
python main.py < test/entrada.txt