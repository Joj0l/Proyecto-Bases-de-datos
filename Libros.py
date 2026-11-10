import customtkinter as ctk
import os
from PIL import Image
from tkinter import messagebox
from Basededatos import conectar


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagenes")


class Libros(ctk.CTkFrame):
    def __init__(self, master, usuario=None):
        super().__init__(master, fg_color="#ffffff")

        self.usuario = usuario
        self.libros = []
        self.categorias = []
        self.tarjetas = []
        self.libro_seleccionado = None

        self.crear_interfaz()

    # ==========================================
    # INTERFAZ PRINCIPAL
    # ==========================================

    def crear_interfaz(self):

        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            encabezado,
            text="📚 Gestión de libros",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#202c3c",
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Consulta, administra y organiza el catálogo de libros.",
            font=ctk.CTkFont(size=14),
            text_color="#6b7280",
        ).pack(anchor="w", pady=3)

        # ESTADÍSTICAS

        self.estadisticas_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.estadisticas_frame.pack(fill="x", padx=15, pady=10)

        self.crear_estadisticas()

        # BARRA DE HERRAMIENTAS

        herramientas = ctk.CTkFrame(self, fg_color="transparent")
        herramientas.pack(fill="x", padx=20, pady=10)

        self.buscador = ctk.CTkEntry(
            herramientas,
            placeholder_text="Buscar por título, autor, ISBN o categoría...",
            height=40,
        )
        self.buscador.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.buscador.bind("<KeyRelease>", lambda event: self.filtrar_libros())

        self.filtro_categoria = ctk.CTkComboBox(
            herramientas,
            values=["Todas"],
            width=160,
            height=40,
            command=lambda valor: self.filtrar_libros(),
        )
        self.filtro_categoria.set("Todas")
        self.filtro_categoria.pack(side="left", padx=5)

        self.filtro_estado = ctk.CTkComboBox(
            herramientas,
            values=["Todos", "Disponible", "Prestado"],
            width=145,
            height=40,
            command=lambda valor: self.filtrar_libros(),
        )
        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="left", padx=5)

        ctk.CTkButton(
            herramientas,
            text="↻",
            width=45,
            height=40,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.cargar_libros,
        ).pack(side="left", padx=5)

        # BOTONES DE ACCIONES

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(
            acciones,
            text="➕ Registrar libro",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.registrar_libro,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            acciones,
            text="✏ Editar seleccionado",
            fg_color="#0d9488",
            hover_color="#0f766e",
            command=self.editar_seleccionado,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            acciones,
            text="🗑 Eliminar",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.eliminar_seleccionado,
        ).pack(side="left", padx=5)

        # CATÁLOGO

        self.catalogo = ctk.CTkScrollableFrame(
            self, fg_color="#f3f4f6", corner_radius=10
        )
        self.catalogo.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tarjetas_frame = ctk.CTkFrame(self.catalogo, fg_color="transparent")
        self.tarjetas_frame.pack(fill="x", expand=True)

        for columna in range(4):
            self.tarjetas_frame.grid_columnconfigure(columna, weight=1)

        self.cargar_categorias()
        self.cargar_libros()

    # ==========================================
    # ESTADÍSTICAS
    # ==========================================

    def crear_estadisticas(self):

        for widget in self.estadisticas_frame.winfo_children():
            widget.destroy()

        total = len(self.libros)

        disponibles = sum(libro["Disponibilidad"] == 1 for libro in self.libros)

        prestados = total - disponibles

        datos = [
            ("📚 Total de libros", total, "#2563eb"),
            ("🟢 Disponibles", disponibles, "#16a34a"),
            ("🔴 Prestados", prestados, "#dc2626"),
        ]

        for titulo, valor, color in datos:
            tarjeta = ctk.CTkFrame(
                self.estadisticas_frame,
                fg_color="#f9fafb",
                corner_radius=10,
                border_width=1,
                border_color="#e5e7eb",
            )

            tarjeta.pack(side="left", fill="both", expand=True, padx=5)

            ctk.CTkLabel(
                tarjeta, text=titulo, text_color="#4b5563", font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=15, pady=(10, 3))

            ctk.CTkLabel(
                tarjeta,
                text=str(valor),
                text_color=color,
                font=ctk.CTkFont(size=24, weight="bold"),
            ).pack(anchor="w", padx=15, pady=(0, 10))

    # ==========================================
    # CARGAR CATEGORÍAS
    # ==========================================

    def cargar_categorias(self):

        conexion = conectar()

        if conexion is None:
            return

        cursor = None

        try:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT ID_Categoria, NCategoria
                FROM Categoria
                ORDER BY NCategoria
            """)

            self.categorias = cursor.fetchall()

            nombres = ["Todas"] + [
                categoria["NCategoria"] for categoria in self.categorias
            ]

            self.filtro_categoria.configure(values=nombres)

            self.filtro_categoria.set("Todas")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las categorías:\n{e}")

        finally:
            if cursor:
                cursor.close()

            conexion.close()

    # ==========================================
    # CARGAR LIBROS DESDE MYSQL
    # ==========================================

    def cargar_libros(self):

        conexion = conectar()

        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar con la base de datos.")
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
                    L.Disponibilidad,

                    GROUP_CONCAT(
                        C.NCategoria
                        SEPARATOR ', '
                    ) AS NCategoria

                FROM Libro L

                LEFT JOIN CAT_Libro CL
                    ON L.ID_Libro = CL.ID_Libro

                LEFT JOIN Categoria C
                    ON CL.ID_Categoria = C.ID_Categoria

                GROUP BY
                    L.ID_Libro,
                    L.Titulo,
                    L.Autor,
                    L.ISBN,
                    L.Disponibilidad

                ORDER BY L.Titulo
            """

            cursor.execute(consulta)

            self.libros = cursor.fetchall()

            self.actualizar_catalogo()

            self.crear_estadisticas()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los libros:\n{e}")

        finally:
            if cursor:
                cursor.close()

            conexion.close()
            # ==========================================

    # CARGAR PORTADA
    # ==========================================

    def cargar_portada(self, isbn, tarjeta):

        ruta_imagen = None

        if isbn:
            ruta_imagen = os.path.join(BASE_DIR, f"{isbn}.png")

        if ruta_imagen and os.path.isfile(ruta_imagen):
            imagen = Image.open(ruta_imagen)

            imagen_ctk = ctk.CTkImage(
                light_image=imagen, dark_image=imagen, size=(130, 170)
            )

            etiqueta = ctk.CTkLabel(tarjeta, text="", image=imagen_ctk)

            etiqueta.image = imagen_ctk
            etiqueta.pack(pady=(15, 8))

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

    # ==========================================
    # ACTUALIZAR CATÁLOGO
    # ==========================================

    def actualizar_catalogo(self):

        for widget in self.tarjetas_frame.winfo_children():
            widget.destroy()

        self.tarjetas = []

        for indice, libro in enumerate(self.libros):
            fila = indice // 4
            columna = indice % 4

            tarjeta = ctk.CTkFrame(
                self.tarjetas_frame,
                fg_color="#ffffff",
                corner_radius=12,
                width=190,
                height=350,
                border_width=1,
                border_color="#e5e7eb",
            )

            tarjeta.grid(row=fila, column=columna, padx=10, pady=10, sticky="n")

            tarjeta.grid_propagate(False)

            # PORTADA

            self.cargar_portada(libro.get("ISBN"), tarjeta)

            # TÍTULO

            ctk.CTkLabel(
                tarjeta,
                text=libro["Titulo"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#1f2937",
                wraplength=160,
            ).pack(pady=3)

            # AUTOR

            ctk.CTkLabel(
                tarjeta,
                text=f"Autor: {libro['Autor']}",
                font=ctk.CTkFont(size=12),
                text_color="#6b7280",
                wraplength=160,
            ).pack(pady=3)

            # CATEGORÍA

            ctk.CTkLabel(
                tarjeta,
                text=libro.get("NCategoria") or "Sin categoría",
                font=ctk.CTkFont(size=12),
                text_color="#2563eb",
                wraplength=160,
            ).pack(pady=3)

            # DISPONIBILIDAD

            disponible = libro["Disponibilidad"] == 1

            ctk.CTkLabel(
                tarjeta,
                text=("● Disponible" if disponible else "● Prestado"),
                text_color=("#16a34a" if disponible else "#dc2626"),
                font=ctk.CTkFont(size=12, weight="bold"),
            ).pack(pady=3)

            # BOTÓN DETALLES

            ctk.CTkButton(
                tarjeta,
                text="Ver detalles",
                width=140,
                height=32,
                fg_color="#2563eb",
                hover_color="#1d4ed8",
                command=lambda l=libro: self.ver_detalles_libro(l),
            ).pack(pady=8)

            # SELECCIONAR LIBRO

            tarjeta.bind("<Button-1>", lambda event, l=libro: self.seleccionar_libro(l))

            self.tarjetas.append((tarjeta, libro))

        self.filtrar_libros()

    # ==========================================
    # BUSCADOR Y FILTROS
    # ==========================================

    def filtrar_libros(self):

        texto = self.buscador.get().lower().strip()

        categoria = self.filtro_categoria.get()
        estado = self.filtro_estado.get()

        for tarjeta, libro in self.tarjetas:
            coincide_texto = (
                texto in str(libro["Titulo"]).lower()
                or texto in str(libro["Autor"]).lower()
                or texto in str(libro.get("ISBN") or "").lower()
                or texto in str(libro.get("NCategoria") or "").lower()
            )

            coincide_categoria = categoria == "Todas" or categoria in str(
                libro.get("NCategoria") or ""
            )

            disponible = libro["Disponibilidad"] == 1

            coincide_estado = (
                estado == "Todos"
                or (estado == "Disponible" and disponible)
                or (estado == "Prestado" and not disponible)
            )

            if coincide_texto and coincide_categoria and coincide_estado:
                tarjeta.grid()

            else:
                tarjeta.grid_remove()

    # ==========================================
    # SELECCIONAR LIBRO
    # ==========================================

    def seleccionar_libro(self, libro):

        self.libro_seleccionado = libro

        for tarjeta, datos in self.tarjetas:
            tarjeta.configure(
                border_color=(
                    "#2563eb" if datos["ID_Libro"] == libro["ID_Libro"] else "#e5e7eb"
                )
            )

    # ==========================================
    # VER DETALLES DEL LIBRO
    # ==========================================

    def ver_detalles_libro(self, libro):

        ventana = ctk.CTkToplevel(self)

        ventana.title("Detalles del libro")
        ventana.geometry("750x550")
        ventana.minsize(650, 480)

        ventana.configure(fg_color="#ffffff")

        ventana.transient(self.winfo_toplevel())

        ventana.grab_set()

        # ENCABEZADO

        ctk.CTkLabel(
            ventana,
            text="Información del libro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#202c3c",
        ).pack(anchor="w", padx=25, pady=(20, 5))

        ctk.CTkLabel(
            ventana, text=f"ID del libro: {libro['ID_Libro']}", text_color="#6b7280"
        ).pack(anchor="w", padx=25)

        # CONTENEDOR PRINCIPAL

        contenido = ctk.CTkFrame(ventana, fg_color="#f3f4f6", corner_radius=12)
        contenido.pack(fill="both", expand=True, padx=25, pady=20)

        # PORTADA

        portada_frame = ctk.CTkFrame(contenido, fg_color="transparent", width=220)
        portada_frame.pack(side="left", fill="y", padx=20, pady=20)

        isbn = libro.get("ISBN")

        ruta_imagen = os.path.join(BASE_DIR, f"{isbn}.png") if isbn else None

        if ruta_imagen and os.path.isfile(ruta_imagen):
            imagen = Image.open(ruta_imagen)

            imagen_ctk = ctk.CTkImage(
                light_image=imagen, dark_image=imagen, size=(180, 250)
            )

            lbl_imagen = ctk.CTkLabel(portada_frame, text="", image=imagen_ctk)

            lbl_imagen.image = imagen_ctk
            lbl_imagen.pack(pady=10)

        else:
            ctk.CTkLabel(
                portada_frame,
                text="📚\nSin portada",
                width=180,
                height=250,
                fg_color="#d1d5db",
                corner_radius=10,
                text_color="#4b5563",
                font=ctk.CTkFont(size=18, weight="bold"),
            ).pack(pady=10)

        # INFORMACIÓN

        informacion = ctk.CTkFrame(contenido, fg_color="transparent")
        informacion.pack(side="left", fill="both", expand=True, padx=10, pady=20)

        def agregar_dato(titulo, valor, color="#374151"):

            ctk.CTkLabel(
                informacion,
                text=titulo,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#6b7280",
            ).pack(anchor="w", pady=(10, 2))

            ctk.CTkLabel(
                informacion,
                text=str(valor or "No especificado"),
                font=ctk.CTkFont(size=15),
                text_color=color,
                wraplength=350,
                justify="left",
            ).pack(anchor="w")

        agregar_dato("Título", libro["Titulo"], "#1f2937")

        agregar_dato("Autor", libro["Autor"])

        agregar_dato("ISBN", libro.get("ISBN"))

        agregar_dato("Categoría", libro.get("NCategoria") or "Sin categoría")

        disponible = libro["Disponibilidad"] == 1

        agregar_dato(
            "Disponibilidad",
            "Disponible" if disponible else "Prestado",
            "#16a34a" if disponible else "#dc2626",
        )

        # BOTÓN CERRAR

        ctk.CTkButton(
            ventana,
            text="Cerrar",
            width=130,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=ventana.destroy,
        ).pack(pady=(0, 15))

        return ventana

    # ==========================================
    # REGISTRAR LIBRO
    # ==========================================

    def registrar_libro(self):

        self.abrir_formulario_libro()

    # ==========================================
    # EDITAR LIBRO SELECCIONADO
    # ==========================================

    def editar_seleccionado(self):

        if not self.libro_seleccionado:
            messagebox.showwarning(
                "Seleccionar libro", "Primero selecciona un libro del catálogo."
            )
            return

        self.abrir_formulario_libro(self.libro_seleccionado)

    # ==========================================
    # FORMULARIO DE LIBROS
    # ==========================================

    def abrir_formulario_libro(self, libro=None):

        editar = libro is not None

        ventana = ctk.CTkToplevel(self)

        ventana.title("Editar libro" if editar else "Registrar libro")

        ventana.geometry("500x650")
        ventana.resizable(False, False)

        ventana.configure(fg_color="#ffffff")

        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text=("✏ Editar libro" if editar else "➕ Registrar nuevo libro"),
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color="#202c3c",
        ).pack(anchor="w", padx=25, pady=(25, 5))

        ctk.CTkLabel(
            ventana,
            text="Completa la información correspondiente.",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280",
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # FORMULARIO

        formulario = ctk.CTkScrollableFrame(
            ventana, fg_color="#f3f4f6", corner_radius=10
        )
        formulario.pack(fill="both", expand=True, padx=20, pady=10)

        entradas = {}

        campos = [
            ("Titulo", "Título del libro"),
            ("Autor", "Nombre del autor"),
            ("ISBN", "ISBN del libro"),
        ]

        for clave, placeholder in campos:
            ctk.CTkLabel(
                formulario,
                text=placeholder,
                text_color="#374151",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(anchor="w", padx=15, pady=(12, 4))

            entrada = ctk.CTkEntry(formulario, placeholder_text=placeholder, height=40)

            entrada.pack(fill="x", padx=15)

            entradas[clave] = entrada

            if editar:
                entrada.insert(0, str(libro.get(clave) or ""))

        # CATEGORÍA

        ctk.CTkLabel(
            formulario,
            text="Categoría",
            text_color="#374151",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(15, 4))

        nombres_categorias = [categoria["NCategoria"] for categoria in self.categorias]

        combo_categoria = ctk.CTkComboBox(
            formulario, values=nombres_categorias, height=40
        )

        combo_categoria.pack(fill="x", padx=15)

        if editar:
            categorias_actuales = (libro.get("NCategoria") or "").split(", ")

            if categorias_actuales:
                combo_categoria.set(categorias_actuales[0])

        elif nombres_categorias:
            combo_categoria.set(nombres_categorias[0])

        # DISPONIBILIDAD

        ctk.CTkLabel(
            formulario,
            text="Disponibilidad",
            text_color="#374151",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(15, 4))

        combo_estado = ctk.CTkComboBox(
            formulario, values=["Disponible", "Prestado"], height=40
        )

        combo_estado.pack(fill="x", padx=15)

        if editar:
            combo_estado.set(
                "Disponible" if libro["Disponibilidad"] == 1 else "Prestado"
            )

        else:
            combo_estado.set("Disponible")

        # MENSAJE

        mensaje = ctk.CTkLabel(formulario, text="", text_color="#dc2626")

        mensaje.pack(anchor="w", padx=15, pady=10)

        # ======================================
        # GUARDAR INFORMACIÓN
        # ======================================

        def guardar():

            titulo = entradas["Titulo"].get().strip()
            autor = entradas["Autor"].get().strip()
            isbn = entradas["ISBN"].get().strip()

            categoria_nombre = combo_categoria.get()

            estado = combo_estado.get()

            if not titulo or not autor or not isbn:
                mensaje.configure(
                    text="Completa todos los campos obligatorios.", text_color="#dc2626"
                )
                return

            if not self.categorias:
                mensaje.configure(
                    text="No hay categorías registradas.", text_color="#dc2626"
                )
                return

            categoria_seleccionada = next(
                (c for c in self.categorias if c["NCategoria"] == categoria_nombre),
                None,
            )

            if not categoria_seleccionada:
                mensaje.configure(
                    text="Selecciona una categoría válida.", text_color="#dc2626"
                )
                return

            disponibilidad = 1 if estado == "Disponible" else 0

            conexion = conectar()

            if conexion is None:
                mensaje.configure(
                    text="No se pudo conectar con la base de datos.",
                    text_color="#dc2626",
                )
                return

            cursor = None

            try:
                cursor = conexion.cursor()

                # COMPROBAR ISBN DUPLICADO

                if editar:
                    cursor.execute(
                        """
                        SELECT ID_Libro
                        FROM Libro
                        WHERE ISBN = %s
                        AND ID_Libro != %s
                        """,
                        (isbn, libro["ID_Libro"]),
                    )

                else:
                    cursor.execute(
                        """
                        SELECT ID_Libro
                        FROM Libro
                        WHERE ISBN = %s
                        """,
                        (isbn,),
                    )

                if cursor.fetchone():
                    mensaje.configure(
                        text="Ya existe un libro con ese ISBN.", text_color="#dc2626"
                    )
                    return

                # ACTUALIZAR LIBRO

                if editar:
                    cursor.execute(
                        """
                        UPDATE Libro

                        SET
                            Titulo = %s,
                            Autor = %s,
                            ISBN = %s,
                            Disponibilidad = %s

                        WHERE ID_Libro = %s
                        """,
                        (titulo, autor, isbn, disponibilidad, libro["ID_Libro"]),
                    )

                    id_libro = libro["ID_Libro"]

                    # ACTUALIZAR CATEGORÍA

                    cursor.execute(
                        """
                        DELETE FROM CAT_Libro
                        WHERE ID_Libro = %s
                        """,
                        (id_libro,),
                    )

                # INSERTAR LIBRO

                else:
                    cursor.execute(
                        """
                        INSERT INTO Libro (
                            Titulo,
                            Autor,
                            ISBN,
                            Disponibilidad
                        )

                        VALUES (%s, %s, %s, %s)
                        """,
                        (titulo, autor, isbn, disponibilidad),
                    )

                    id_libro = cursor.lastrowid

                # ASIGNAR CATEGORÍA

                cursor.execute(
                    """
                    INSERT INTO CAT_Libro (
                        ID_Libro,
                        ID_Categoria
                    )

                    VALUES (%s, %s)
                    """,
                    (id_libro, categoria_seleccionada["ID_Categoria"]),
                )

                conexion.commit()

                messagebox.showinfo(
                    "Operación exitosa",
                    (
                        "Libro actualizado correctamente."
                        if editar
                        else "Libro registrado correctamente."
                    ),
                    parent=ventana,
                )

                ventana.destroy()

                self.libro_seleccionado = None

                self.cargar_libros()

            except Exception as e:
                conexion.rollback()

                mensaje.configure(text=f"Error al guardar: {e}", text_color="#dc2626")

            finally:
                if cursor:
                    cursor.close()

                conexion.close()

        # BOTONES

        botones = ctk.CTkFrame(ventana, fg_color="transparent")

        botones.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(
            botones,
            text="💾 Guardar",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=guardar,
        ).pack(side="left", expand=True, fill="x", padx=5)

        ctk.CTkButton(
            botones,
            text="Cancelar",
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=ventana.destroy,
        ).pack(side="left", expand=True, fill="x", padx=5)

    # ==========================================
    # ELIMINAR LIBRO
    # ==========================================

    def eliminar_seleccionado(self):

        if not self.libro_seleccionado:
            messagebox.showwarning(
                "Seleccionar libro", "Primero selecciona un libro del catálogo."
            )
            return

        libro = self.libro_seleccionado

        confirmar = messagebox.askyesno(
            "Eliminar libro",
            (
                f"¿Estás seguro de eliminar el libro?\n\n"
                f"{libro['Titulo']}\n\n"
                "Esta acción no se puede deshacer."
            ),
        )

        if not confirmar:
            return

        conexion = conectar()

        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar con la base de datos.")
            return

        cursor = None

        try:
            cursor = conexion.cursor()

            # ELIMINAR RELACIONES CON CATEGORÍAS

            cursor.execute(
                """
                DELETE FROM CAT_Libro
                WHERE ID_Libro = %s
                """,
                (libro["ID_Libro"],),
            )

            # ELIMINAR LIBRO

            cursor.execute(
                """
                DELETE FROM Libro
                WHERE ID_Libro = %s
                """,
                (libro["ID_Libro"],),
            )

            conexion.commit()

            self.libro_seleccionado = None

            messagebox.showinfo(
                "Operación exitosa", "El libro se eliminó correctamente."
            )

            self.cargar_libros()

        except Exception as e:
            conexion.rollback()

            messagebox.showerror("Error", f"No se pudo eliminar el libro:\n{e}")

        finally:
            if cursor:
                cursor.close()

            conexion.close()
