# 1. Crear el archivo de prueba (como se indica en la última captura)
datos_csv = """fecha,producto,cantidad,precio_unitario
2023-01-01,Laptop,2,1500.00
2023-01-02,Mouse,10,25.50
2023-01-03,Laptop,1,1499.90
2023-01-04,Teclado,5,85.00
2023-01-05,Mouse,5,25.50"""

# 0. Aqui lo busque de internet por que no tenia ni la menor idea de como hacerlo. Aun no lo hemos visto
with open('ventas.csv', 'w') as f:
    f.write(datos_csv)

# 2. Función principal para procesar las ventas
def procesar_ventas(ruta_archivo):
    productos = {} 

    try:
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            
        # Ignoramos la primera línea si es el encabezado
        inicio = 1 if 'fecha' in lineas[0].lower() else 0
        
        for linea in lineas[inicio:]:
            linea = linea.strip()
            
            # Regla 5: Ignorar líneas inválidas o vacías
            if not linea:
                continue 
                
            partes = linea.split(',')
            if len(partes) != 4:
                continue
                
            fecha, producto, cantidad_str, precio_str = partes
            
            try:
                cantidad = int(cantidad_str)
                precio = float(precio_str)
            except ValueError:
                continue
                
            ingreso = cantidad * precio
            
            # Regla 1: Agrupar por producto
            if producto not in productos:
                productos[producto] = {
                    "unidades": 0,
                    "ingreso": 0.0
                }
            
            productos[producto]["unidades"] += cantidad
            productos[producto]["ingreso"] += ingreso
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return

    # Regla 2: Calcular el Precio Promedio
    for prod, datos in productos.items():
        if datos["unidades"] > 0:
            datos["precio_promedio"] = datos["ingreso"] / datos["unidades"]
        else:
            datos["precio_promedio"] = 0.0
        
    # Regla 3: Ordenar por Ingreso Total
    productos_ordenados = sorted(productos.items(), key=lambda x: x[1]["ingreso"], reverse=True)
    
    # Regla 4 y Especificación de Salida: Imprimir resultados con formato
    print("producto,unidades_vendidas,ingreso_total,precio_promedio")
    for prod, datos in productos_ordenados:
        unidades = datos["unidades"]
        ingreso_total = f"{datos['ingreso']:.2f}"
        precio_promedio = f"{datos['precio_promedio']:.2f}"
        print(f"{prod},{unidades},{ingreso_total},{precio_promedio}")

# 3. Ejecutar el procesador
procesar_ventas('entrada_prueba.txt')