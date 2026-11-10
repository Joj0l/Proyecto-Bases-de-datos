import customtkinter as ctk
from tkinter import messagebox


class Configuracion(ctk.CTkFrame):
    def __init__(self, parent, usuario=None):
        super().__init__(parent, fg_color="white")

        self.usuario = usuario

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
            text="Configuración del sistema",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#1f2937",
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Personaliza y administra las preferencias del sistema.",
            font=ctk.CTkFont(size=13),
            text_color="#6b7280",
        ).pack(anchor="w", pady=3)

        # CONTENEDOR PRINCIPAL

        self.contenedor = ctk.CTkScrollableFrame(
            principal, fg_color="#f3f4f6", corner_radius=10
        )

        self.contenedor.pack(fill="both", expand=True)

        # SECCIONES

        self.crear_seccion_general()
        self.crear_seccion_apariencia()
        self.crear_seccion_prestamos()
        self.crear_seccion_notificaciones()
        self.crear_seccion_seguridad()
        self.crear_seccion_sistema()

    # ==========================================
    # CREAR TÍTULO DE SECCIÓN
    # ==========================================

    def crear_titulo_seccion(self, parent, titulo, descripcion):

        encabezado = ctk.CTkFrame(parent, fg_color="transparent")

        encabezado.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            encabezado,
            text=titulo,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1f2937",
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text=descripcion,
            font=ctk.CTkFont(size=12),
            text_color="#6b7280",
        ).pack(anchor="w", pady=2)

    # ==========================================
    # CREAR TARJETA DE SECCIÓN
    # ==========================================

    def crear_tarjeta(self, titulo, descripcion):

        tarjeta = ctk.CTkFrame(
            self.contenedor,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#e5e7eb",
        )

        tarjeta.pack(fill="x", padx=10, pady=8)

        self.crear_titulo_seccion(tarjeta, titulo, descripcion)

        return tarjeta

    # ==========================================
    # CREAR OPCIÓN CON INTERRUPTOR
    # ==========================================

    def crear_interruptor(self, parent, titulo, descripcion, valor=False):

        fila = ctk.CTkFrame(parent, fg_color="transparent")

        fila.pack(fill="x", padx=20, pady=10)

        info = ctk.CTkFrame(fila, fg_color="transparent")

        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            info,
            text=titulo,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info, text=descripcion, font=ctk.CTkFont(size=11), text_color="#6b7280"
        ).pack(anchor="w")

        interruptor = ctk.CTkSwitch(fila, text="", progress_color="#2563eb")

        interruptor.pack(side="right")

        if valor:
            interruptor.select()

        return interruptor

    # ==========================================
    # CREAR OPCIÓN CON SELECTOR
    # ==========================================

    def crear_selector(self, parent, titulo, opciones, valor):

        fila = ctk.CTkFrame(parent, fg_color="transparent")

        fila.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            fila,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#374151",
        ).pack(side="left", anchor="w")

        selector = ctk.CTkComboBox(fila, values=opciones, width=180, height=35)

        selector.set(valor)

        selector.pack(side="right")

        return selector

    # ==========================================
    # CREAR CAMPO DE TEXTO
    # ==========================================

    def crear_campo(self, parent, titulo, placeholder, valor=""):

        fila = ctk.CTkFrame(parent, fg_color="transparent")

        fila.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            fila,
            text=titulo,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#374151",
        ).pack(anchor="w", pady=(0, 5))

        entrada = ctk.CTkEntry(fila, placeholder_text=placeholder, height=36)

        entrada.pack(fill="x")

        if valor:
            entrada.insert(0, valor)

        return entrada

    # ==========================================
    # CONFIGURACIÓN GENERAL
    # ==========================================

    def crear_seccion_general(self):

        tarjeta = self.crear_tarjeta(
            "⚙ Configuración general",
            "Administra las preferencias principales de la biblioteca.",
        )

        self.crear_campo(
            tarjeta,
            "Nombre de la institución",
            "Introduce el nombre de la institución",
            "Biblioteca Central",
        )

        self.crear_campo(
            tarjeta,
            "Nombre del sistema",
            "Introduce el nombre del sistema",
            "Sistema de Gestión Bibliotecaria",
        )

        self.crear_selector(
            tarjeta, "Idioma del sistema", ["Español", "Inglés", "Francés"], "Español"
        )

        self.crear_selector(
            tarjeta,
            "Formato de fecha",
            ["DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"],
            "AAAA-MM-DD",
        )

        self.crear_interruptor(
            tarjeta,
            "Inicio de sesión automático",
            "Mantener la sesión iniciada en el sistema.",
            False,
        )

        ctk.CTkButton(
            tarjeta,
            text="Guardar configuración",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=160,
        ).pack(anchor="e", padx=20, pady=15)

    # ==========================================
    # APARIENCIA
    # ==========================================

    def crear_seccion_apariencia(self):

        tarjeta = self.crear_tarjeta(
            "🎨 Apariencia", "Personaliza los colores y el aspecto visual del sistema."
        )

        self.crear_selector(
            tarjeta, "Tema de la aplicación", ["Claro", "Oscuro", "Sistema"], "Claro"
        )

        self.crear_selector(
            tarjeta, "Color principal", ["Azul", "Verde", "Morado", "Rojo"], "Azul"
        )

        self.crear_selector(
            tarjeta, "Tamaño de fuente", ["Pequeño", "Mediano", "Grande"], "Mediano"
        )

        self.crear_interruptor(
            tarjeta, "Animaciones", "Mostrar animaciones en las transiciones.", True
        )

        self.crear_interruptor(
            tarjeta, "Modo compacto", "Reducir el espacio entre los elementos.", False
        )

        ctk.CTkButton(
            tarjeta,
            text="Aplicar apariencia",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=160,
        ).pack(anchor="e", padx=20, pady=15)

    # ==========================================
    # CONFIGURACIÓN DE PRÉSTAMOS
    # ==========================================

    def crear_seccion_prestamos(self):

        tarjeta = self.crear_tarjeta(
            "📚 Configuración de préstamos",
            "Define las reglas generales para el préstamo de libros.",
        )

        self.crear_selector(
            tarjeta,
            "Duración del préstamo",
            ["7 días", "14 días", "21 días", "30 días"],
            "14 días",
        )

        self.crear_selector(
            tarjeta,
            "Máximo de libros por usuario",
            ["1", "2", "3", "4", "5", "10"],
            "3",
        )

        self.crear_selector(
            tarjeta,
            "Días de tolerancia",
            ["0 días", "1 día", "2 días", "3 días", "5 días"],
            "0 días",
        )

        self.crear_interruptor(
            tarjeta,
            "Permitir renovaciones",
            "Permitir extender la fecha de devolución.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Bloquear préstamos vencidos",
            "Impedir nuevos préstamos a usuarios con retrasos.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Permitir reservas",
            "Habilitar reservas de libros no disponibles.",
            False,
        )

        ctk.CTkButton(
            tarjeta,
            text="Guardar reglas",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=160,
        ).pack(anchor="e", padx=20, pady=15)

    # ==========================================
    # NOTIFICACIONES
    # ==========================================

    def crear_seccion_notificaciones(self):

        tarjeta = self.crear_tarjeta(
            "🔔 Notificaciones", "Configura los avisos y recordatorios del sistema."
        )

        self.crear_interruptor(
            tarjeta,
            "Notificaciones de préstamos",
            "Mostrar avisos cuando se registre un nuevo préstamo.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Recordatorios de devolución",
            "Avisar cuando se acerque la fecha de devolución.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Notificar préstamos vencidos",
            "Mostrar avisos de libros que no fueron devueltos a tiempo.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Notificaciones de nuevos usuarios",
            "Avisar cuando se registre un nuevo usuario.",
            False,
        )

        self.crear_selector(
            tarjeta,
            "Anticipación del recordatorio",
            ["1 día", "2 días", "3 días", "5 días"],
            "2 días",
        )

        ctk.CTkButton(
            tarjeta,
            text="Guardar notificaciones",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=180,
        ).pack(anchor="e", padx=20, pady=15)

    # ==========================================
    # SEGURIDAD Y CUENTA
    # ==========================================

    def crear_seccion_seguridad(self):

        tarjeta = self.crear_tarjeta(
            "🔒 Seguridad y cuenta",
            "Opciones relacionadas con el acceso y la protección del sistema.",
        )

        self.crear_selector(
            tarjeta,
            "Tiempo de cierre de sesión",
            ["5 minutos", "10 minutos", "15 minutos", "30 minutos", "Nunca"],
            "15 minutos",
        )

        self.crear_interruptor(
            tarjeta,
            "Confirmar acciones importantes",
            "Solicitar confirmación antes de eliminar registros.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Registro de actividad",
            "Mantener un historial de las operaciones realizadas.",
            True,
        )

        self.crear_interruptor(
            tarjeta,
            "Protección de sesión",
            "Solicitar autenticación al regresar al sistema.",
            False,
        )

        # INFORMACIÓN DE CUENTA

        ctk.CTkLabel(
            tarjeta,
            text="Información de la cuenta",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151",
        ).pack(anchor="w", padx=20, pady=(15, 5))

        nombre_usuario = "Administrador"

        if self.usuario:
            nombre_usuario = str(self.usuario)

        ctk.CTkLabel(
            tarjeta,
            text=f"Usuario actual: {nombre_usuario}",
            text_color="#6b7280",
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=20, pady=5)

        ctk.CTkButton(
            tarjeta,
            text="Cambiar contraseña",
            fg_color="#6b7280",
            hover_color="#4b5563",
            width=160,
        ).pack(anchor="e", padx=20, pady=15)

    # ==========================================
    # INFORMACIÓN DEL SISTEMA
    # ==========================================

    def crear_seccion_sistema(self):

        tarjeta = self.crear_tarjeta(
            "💻 Información del sistema",
            "Consulta los datos generales de la aplicación.",
        )

        datos = [
            ("Nombre del sistema", "Sistema de Gestión Bibliotecaria"),
            ("Versión", "1.0.0"),
            ("Desarrollado en", "Python"),
            ("Interfaz gráfica", "CustomTkinter"),
            ("Base de datos", "Por configurar"),
            ("Estado del sistema", "En desarrollo"),
        ]

        for titulo, valor in datos:
            fila = ctk.CTkFrame(tarjeta, fg_color="transparent")

            fila.pack(fill="x", padx=20, pady=7)

            ctk.CTkLabel(
                fila, text=titulo, text_color="#4b5563", font=ctk.CTkFont(size=13)
            ).pack(side="left")

            ctk.CTkLabel(
                fila,
                text=valor,
                text_color="#1f2937",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(side="right")

        ctk.CTkButton(
            tarjeta,
            text="Buscar actualizaciones",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            width=180,
        ).pack(anchor="e", padx=20, pady=15)

        # PIE DE PÁGINA

        ctk.CTkLabel(
            self.contenedor,
            text="Sistema de Gestión Bibliotecaria | Versión 1.0.0",
            text_color="#9ca3af",
            font=ctk.CTkFont(size=11),
        ).pack(pady=15)
