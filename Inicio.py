import customtkinter as ctk
import os
from PIL import Image
from tkinter import messagebox

from Basededatos import conectar


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")


class Inicio(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color="#ffffff")

        self.usuario = usuario

        self.crear_interfaz()

    def crear_interfaz(self):

        # ENCABEZADO
        ctk.CTkLabel(
            self,
            text="Bienvenido a Biblioteca don Epifanio",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#202c3c",
        ).pack(anchor="w", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Explora nuestra colección de libros.",
            font=ctk.CTkFont(size=14),
            text_color="#6b7280",
        ).pack(anchor="w", padx=20, pady=(0, 25))

        # TÍTULO DE SECCIÓN
        ctk.CTkLabel(
            self,
            text="📚 Libros recomendados",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#1f2937",
        ).pack(anchor="w", padx=20, pady=10)

        # CONTENEDOR CON SCROLL
        libros_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", orientation="vertical"
        )

        libros_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # CONTENEDOR DE TARJETAS
        tarjetas_frame = ctk.CTkFrame(libros_frame, fg_color="transparent")

        tarjetas_frame.pack(fill="x", expand=True)

        # CONFIGURAR 4 COLUMNAS
        for columna in range(4):
            tarjetas_frame.grid_columnconfigure(columna, weight=1)

        # CONEXIÓN A MYSQL
        conexion = conectar()

        if conexion is None:
            ctk.CTkLabel(
                libros_frame,
                text="No se pudo conectar con la base de datos.",
                text_color="red",
            ).pack(pady=20)
            return

        cursor = None

        try:
            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT
                    L.ID_Libro,
                    L.Titulo,
                    L.Autor,
                    L.ISBN,
                    C.NCategoria

                FROM Libro L

                INNER JOIN CAT_Libro CL
                    ON L.ID_Libro = CL.ID_Libro

                INNER JOIN Categoria C
                    ON CL.ID_Categoria = C.ID_Categoria

                WHERE L.Disponibilidad = 1

                ORDER BY RAND()
                LIMIT 30
            """

            cursor.execute(consulta)
            libros = cursor.fetchall()

            if not libros:
                ctk.CTkLabel(
                    libros_frame,
                    text="No hay libros disponibles.",
                    font=ctk.CTkFont(size=16),
                ).pack(pady=30)
                return

            # RECORRER LIBROS
            for indice, libro in enumerate(libros):
                fila = indice // 4
                columna = indice % 4

                # TARJETA
                tarjeta = ctk.CTkFrame(
                    tarjetas_frame,
                    fg_color="#f3f4f6",
                    corner_radius=12,
                    width=180,
                    height=330,
                )

                tarjeta.grid(row=fila, column=columna, padx=10, pady=15, sticky="n")

                tarjeta.grid_propagate(False)

                # IMAGEN
                isbn = libro.get("ISBN")
                ruta_imagen = None

                if isbn:
                    nombre_imagen = f"{isbn}.png"
                    ruta_imagen = os.path.join(BASE_DIR, nombre_imagen)

                if ruta_imagen and os.path.isfile(ruta_imagen):
                    imagen = Image.open(ruta_imagen)
                    imagen = imagen.resize((130, 170))

                    imagen_ctk = ctk.CTkImage(
                        light_image=imagen, dark_image=imagen, size=(130, 170)
                    )

                    lbl_imagen = ctk.CTkLabel(tarjeta, text="", image=imagen_ctk)

                    lbl_imagen.image = imagen_ctk
                    lbl_imagen.pack(pady=(15, 8))

                else:
                    ctk.CTkLabel(
                        tarjeta,
                        text="📚\nSin imagen",
                        width=130,
                        height=170,
                        fg_color="#d1d5db",
                        text_color="#4b5563",
                        corner_radius=8,
                        font=ctk.CTkFont(size=14, weight="bold"),
                    ).pack(pady=(15, 8))

                # TÍTULO
                ctk.CTkLabel(
                    tarjeta,
                    text=libro["Titulo"],
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#1f2937",
                    wraplength=150,
                ).pack(pady=3)

                # AUTOR
                ctk.CTkLabel(
                    tarjeta,
                    text=f"Autor: {libro['Autor']}",
                    font=ctk.CTkFont(size=12),
                    text_color="#6b7280",
                ).pack(pady=3)

                # CATEGORÍA
                ctk.CTkLabel(
                    tarjeta,
                    text=libro["NCategoria"],
                    font=ctk.CTkFont(size=12),
                    text_color="#2563eb",
                ).pack(pady=3)

                # BOTÓN VER MÁS
                ctk.CTkButton(
                    tarjeta,
                    text="Ver más",
                    width=130,
                    height=32,
                    fg_color="#2563eb",
                    hover_color="#1d4ed8",
                    command=lambda l=libro: self.ver_detalles_libro(l),
                ).pack(pady=8)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los libros:\n{e}")

        finally:
            if cursor:
                cursor.close()

            conexion.close()

    def ver_detalles_libro(self, libro):
        # Aquí podrás implementar posteriormente
        # la ventana con los detalles del libro.
        pass
