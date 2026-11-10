import customtkinter as ctk
from tkinter import messagebox
import re


class Usuarios(ctk.CTkFrame):
    def __init__(self, parent, usuario=None):
        super().__init__(parent, fg_color="white")

        self.usuario = usuario

        # Datos de ejemplo
        self.empleados = [
            {
                "id": 1,
                "nombre": "Carlos Hernández",
                "puesto": "Administrador",
                "departamento": "Administración",
                "correo": "carlos@empresa.com",
                "telefono": "3312345678",
                "estado": "Activo",
            },
            {
                "id": 2,
                "nombre": "María González",
                "puesto": "Contadora",
                "departamento": "Finanzas",
                "correo": "maria@empresa.com",
                "telefono": "3312345679",
                "estado": "Activo",
            },
            {
                "id": 3,
                "nombre": "Luis Ramírez",
                "puesto": "Desarrollador",
                "departamento": "Tecnología",
                "correo": "luis@empresa.com",
                "telefono": "3312345680",
                "estado": "Vacaciones",
            },
        ]

        self.empleado_seleccionado = None
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
            text="Gestión de empleados",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#1f2937",
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Administra, registra y consulta los empleados de la empresa.",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280",
        ).pack(anchor="w", pady=3)

        # ======================================
        # ESTADÍSTICAS
        # ======================================

        self.estadisticas_frame = ctk.CTkFrame(principal, fg_color="transparent")
        self.estadisticas_frame.pack(fill="x", pady=(0, 15))

        self.crear_estadisticas()

        # ======================================
        # NAVEGACIÓN
        # ======================================

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
            text="👥 Directorio",
            fg_color="transparent",
            text_color="#1f2937",
            hover_color="#d1d5db",
            command=lambda: self.cambiar_pestana(self.frame_directorio),
        ).pack(side="left", padx=3, pady=3)

        ctk.CTkButton(
            navegacion,
            text="➕ Nuevo empleado",
            fg_color="transparent",
            text_color="#1f2937",
            hover_color="#d1d5db",
            command=self.nuevo_empleado,
        ).pack(side="left", padx=3, pady=3)

        self.cambiar_pestana(self.frame_directorio)

    # ==========================================
    # ESTADÍSTICAS
    # ==========================================

    def crear_estadisticas(self):

        for widget in self.estadisticas_frame.winfo_children():
            widget.destroy()

        total = len(self.empleados)

        activos = sum(e["estado"] == "Activo" for e in self.empleados)

        inactivos = sum(e["estado"] == "Inactivo" for e in self.empleados)

        departamentos = len(set(e["departamento"] for e in self.empleados))

        datos = [
            ("👥 Total empleados", total, "#2563eb"),
            ("🟢 Activos", activos, "#16a34a"),
            ("🔴 Inactivos", inactivos, "#dc2626"),
            ("🏢 Departamentos", departamentos, "#7c3aed"),
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
    # DIRECTORIO DE EMPLEADOS
    # ==========================================

    def crear_directorio(self):

        widget = ctk.CTkFrame(self.contenedor, fg_color="transparent")

        ctk.CTkLabel(
            widget,
            text="Directorio de empleados",
            text_color="#1f2937",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", pady=(0, 12))

        # BUSCADOR

        self.buscador = ctk.CTkEntry(
            widget,
            placeholder_text="Buscar por nombre, puesto, departamento o correo...",
            height=38,
        )
        self.buscador.pack(fill="x", pady=(0, 10))

        self.buscador.bind("<KeyRelease>", lambda event: self.actualizar_directorio())

        # FILTROS

        filtros = ctk.CTkFrame(widget, fg_color="transparent")
        filtros.pack(fill="x", pady=(0, 12))

        self.filtro_departamento = ctk.CTkComboBox(
            filtros,
            values=["Todos"],
            width=190,
            command=lambda valor: self.actualizar_directorio(),
        )
        self.filtro_departamento.pack(side="left", padx=(0, 10))

        self.filtro_estado = ctk.CTkComboBox(
            filtros,
            values=["Todos", "Activo", "Inactivo", "Vacaciones"],
            width=160,
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

        self.lista_empleados = ctk.CTkScrollableFrame(
            widget, fg_color="#f3f4f6", corner_radius=10
        )
        self.lista_empleados.pack(fill="both", expand=True)

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
            text="🗑 Dar de baja",
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

        for widget in self.lista_empleados.winfo_children():
            widget.destroy()

        departamentos = sorted(set(e["departamento"] for e in self.empleados))

        opciones = ["Todos"] + departamentos

        self.filtro_departamento.configure(values=opciones)

        if self.filtro_departamento.get() not in opciones:
            self.filtro_departamento.set("Todos")

        texto = self.buscador.get().lower().strip()

        departamento = self.filtro_departamento.get()
        estado = self.filtro_estado.get()

        resultados = []

        for empleado in self.empleados:
            coincide_texto = any(
                texto in empleado[campo].lower()
                for campo in ["nombre", "puesto", "departamento", "correo"]
            )

            coincide_departamento = (
                departamento == "Todos" or empleado["departamento"] == departamento
            )

            coincide_estado = estado == "Todos" or empleado["estado"] == estado

            if coincide_texto and coincide_departamento and coincide_estado:
                resultados.append(empleado)

        self.tarjetas_empleados = []

        for empleado in resultados:
            tarjeta = ctk.CTkFrame(
                self.lista_empleados,
                fg_color="white",
                corner_radius=10,
                border_width=1,
                border_color="#e5e7eb",
            )

            tarjeta.pack(fill="x", padx=8, pady=6)

            contenido = ctk.CTkFrame(tarjeta, fg_color="transparent")
            contenido.pack(fill="x", padx=15, pady=12)

            # AVATAR

            avatar = ctk.CTkFrame(
                contenido, width=55, height=55, fg_color="#dbeafe", corner_radius=30
            )
            avatar.pack(side="left", padx=(0, 15))
            avatar.pack_propagate(False)

            iniciales = "".join(
                palabra[0].upper() for palabra in empleado["nombre"].split()[:2]
            )

            ctk.CTkLabel(
                avatar,
                text=iniciales,
                text_color="#2563eb",
                font=ctk.CTkFont(size=17, weight="bold"),
            ).pack(expand=True)

            # INFORMACIÓN

            info = ctk.CTkFrame(contenido, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(
                info,
                text=empleado["nombre"],
                text_color="#1f2937",
                font=ctk.CTkFont(size=17, weight="bold"),
            ).pack(anchor="w")

            ctk.CTkLabel(
                info,
                text=f"{empleado['puesto']} | {empleado['departamento']}",
                text_color="#4b5563",
            ).pack(anchor="w", pady=2)

            ctk.CTkLabel(
                info,
                text=f"✉ {empleado['correo']}    ☎ {empleado['telefono']}",
                text_color="#6b7280",
            ).pack(anchor="w")

            # ESTADO

            colores = {
                "Activo": "#16a34a",
                "Inactivo": "#dc2626",
                "Vacaciones": "#d97706",
            }

            ctk.CTkLabel(
                contenido,
                text=empleado["estado"],
                text_color=colores.get(empleado["estado"], "#6b7280"),
                font=ctk.CTkFont(weight="bold"),
            ).pack(side="right", padx=10)

            # SELECCIÓN

            tarjeta.bind(
                "<Button-1>", lambda event, e=empleado: self.seleccionar_empleado(e)
            )

            for hijo in contenido.winfo_children():
                hijo.bind(
                    "<Button-1>", lambda event, e=empleado: self.seleccionar_empleado(e)
                )

            for hijo in info.winfo_children():
                hijo.bind(
                    "<Button-1>", lambda event, e=empleado: self.seleccionar_empleado(e)
                )

            self.tarjetas_empleados.append((tarjeta, empleado))

        if not resultados:
            ctk.CTkLabel(
                self.lista_empleados,
                text="No se encontraron empleados.",
                text_color="#6b7280",
                font=ctk.CTkFont(size=14),
            ).pack(pady=30)

        self.crear_estadisticas()

    # ==========================================
    # SELECCIONAR EMPLEADO
    # ==========================================

    def seleccionar_empleado(self, empleado):

        self.empleado_seleccionado = empleado

        for tarjeta, datos in self.tarjetas_empleados:
            tarjeta.configure(
                border_color=("#2563eb" if datos["id"] == empleado["id"] else "#e5e7eb")
            )

    # ==========================================
    # FORMULARIO DE EMPLEADOS
    # ==========================================

    def crear_formulario(self):

        widget = ctk.CTkFrame(self.contenedor, fg_color="transparent")

        ctk.CTkLabel(
            widget,
            text="Registro de empleados",
            text_color="#1f2937",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", pady=(0, 15))

        formulario = ctk.CTkScrollableFrame(
            widget, fg_color="#f9fafb", corner_radius=10
        )
        formulario.pack(fill="both", expand=True)

        self.campos = {}

        campos = [
            ("nombre", "Nombre completo"),
            ("puesto", "Puesto de trabajo"),
            ("correo", "Correo electrónico"),
            ("telefono", "Teléfono"),
        ]

        for clave, placeholder in campos:
            ctk.CTkLabel(formulario, text=placeholder, text_color="#374151").pack(
                anchor="w", padx=15, pady=(12, 3)
            )

            entrada = ctk.CTkEntry(formulario, placeholder_text=placeholder, height=38)
            entrada.pack(fill="x", padx=15)

            self.campos[clave] = entrada

        # DEPARTAMENTO

        ctk.CTkLabel(formulario, text="Departamento", text_color="#374151").pack(
            anchor="w", padx=15, pady=(12, 3)
        )

        self.campos["departamento"] = ctk.CTkComboBox(
            formulario,
            values=[
                "Administración",
                "Finanzas",
                "Tecnología",
                "Recursos Humanos",
                "Ventas",
                "Marketing",
                "Operaciones",
            ],
            height=38,
        )
        self.campos["departamento"].pack(fill="x", padx=15)

        # ESTADO

        ctk.CTkLabel(formulario, text="Estado del empleado", text_color="#374151").pack(
            anchor="w", padx=15, pady=(12, 3)
        )

        self.campos["estado"] = ctk.CTkComboBox(
            formulario, values=["Activo", "Inactivo", "Vacaciones"], height=38
        )
        self.campos["estado"].set("Activo")
        self.campos["estado"].pack(fill="x", padx=15)

        # BOTONES

        botones = ctk.CTkFrame(formulario, fg_color="transparent")
        botones.pack(fill="x", padx=15, pady=20)

        ctk.CTkButton(
            botones,
            text="💾 Guardar empleado",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.guardar_empleado,
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

            else:
                entrada.set("")

        self.empleado_seleccionado = None

    # ==========================================
    # NUEVO EMPLEADO
    # ==========================================

    def nuevo_empleado(self):

        self.limpiar_formulario()

        self.cambiar_pestana(self.frame_registro)

    # ==========================================
    # GUARDAR EMPLEADO
    # ==========================================

    def guardar_empleado(self):

        datos = {clave: entrada.get().strip() for clave, entrada in self.campos.items()}

        if any(not valor for valor in datos.values()):
            messagebox.showwarning("Campos obligatorios", "Completa todos los campos.")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", datos["correo"]):
            messagebox.showwarning(
                "Correo inválido", "Introduce un correo electrónico válido."
            )
            return

        # COMPROBAR CORREO DUPLICADO

        for empleado in self.empleados:
            if (
                empleado["correo"].lower() == datos["correo"].lower()
                and empleado["id"] != self.empleado_seleccionado["id"]
                if self.empleado_seleccionado
                else empleado["correo"].lower() == datos["correo"].lower()
            ):
                messagebox.showwarning(
                    "Correo duplicado", "Ya existe un empleado con ese correo."
                )
                return

        if self.empleado_seleccionado:
            # EDITAR EMPLEADO

            for empleado in self.empleados:
                if empleado["id"] == self.empleado_seleccionado["id"]:
                    empleado.update(datos)
                    break

            mensaje = "Empleado actualizado correctamente."

        else:
            # REGISTRAR EMPLEADO

            nuevo_id = max([e["id"] for e in self.empleados], default=0) + 1

            datos["id"] = nuevo_id

            self.empleados.append(datos)

            mensaje = "Empleado registrado correctamente."

        messagebox.showinfo("Operación exitosa", mensaje)

        self.limpiar_formulario()
        self.actualizar_directorio()
        self.cambiar_pestana(self.frame_directorio)

    # ==========================================
    # EDITAR EMPLEADO
    # ==========================================

    def editar_seleccionado(self):

        if not self.empleado_seleccionado:
            messagebox.showwarning(
                "Seleccionar empleado", "Primero selecciona un empleado del directorio."
            )
            return

        empleado = self.empleado_seleccionado

        for clave, entrada in self.campos.items():
            entrada.delete(0, "end") if isinstance(entrada, ctk.CTkEntry) else None

            entrada.insert(0, empleado[clave]) if isinstance(
                entrada, ctk.CTkEntry
            ) else entrada.set(empleado[clave])

        self.cambiar_pestana(self.frame_registro)

    # ==========================================
    # ELIMINAR EMPLEADO
    # ==========================================

    def eliminar_seleccionado(self):

        if not self.empleado_seleccionado:
            messagebox.showwarning(
                "Seleccionar empleado", "Selecciona un empleado para darlo de baja."
            )
            return

        empleado = self.empleado_seleccionado

        confirmar = messagebox.askyesno(
            "Confirmar baja", f"¿Deseas dar de baja a {empleado['nombre']}?"
        )

        if not confirmar:
            return

        self.empleados = [e for e in self.empleados if e["id"] != empleado["id"]]

        self.empleado_seleccionado = None

        self.actualizar_directorio()

        messagebox.showinfo(
            "Empleado dado de baja", "El empleado se eliminó del listado."
        )
