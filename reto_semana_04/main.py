
"""
Sistema de Inventario Modular
Genera reporte de productos que necesitan reorden.
"""

from models.producto import Producto
from utils.validators import validar_producto
from utils.io import leer_inventario, escribir_reporte

# Configuracion
ARCHIVO_INVENTARIO = "data/inventario.csv"
ARCHIVO_REPORTE = "outputs/reporte_inventario.csv"


def crear_productos(datos_raw):
    """
    Convierte lista de diccionarios en objetos Producto.
    Ignora registros invalidos mostrando una advertencia.

    Args:
        datos_raw: Lista de diccionarios con datos crudos del CSV

    Returns:
        list: Lista de objetos Producto validos
    """
    productos = []

    for datos in datos_raw:
        es_valido, error = validar_producto(
            datos.get('sku'),
            datos.get('nombre'),
            datos.get('categoria'),
            datos.get('precio'),
            datos.get('stock'),
            datos.get('stock_minimo')
        )

        if not es_valido:
            print(f"Advertencia: Ignorando registro invalido [{datos.get('sku', '???')}] - {error}")
            continue

        producto = Producto(
            sku=datos['sku'],
            nombre=datos['nombre'],
            categoria=datos['categoria'],
            precio=float(datos['precio']),
            stock=int(datos['stock']),
            stock_minimo=int(datos['stock_minimo'])
        )
        productos.append(producto)

    return productos


def filtrar_necesitan_reorden(productos):
    """
    Filtra los productos cuyo stock esta por debajo del minimo.

    Args:
        productos: Lista de objetos Producto

    Returns:
        list: Solo los productos que necesitan reorden
    """
    return [p for p in productos if p.necesita_reorden()]


def ordenar_por_faltantes(productos):
    """
    Ordena productos por unidades faltantes de mayor a menor.

    Args:
        productos: Lista de objetos Producto

    Returns:
        list: Lista ordenada descendentemente por unidades_faltantes
    """
    return sorted(productos, key=lambda p: p.unidades_faltantes(), reverse=True)


def main():
    print("=" * 55)
    print("  SISTEMA DE INVENTARIO - Reporte de Reorden")
    print("=" * 55)

    # 1. Leer datos del CSV
    print(f"\nLeyendo inventario de: {ARCHIVO_INVENTARIO}")
    datos_raw = leer_inventario(ARCHIVO_INVENTARIO)
    print(f"Registros leidos: {len(datos_raw)}")

    # 2. Convertir a objetos Producto (con validacion)
    print()
    productos = crear_productos(datos_raw)
    print(f"\nProductos validos: {len(productos)}")

    # 3. Filtrar los que necesitan reorden
    necesitan_reorden = filtrar_necesitan_reorden(productos)
    print(f"Productos que necesitan reorden: {len(necesitan_reorden)}")

    # 4. Ordenar por urgencia (mas faltantes primero)
    necesitan_reorden = ordenar_por_faltantes(necesitan_reorden)

    # 5. Mostrar resumen en pantalla
    print("\n" + "-" * 55)
    print("PRODUCTOS QUE NECESITAN REORDEN:")
    print("-" * 55)
    for p in necesitan_reorden:
        print(p)

    # 6. Escribir reporte CSV
    escribir_reporte(necesitan_reorden, ARCHIVO_REPORTE)
    print(f"\nReporte guardado en: {ARCHIVO_REPORTE}")

    print("\n" + "=" * 55)
    print("  Proceso completado exitosamente")
    print("=" * 55)


if __name__ == "__main__":
    main()