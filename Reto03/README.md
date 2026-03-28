# Proyecto: Analizador de Ventas

Este repositorio contiene un script en Python diseñado para automatizar el procesamiento y análisis de un registro de transacciones de ventas en formato CSV. El programa extrae los datos, maneja excepciones de formato, realiza los cálculos correspondientes y genera un reporte estructurado.

## Características Principales

- **Lectura y procesamiento de datos:** El script lee de manera eficiente el archivo `ventas.csv`.
- **Manejo de datos inválidos:** Implementa control de excepciones para identificar e ignorar líneas vacías, incompletas o con tipos de datos incorrectos (por ejemplo, texto en campos numéricos), garantizando la estabilidad de la ejecución.
- **Agrupación y cálculo de métricas:** Consolida la información por producto y calcula con precisión las unidades totales vendidas, el ingreso bruto total y el precio promedio por unidad.
- **Ordenamiento de resultados:** Genera un reporte de salida en la consola, ordenando los productos de forma descendente en función de su ingreso total.

## Instrucciones de Ejecución

Para ejecutar este proyecto, es necesario contar con un entorno de Python 3 instalado en su sistema.

1. Abra la terminal o línea de comandos y navegue hasta el directorio que contiene el proyecto.
2. Ejecute el script principal utilizando el siguiente comando:
   ```bash
   python ventas.py