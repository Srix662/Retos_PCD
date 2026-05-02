# Perfilador de Datasets

Herramienta que analiza archivos CSV y genera reportes de calidad de datos.

## Requisitos

- Python 3.8 o superior

## Instalacion

### 1. Clonar el repositorio
```bash
git clone https://github.com/usuario/reto-semana-05.git
cd reto-semana-05
```

### 2. Crear ambiente virtual
```bash
python -m venv .venv
```

### 3. Activar ambiente virtual
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py --input <archivo_entrada.csv> --output <archivo_salida.csv>
```

### Ejemplos
```bash
python main.py --input data/ventas.csv    --output outputs/perfil_ventas.csv
python main.py --input data/empleados.csv --output outputs/perfil_empleados.csv
python main.py --input data/sensores.csv  --output outputs/perfil_sensores.csv
```

## Formato de Salida

El perfil generado contiene una fila por columna del CSV original:

| Columna             | Descripcion                                      |
|---------------------|--------------------------------------------------|
| `nombre_columna`    | Nombre de la columna analizada                   |
| `tipo_inferido`     | Tipo detectado: numerico / texto / fecha / booleano |
| `total_registros`   | Total de filas (sin encabezado)                  |
| `valores_nulos`     | Cantidad de valores vacios                       |
| `porcentaje_nulos`  | Porcentaje de nulos (2 decimales)                |
| `valores_unicos`    | Cantidad de valores distintos (sin nulos)        |
| `porcentaje_unicos` | Porcentaje de unicidad (2 decimales)             |
| `ejemplo_valor`     | Primer valor no nulo encontrado                  |

## Reglas de Procesamiento

- **Nulo**: celda vacia, solo espacios o `None`. No son nulos: `0`, `"0"`, `"null"`, `"None"`.
- **Tipo inferido**: se clasifica si >80% de valores no nulos cumplen el criterio.
- **Valores unicos**: case-sensitive, excluye nulos.

## Autor

Bryan Axel Esparza Davila- Febrero 2026

---
*Reto Semana 5 - Programacion para Ciencia de Datos - IPN 2026*