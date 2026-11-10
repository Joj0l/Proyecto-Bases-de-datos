import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta


class Prestamos(ctk.CTkFrame):
    def __init__(self, parent, usuario=None):
        super().__init__(parent, fg_color="white")

        self.usuario = usuario

        # ==========================================
        # DATOS DE EJEMPLO
        # ==========================================

        self.prestamos = [
            {
                "id": 1,
                "usuario": "Carlos Hernández",
                "matricula": "2024001",
                "libro": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "fecha_prestamo": "2026-11-01",
                "fecha_devolucion": "2026-11-15",
                "estado": "Activo",
            },
            {
                "id": 2,
                "usuario": "María González",
                "matricula": "2024002",
                "libro": "El principito",
                "autor": "Antoine de Saint-Exupéry",
                "fecha_prestamo": "2026-10-20",
                "fecha_devolucion": "2026-11-03",
                "estado": "Vencido",
            },
            {
                "id": 3,
                "usuario": "Luis Ramírez",
                "matricula": "2024003",
                "libro": "Don Quijote de la Mancha",
                "autor": "Miguel de Cervantes",
                "fecha_prestamo": "2026-10-15",
                "fecha_devolucion": "2026-10-29",
                "estado": "Devuelto",
            },
        ]

        self.prestamo_seleccionado = None
        self.campos = {}

        self.crear_interfaz()

    # ==========================================
    # INTERFAZ PRINCIPAL
    # ==========================================

    def crear_interfaz(self):

        principal = ctk.CTkFrame(self, fg_color="transparent")
        principal.pack(fill="both", expand=True, padx=20, pady=20)

        # ENCABEZADO

        encabezado = ctk.CTkFrame(principal, fg_color="transparent")
        encabezado.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            encabezado,
            text="Gestión de préstamos de libros",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#1f2937",
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Administra, registra y consulta los préstamos de la biblioteca.",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280",
        ).pack(anchor="w", pady=3)

        # ESTADÍSTICAS

        self.estadisticas_frame = ctk.CTkFrame(principal, fg_color="transparent")
        self.estadisticas_frame.pack(fill="x", pady=(0, 15))

        self.crear_estadisticas()

        # NAVEGACIÓN

        navegacion = ctk.CTkFrame(
            principal, fg_color="#e5e7eb", height=42, corner_radius=8
        )
        navegacion.pack(fill="x", pady=(0, 10))

        self.contenedor = ctk.CTkFrame(principal, fg_color="white", corner_radius=8)
        self.contenedor.pack(fill="both", expand=True)

        self.frame_directorio = self.crear_directorio()
        self.frame_registro = self.crear_formulario()

        ctk.CTkButton(
            navegacion,
            text="📚 Directorio de préstamos",
            fg_color="transparent",
            text_color="#1f2937",
            hover_color="#d1d5db",
            command=lambda: self.cambiar_pestana(self.frame_directorio),
        ).pack(side="left", padx=3, pady=3)

        ctk.CTkButton(
            navegacion,
            text="➕ Nuevo préstamo",
            fg_color="transparent",
            text_color="#1f2937",
            hover_color="#d1d5db",
            command=self.nuevo_prestamo,
        ).pack(side="left", padx=3, pady=3)

        self.cambiar_pestana(self.frame_directorio)

    # ==========================================
    # ESTADÍSTICAS
    # ==========================================

    def crear_estadisticas(self):

        for widget in self.estadisticas_frame.winfo_children():
            widget.destroy()

        total = len(self.prestamos)

        activos = sum(p["estado"] == "Activo" for p in self.prestamos)

        vencidos = sum(p["estado"] == "Vencido" for p in self.prestamos)

        devueltos = sum(p["estado"] == "Devuelto" for p in self.prestamos)

        datos = [
            ("📚 Total préstamos", total, "#2563eb"),
            ("🟢 Activos", activos, "#16a34a"),
            ("🔴 Vencidos", vencidos, "#dc2626"),
            ("📖 Devueltos", devueltos, "#7c3aed"),
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
                tarjeta,
                text=titulo,
                text_color="#4b5563",
                font=ctk.CTkFont(size=13),
            ).pack(anchor="w", padx=15, pady=(12, 3))

            ctk.CTkLabel(
                tarjeta,
                text=str(valor),
                text_color=color,
                font=ctk.CTkFont(size=25, weight="bold"),
            ).pack(anchor="w", padx=15, pady=(0, 12))

    # ==========================================
    # CAMBIAR PESTAÑAS
    # ==========================================

    def cambiar_pestana(self, frame):

        self.frame_directorio.pack_forget()
        self.frame_registro.pack_forget()

        frame.pack(fill="both", expand=True, padx=15, pady=15)

    # ==========================================
    # DIRECTORIO DE PRÉSTAMOS
    # ==========================================

    def crear_directorio(self):

        widget = ctk.CTkFrame(self.contenedor, fg_color="transparent")

        ctk.CTkLabel(
            widget,
            text="Directorio de préstamos",
            text_color="#1f2937",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", pady=(0, 12))

        # BUSCADOR

        self.buscador = ctk.CTkEntry(
            widget,
            placeholder_text="Buscar por usuario, matrícula, libro o autor...",
            height=38,
        )

        self.buscador.pack(fill="x", pady=(0, 10))

        self.buscador.bind("<KeyRelease>", lambda event: self.actualizar_directorio())

        # FILTROS

        filtros = ctk.CTkFrame(widget, fg_color="transparent")
        filtros.pack(fill="x", pady=(0, 12))

        self.filtro_estado = ctk.CTkComboBox(
            filtros,
            values=["Todos", "Activo", "Vencido", "Devuelto"],
            width=180,
            command=lambda valor: self.actualizar_directorio(),
        )

        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="left")

        ctk.CTkButton(
            filtros,
            text="↻ Actualizar",
            width=110,
            fg_color="#2563eb",
            command=self.actualizar_directorio,
        ).pack(side="right")

        # LISTA CON SCROLL

        self.lista_prestamos = ctk.CTkScrollableFrame(
            widget, fg_color="#f3f4f6", corner_radius=10
        )

        self.lista_prestamos.pack(fill="both", expand=True)

        # BOTONES INFERIORES

        acciones = ctk.CTkFrame(widget, fg_color="transparent")
        acciones.pack(fill="x", pady=10)

        ctk.CTkButton(
            acciones,
            text="✏ Editar seleccionado",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.editar_seleccionado,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            acciones,
            text="↩ Registrar devolución",
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.registrar_devolucion,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            acciones,
            text="🗑 Eliminar préstamo",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            command=self.eliminar_seleccionado,
        ).pack(side="left", padx=5)

        self.actualizar_directorio()

        return widget

    # ==========================================
    # ACTUALIZAR DIRECTORIO
    # ==========================================

    def actualizar_directorio(self):

        for widget in self.lista_prestamos.winfo_children():
            widget.destroy()

        texto = self.buscador.get().lower().strip()

        estado = self.filtro_estado.get()

        resultados = []

        for prestamo in self.prestamos:
            coincide_texto = any(
                texto in prestamo[campo].lower()
                for campo in ["usuario", "matricula", "libro", "autor"]
            )

            coincide_estado = estado == "Todos" or prestamo["estado"] == estado

            if coincide_texto and coincide_estado:
                resultados.append(prestamo)

        self.tarjetas_prestamos = []

        for prestamo in resultados:
            tarjeta = ctk.CTkFrame(
                self.lista_prestamos,
                fg_color="white",
                corner_radius=10,
                border_width=1,
                border_color="#e5e7eb",
            )

            tarjeta.pack(fill="x", padx=8, pady=6)

            contenido = ctk.CTkFrame(tarjeta, fg_color="transparent")
            contenido.pack(fill="x", padx=15, pady=12)

            # ICONO DEL LIBRO

            icono = ctk.CTkFrame(
                contenido, width=55, height=55, fg_color="#dbeafe", corner_radius=10
            )

            icono.pack(side="left", padx=(0, 15))
            icono.pack_propagate(False)

            ctk.CTkLabel(
                icono,
                text="📚",
                font=ctk.CTkFont(size=25),
            ).pack(expand=True)

            # INFORMACIÓN

            info = ctk.CTkFrame(contenido, fg_color="transparent")

            info.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(
                info,
                text=prestamo["libro"],
                text_color="#1f2937",
                font=ctk.CTkFont(size=17, weight="bold"),
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"Autor: {prestamo['autor']}",
                text_color="#4b5563",
            ).pack(anchor="w", pady=2)

            ctk.CTkLabel(
                info,
                text=(
                    f"Usuario: {prestamo['usuario']} | "
                    f"Matrícula: {prestamo['matricula']}"
                ),
                text_color="#6b7280",
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=(
                    f"Préstamo: {prestamo['fecha_prestamo']}   "
                    f"Devolución: {prestamo['fecha_devolucion']}"
                ),
                text_color="#6b7280",
            ).pack(anchor="w", pady=2)

            # ESTADO

            colores = {
                "Activo": "#16a34a",
                "Vencido": "#dc2626",
                "Devuelto": "#7c3aed",
            }

            ctk.CTkLabel(
                contenido,
                text=prestamo["estado"],
                text_color=colores.get(prestamo["estado"], "#6b7280"),
                font=ctk.CTkFont(weight="bold"),
            ).pack(side="right", padx=10)

            # SELECCIÓN

            tarjeta.bind(
                "<Button-1>", lambda event, p=prestamo: self.seleccionar_prestamo(p)
            )

            for hijo in contenido.winfo_children():
                hijo.bind(
                    "<Button-1>", lambda event, p=prestamo: self.seleccionar_prestamo(p)
                )

            for hijo in info.winfo_children():
                hijo.bind(
                    "<Button-1>", lambda event, p=prestamo: self.seleccionar_prestamo(p)
                )

            self.tarjetas_prestamos.append((tarjeta, prestamo))

        if not resultados:
            ctk.CTkLabel(
                self.lista_prestamos,
                text="No se encontraron préstamos.",
                text_color="#6b7280",
                font=ctk.CTkFont(size=14),
            ).pack(pady=30)

        self.crear_estadisticas()

    # ==========================================
    # SELECCIONAR PRÉSTAMO
    # ==========================================

    def seleccionar_prestamo(self, prestamo):

        self.prestamo_seleccionado = prestamo

        for tarjeta, datos in self.tarjetas_prestamos:
            tarjeta.configure(
                border_color=("#2563eb" if datos["id"] == prestamo["id"] else "#e5e7eb")
            )

    # ==========================================
    # FORMULARIO DE PRÉSTAMOS
    # ==========================================

    def crear_formulario(self):

        widget = ctk.CTkFrame(self.contenedor, fg_color="transparent")

        ctk.CTkLabel(
            widget,
            text="Registro de préstamo",
            text_color="#1f2937",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", pady=(0, 15))

        formulario = ctk.CTkScrollableFrame(
            widget, fg_color="#f9fafb", corner_radius=10
        )

        formulario.pack(fill="both", expand=True)

        self.campos = {}

        campos = [
            ("usuario", "Nombre completo del usuario"),
            ("matricula", "Matrícula o número de identificación"),
            ("libro", "Título del libro"),
            ("autor", "Autor del libro"),
            ("fecha_prestamo", "Fecha del préstamo (AAAA-MM-DD)"),
            ("fecha_devolucion", "Fecha límite de devolución (AAAA-MM-DD)"),
        ]

        for clave, placeholder in campos:
            ctk.CTkLabel(formulario, text=placeholder, text_color="#374151").pack(
                anchor="w", padx=15, pady=(12, 3)
            )

            entrada = ctk.CTkEntry(formulario, placeholder_text=placeholder, height=38)

            entrada.pack(fill="x", padx=15)

            self.campos[clave] = entrada

        # ESTADO DEL PRÉSTAMO

        ctk.CTkLabel(formulario, text="Estado del préstamo", text_color="#374151").pack(
            anchor="w", padx=15, pady=(12, 3)
        )

        self.campos["estado"] = ctk.CTkComboBox(
            formulario, values=["Activo", "Vencido", "Devuelto"], height=38
        )

        self.campos["estado"].set("Activo")

        self.campos["estado"].pack(fill="x", padx=15)

        # BOTONES

        botones = ctk.CTkFrame(formulario, fg_color="transparent")

        botones.pack(fill="x", padx=15, pady=20)

        ctk.CTkButton(
            botones,
            text="💾 Guardar préstamo",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.guardar_prestamo,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botones,
            text="Limpiar",
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.limpiar_formulario,
        ).pack(side="left", padx=5)

        return widget

    # ==========================================
    # LIMPIAR FORMULARIO
    # ==========================================

    def limpiar_formulario(self):

        for clave, entrada in self.campos.items():
            if isinstance(entrada, ctk.CTkEntry):
                entrada.delete(0, "end")

            elif clave == "estado":
                entrada.set("Activo")

        self.prestamo_seleccionado = None

    # ==========================================
    # NUEVO PRÉSTAMO
    # ==========================================

    def nuevo_prestamo(self):

        self.limpiar_formulario()

        self.cambiar_pestana(self.frame_registro)

    # ==========================================
    # VALIDAR FECHAS
    # ==========================================

    def validar_fechas(self, fecha_prestamo, fecha_devolucion):

        try:
            inicio = datetime.strptime(fecha_prestamo, "%Y-%m-%d")

            fin = datetime.strptime(fecha_devolucion, "%Y-%m-%d")

            if fin <= inicio:
                messagebox.showwarning(
                    "Fechas inválidas",
                    "La fecha de devolución debe ser posterior a la fecha del préstamo.",
                )

                return False

            return True

        except ValueError:
            messagebox.showwarning(
                "Formato incorrecto", "Las fechas deben tener el formato AAAA-MM-DD."
            )

            return False

    # ==========================================
    # GUARDAR PRÉSTAMO
    # ==========================================

    def guardar_prestamo(self):

        datos = {clave: entrada.get().strip() for clave, entrada in self.campos.items()}

        # VALIDAR CAMPOS

        if any(not valor for valor in datos.values()):
            messagebox.showwarning("Campos obligatorios", "Completa todos los campos.")

            return

        # VALIDAR FECHAS

        if not self.validar_fechas(datos["fecha_prestamo"], datos["fecha_devolucion"]):
            return

        # COMPROBAR DUPLICADOS

        for prestamo in self.prestamos:
            mismo_registro = (
                prestamo["matricula"].lower() == datos["matricula"].lower()
                and prestamo["libro"].lower() == datos["libro"].lower()
                and prestamo["estado"] != "Devuelto"
            )

            es_otro = (
                not self.prestamo_seleccionado
                or prestamo["id"] != self.prestamo_seleccionado["id"]
            )

            if mismo_registro and es_otro:
                messagebox.showwarning(
                    "Préstamo duplicado",
                    "Este usuario ya tiene un préstamo activo de ese libro.",
                )

                return

        # EDITAR PRÉSTAMO

        if self.prestamo_seleccionado:
            for prestamo in self.prestamos:
                if prestamo["id"] == self.prestamo_seleccionado["id"]:
                    prestamo.update(datos)

                    break

            mensaje = "Préstamo actualizado correctamente."

        # REGISTRAR PRÉSTAMO

        else:
            nuevo_id = max([p["id"] for p in self.prestamos], default=0) + 1

            datos["id"] = nuevo_id

            self.prestamos.append(datos)

            mensaje = "Préstamo registrado correctamente."

        messagebox.showinfo("Operación exitosa", mensaje)

        self.limpiar_formulario()

        self.actualizar_directorio()

        self.cambiar_pestana(self.frame_directorio)

    # ==========================================
    # EDITAR PRÉSTAMO
    # ==========================================

    def editar_seleccionado(self):

        if not self.prestamo_seleccionado:
            messagebox.showwarning(
                "Seleccionar préstamo", "Primero selecciona un préstamo del directorio."
            )

            return

        prestamo = self.prestamo_seleccionado

        for clave, entrada in self.campos.items():
            if isinstance(entrada, ctk.CTkEntry):
                entrada.delete(0, "end")

                entrada.insert(0, prestamo[clave])

            else:
                entrada.set(prestamo[clave])

        self.cambiar_pestana(self.frame_registro)

    # ==========================================
    # REGISTRAR DEVOLUCIÓN
    # ==========================================

    def registrar_devolucion(self):

        if not self.prestamo_seleccionado:
            messagebox.showwarning(
                "Seleccionar préstamo",
                "Selecciona un préstamo para registrar su devolución.",
            )

            return

        prestamo = self.prestamo_seleccionado

        if prestamo["estado"] == "Devuelto":
            messagebox.showinfo(
                "Préstamo devuelto",
                "Este libro ya se encuentra registrado como devuelto.",
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar devolución",
            f"¿Confirmas la devolución del libro '{prestamo['libro']}'?",
        )

        if not confirmar:
            return

        prestamo["estado"] = "Devuelto"

        self.prestamo_seleccionado = None

        self.actualizar_directorio()

        messagebox.showinfo(
            "Devolución exitosa", "El libro se registró como devuelto correctamente."
        )

    # ==========================================
    # ELIMINAR PRÉSTAMO
    # ==========================================

    def eliminar_seleccionado(self):

        if not self.prestamo_seleccionado:
            messagebox.showwarning(
                "Seleccionar préstamo", "Selecciona un préstamo para eliminar."
            )

            return

        prestamo = self.prestamo_seleccionado

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el préstamo del libro '{prestamo['libro']}'?",
        )

        if not confirmar:
            return

        self.prestamos = [p for p in self.prestamos if p["id"] != prestamo["id"]]

        self.prestamo_seleccionado = None

        self.actualizar_directorio()

        messagebox.showinfo(
            "Préstamo eliminado", "El registro del préstamo se eliminó correctamente."
        )

