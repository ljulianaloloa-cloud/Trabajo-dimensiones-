
import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "datacaos_estrella.db"


def actualizar_dimension(nombre_tabla, ruta_csv, clave, columnas):
    """
    Aplica una actualización SCD Tipo 1:
    - Si la clave existe, actualiza sus columnas.
    - Si la clave no existe, inserta el registro.
    """
    ruta_csv = BASE_DIR / ruta_csv
    datos = pd.read_csv(ruta_csv)

    columnas_esperadas = [clave] + columnas
    faltantes = [col for col in columnas_esperadas if col not in datos.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el CSV: {faltantes}")

    datos = datos[columnas_esperadas].drop_duplicates(subset=[clave])
    datos = datos.where(pd.notna(datos), None)

    with sqlite3.connect(DB_PATH) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")

        actualizados = 0
        insertados = 0

        for registro in datos.to_dict(orient="records"):
            existe = conexion.execute(
                f"SELECT 1 FROM {nombre_tabla} WHERE {clave} = ?",
                (registro[clave],)
            ).fetchone()

            if existe:
                asignaciones = ", ".join(
                    f"{columna} = ?" for columna in columnas
                )
                valores = [registro[columna] for columna in columnas]
                valores.append(registro[clave])

                conexion.execute(
                    f"UPDATE {nombre_tabla} SET {asignaciones} "
                    f"WHERE {clave} = ?",
                    valores
                )
                actualizados += 1
            else:
                nombres = ", ".join(columnas_esperadas)
                marcadores = ", ".join("?" for _ in columnas_esperadas)
                valores = [registro[columna] for columna in columnas_esperadas]

                conexion.execute(
                    f"INSERT INTO {nombre_tabla} ({nombres}) "
                    f"VALUES ({marcadores})",
                    valores
                )
                insertados += 1

        conexion.commit()

    print(f"Tabla: {nombre_tabla}")
    print(f"Registros actualizados: {actualizados}")
    print(f"Registros insertados: {insertados}")
    print(f"Total procesado: {actualizados + insertados}")


if __name__ == "__main__":
    actualizar_dimension(
        nombre_tabla="DimTienda",
        ruta_csv="data/tiendas_actualizaciones.csv",
        clave="TiendaID",
        columnas=['NombreTienda', 'Ciudad', 'Region', 'FechaApertura']
    )
