import customtkinter as ctk
from tkinter import messagebox

from Inicio import Inicio
from Libros import Libros
from Prestamos import Prestamos
from Usuarios import Usuarios
from Configuracion import Configuracion


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Biblioteca don Epifanio")
        self.geometry("1250x800")
        self.minsize(1000, 650)
        self.configure(fg_color="#ffffff")

        # VARIABLES PRINCIPALES
        self.usuario = None
        self.frame_actual = None

        self.crear_interfaz()

    # INTERFAZ PRINCIPAL
    def crear_interfaz(self):

        # MARCO PRINCIPAL
        principal = ctk.CTkFrame(self, fg_color="transparent")

        principal.pack(fill="both", expand=True)

        # BARRA LATERAL
        self.barra = ctk.CTkFrame(
            principal, width=220, corner_radius=0, fg_color="#202c3c"
        )

        self.barra.pack(side="left", fill="y")
        self.barra.pack_propagate(False)

        # TÍTULO
        ctk.CTkLabel(
            self.barra,
            text="BIBLIOTECA",
            text_color="white",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=20, pady=(25, 30))

        # CONTENEDOR PRINCIPAL
        self.contenido = ctk.CTkFrame(principal, fg_color="#ffffff", corner_radius=0)

        self.contenido.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # OPCIONES DEL MENÚ
        opciones = [
            ("🏠  Inicio", self.mostrar_inicio),
            ("📚  Libros", lambda: self.mostrar_frame(Libros)),
            ("👥  Usuarios", lambda: self.mostrar_frame(Usuarios)),
            ("📋  Préstamos", lambda: self.mostrar_frame(Prestamos)),
            ("⚙  Configuración", lambda: self.mostrar_frame(Configuracion)),
        ]

        for texto, comando in opciones:
            boton = ctk.CTkButton(
                self.barra,
                text=texto,
                fg_color="transparent",
                text_color="white",
                hover_color="#34465e",
                anchor="w",
                font=ctk.CTkFont(size=14),
                height=42,
                corner_radius=6,
                command=comando,
            )

            boton.pack(fill="x", padx=12, pady=5)

        # BOTÓN INICIAR SESIÓN
        boton_login = ctk.CTkButton(
            self.barra,
            text="🔐  Iniciar sesión",
            fg_color="transparent",
            text_color="#9ca3af",
            hover_color="#34465e",
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=self.abrir_login,
        )

        boton_login.pack(side="bottom", fill="x", padx=12, pady=20)

        # MOSTRAR INICIO
        self.mostrar_inicio()

    # MOSTRAR MÓDULOS
    def mostrar_frame(self, clase_frame):

        # ELIMINAR CONTENIDO ANTERIOR
        for widget in self.contenido.winfo_children():
            widget.destroy()

        try:
            # CREAR MÓDULO
            nuevo_frame = clase_frame(self.contenido, self.usuario)

            nuevo_frame.pack(fill="both", expand=True)

            self.frame_actual = nuevo_frame

        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo abrir el módulo seleccionado:\n\n{e}"
            )

    # MOSTRAR INICIO
    def mostrar_inicio(self):
        self.mostrar_frame(Inicio)

    # INICIAR SESIÓN
    def abrir_login(self):

        ventana = ctk.CTkToplevel(self)

        ventana.title("Inicio de sesión")
        ventana.geometry("420x480")
        ventana.resizable(False, False)

        ventana.configure(fg_color="#f3f4f6")

        ventana.transient(self)
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="🔐", font=ctk.CTkFont(size=45)).pack(pady=(25, 5))

        ctk.CTkLabel(
            ventana,
            text="Iniciar sesión",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#202c3c",
        ).pack(pady=5)

        ctk.CTkLabel(
            ventana,
            text="Ingresa tus credenciales para continuar",
            text_color="#6b7280",
            font=ctk.CTkFont(size=13),
        ).pack(pady=(0, 20))

        usuario = ctk.CTkEntry(
            ventana, placeholder_text="Nombre de usuario", width=320, height=42
        )

        usuario.pack(pady=10)

        contrasena = ctk.CTkEntry(
            ventana, placeholder_text="Contraseña", show="*", width=320, height=42
        )

        contrasena.pack(pady=10)

        mensaje = ctk.CTkLabel(
            ventana, text="", text_color="#dc2626", font=ctk.CTkFont(size=12)
        )

        mensaje.pack(pady=8)

        def iniciar_sesion():

            nombre_usuario = usuario.get().strip()
            password = contrasena.get().strip()

            if not nombre_usuario or not password:
                mensaje.configure(
                    text="Completa todos los campos.", text_color="#dc2626"
                )

                return

            mensaje.configure(
                text="Conecta aquí tu sistema de autenticación.", text_color="#2563eb"
            )

        ctk.CTkButton(
            ventana,
            text="Entrar",
            width=320,
            height=42,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=iniciar_sesion,
        ).pack(pady=12)

        ctk.CTkButton(
            ventana,
            text="Cancelar",
            width=320,
            height=38,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=ventana.destroy,
        ).pack(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
