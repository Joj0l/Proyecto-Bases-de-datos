import mysql.connector
from CTkMessagebox import CTkMessagebox


def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost", user="root", password="", database="Biblioteca"
        )

        return conexion

    except mysql.connector.Error as error:
        CTkMessagebox.showerror(
            "Base de datos", f"No se pudo conectar con la base de datos.\n\n{error}"
        )

        return None
