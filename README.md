# Pipeline de actualización de dimensiones - Esquema estrella

## Objetivo
Actualizar las dimensiones `DimCliente`, `DimTienda` y `DimProducto` de una base de datos SQLite.

La solución usa SCD Tipo 1:
- Si la clave primaria ya existe, se actualizan sus atributos.
- Si la clave primaria no existe, se inserta un registro nuevo.
- No se elimina información.
- No se conserva historial de cambios.

## Estructura

```text
pipeline_dimensiones_estrella/
├── actualizar_clientes.py
├── actualizar_tiendas.py
├── actualizar_productos.py
├── datacaos_estrella.db
└── data/
    ├── clientes_actualizaciones.csv
    ├── tiendas_actualizaciones.csv
    └── productos_actualizaciones.csv
```

## Instalación

```bash
pip install pandas
```

Python ya incluye `sqlite3` y `pathlib`.

## Ejecución

Desde la carpeta del proyecto:

```bash
python actualizar_clientes.py
python actualizar_tiendas.py
python actualizar_productos.py
```

## Conceptos para explicar en clase

1. `Path(__file__).resolve().parent`: encuentra la carpeta donde está el script.
2. `pd.read_csv()`: lee el archivo CSV.
3. `drop_duplicates()`: evita procesar dos veces la misma clave dentro del archivo.
4. `sqlite3.connect()`: abre la conexión con SQLite.
5. `SELECT 1 ... WHERE clave = ?`: verifica si el registro existe.
6. `UPDATE`: modifica un registro existente.
7. `INSERT`: agrega un registro nuevo.
8. `commit()`: confirma los cambios.
9. SCD Tipo 1: reemplaza el valor anterior y no conserva historial.

## Nota
Los archivos CSV de la carpeta `data` son ejemplos de actualización:
- Cliente `CLI0001`: cambia el segmento a `Premium`.
- Tienda `T01`: cambia la región.
- Producto `PRD001`: cambia el precio listado.
- También se agrega un registro nuevo en cada dimensión.
