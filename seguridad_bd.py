import sqlite3
from pathlib import Path
from datetime import datetime

CARPETA = Path(__file__).resolve().parent
RUTA_BD = CARPETA / "laboratorio.db"


def verificar_y_respaldar():
    if not RUTA_BD.is_file():
        print("No se encontró laboratorio.db.")
        print("Ejecuta primero crear_bd.py.")
        return

    origen = sqlite3.connect(
        RUTA_BD.as_uri() + "?mode=ro",
        uri=True,
    )

    try:
        print("TPE 4 - GRUPO 5")
        print("SEGURIDAD DE LA BASE DE DATOS")
        print()

        resultados = origen.execute(
            "PRAGMA integrity_check"
        ).fetchall()

        if resultados != [("ok",)]:
            print("Se detectaron problemas de integridad:")

            for fila in resultados:
                print(f"  {fila[0]}")

            return

        print("Comprobación de integridad: OK")
        print("Conexión a la base original: solo lectura")

        carpeta_respaldos = CARPETA / "respaldos"
        carpeta_respaldos.mkdir(exist_ok=True)

        fecha = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        ruta_respaldo = (
            carpeta_respaldos / f"laboratorio_{fecha}.db"
        )

        destino = sqlite3.connect(ruta_respaldo)

        try:
            origen.backup(destino)

            verificacion = destino.execute(
                "PRAGMA integrity_check"
            ).fetchall()

            if verificacion != [("ok",)]:
                print("El respaldo no superó la verificación.")
                return

        finally:
            destino.close()

        print("Copia de respaldo creada y verificada.")
        print(f"Archivo: {ruta_respaldo}")
        print()
        print("Proceso finalizado.")

    finally:
        origen.close()


if __name__ == "__main__":
    verificar_y_respaldar()