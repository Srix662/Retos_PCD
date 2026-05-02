Sistema de Inventario Modular

Sistema que lee un inventario desde un archivo CSV, detecta productos que necesitan reorden (stock menor al minimo requerido) y genera un reporte ordenado para el departamento de compras.
Estructura del Proyecto
reto_semana_04/
main.py                  # Punto de entrada del sistema
README.md                # Este archivo
.gitignore               # Archivos excluidos de Git
models/
   __init__.py
   producto.py          # Clase Producto con logica de negocio
utils/
   __init__.py
    io.py                # Lectura y escritura de archivos CSV
   validators.py        # Validacion de campos
data/
   inventario.csv       # Archivo de entrada
 outputs/
    reporte_inventario.csv  # Reporte generado

Como Ejecutar
python main.py

Entrada
Archivo: data/inventario.csv
Columna	Tipo	Descripcion
sku	texto	Identificador unico
nombre	texto	Nombre del producto
categoria	texto	Categoria
precio	decimal	Precio unitario
stock	entero	Cantidad actual
stock_minimo	entero	Nivel minimo antes de reordenar

Las lineas con datos invalidos (precio no numerico, stock no numerico, columnas faltantes o extra) son ignoradas automaticamente.
Salida
Archivo: outputs/reporte_inventario.csv
Contiene solo los productos donde stock < stock_minimo, ordenados por unidades_faltantes de mayor a menor.
Columna	Descripcion
sku	SKU del producto
nombre	Nombre
categoria	Categoria
stock_actual	Stock actual
stock_minimo	Stock minimo requerido
unidades_faltantes	stock_minimo - stock_actual
valor_inventario	precio * stock_actual

Autor
Bryan Axel Esparza Davila

Reto Semana 4 - Programacion para Ciencia de Datos - IPN 2026
