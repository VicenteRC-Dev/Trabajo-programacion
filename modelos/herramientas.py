import io
import random
import string
import webbrowser as web
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pyqrcode
from faker import Faker
from PIL import Image

from modelos.calculadora_run import CalculadoraRUN


class GeneradorDatos:
    """Capa lógica encargada de generar datos ficticios y códigos QR."""

    def __init__(self):
        self.fake = Faker()

    def generar_ips(self, cantidad: int) -> list[str]:
        return [self.fake.ipv4() for _ in range(cantidad)]

    def generar_user_agents(self, cantidad: int) -> list[str]:
        return [self.fake.user_agent() for _ in range(cantidad)]

    def generar_direcciones(self, cantidad: int) -> list[str]:
        return [self.fake.address().replace("\n", ", ") for _ in range(cantidad)]

    def generar_tarjetas(self, cantidad: int, tipo: str = "Ambas") -> list[str]:
        meses = [f"{m:02d}" for m in range(1, 13)]
        resultados = []

        for _ in range(cantidad):
            marca_actual = (
                random.choice(["Visa", "MasterCard"])
                if tipo == "Ambas"
                else tipo
            )
            mes = random.choice(meses)
            anio = random.randint(26, 32)
            cvv = "".join(random.choices(string.digits, k=3))
            titular = self.fake.name()
            direccion = self.fake.street_address()

            if marca_actual == "Visa":
                numero = "4" + "".join(random.choices(string.digits, k=15))
            else:
                prefijo = random.randint(51, 55)
                numero = f"{prefijo}" + "".join(random.choices(string.digits, k=14))

            numero_formateado = " ".join(
                numero[i : i + 4] for i in range(0, len(numero), 4)
            )
            bloque = (
                f"Marca:       {marca_actual}\n"
                f"Número:      {numero_formateado}\n"
                f"Titular:     {titular}\n"
                f"Vencimiento: {mes}/20{anio}  |  CVV: {cvv}\n"
                f"Dirección:   {direccion}"
            )
            resultados.append(bloque)

        return resultados

    def generar_telefonos(self, cantidad: int, pais: str = "Aleatorio") -> list[str]:
        paises_disponibles = ["Chile", "España", "Perú", "Colombia"]
        resultados = []

        for _ in range(cantidad):
            pais_actual = (
                random.choice(paises_disponibles)
                if pais == "Aleatorio"
                else pais
            )

            if pais_actual == "Chile":
                numero = f"+56 9 {random.randint(1000, 9999)} {random.randint(1000, 9999)}"
            elif pais_actual == "España":
                inicio = random.choice([6, 7])
                numero = (
                    f"+34 {inicio}{random.randint(10, 99)} "
                    f"{random.randint(100, 999)} {random.randint(100, 999)}"
                )
            elif pais_actual == "Perú":
                numero = (
                    f"+51 9{random.randint(10, 99)} "
                    f"{random.randint(100, 999)} {random.randint(100, 999)}"
                )
            else:
                numero = (
                    f"+57 3{random.randint(0, 5)}{random.randint(0, 9)} "
                    f"{random.randint(100, 999)} {random.randint(1000, 9999)}"
                )

            resultados.append(f"[{pais_actual}]  {numero}")

        return resultados

    @staticmethod
    def crear_imagen_qr(texto: str, scale: int = 8) -> tuple[pyqrcode.QRCode, Image.Image]:
        qr = pyqrcode.create(texto)
        buffer = io.BytesIO()
        qr.png(buffer, scale=scale)
        buffer.seek(0)
        imagen_pil = Image.open(buffer).convert("RGB")
        return qr, imagen_pil


class Herramientas(ctk.CTk):
    """Interfaz gráfica principal del proyecto."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("KDZ Tools v2.0 — Herramientas y Generadores")
        self.geometry("980x640")
        self.minsize(860, 560)

        self.generador = GeneradorDatos()
        self.calculadora = CalculadoraRUN()
        self.vista_actual = "ips"
        self.qr_actual = None
        self.qr_ctk_image = None
        self.botones_nav = {}

        self._configurar_layout()
        self._construir_sidebar()
        self._construir_vistas()
        self.mostrar_vista("ips")

    # Alias por compatibilidad con la estructura original
    def menu_principal(self):
        self.mainloop()

    def _configurar_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Cabecera / Logo
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(20, 14))

        ctk.CTkLabel(
            header,
            text="KDZ | 😼 | TOOLS",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Herramientas y Generadores • v2.0",
            font=ctk.CTkFont(size=12),
            text_color="gray70",
        ).pack(anchor="w")

        # Sección: Generadores
        self._agregar_titulo_seccion("GENERADORES FAKES")
        items_generadores = [
            ("ips", "🌐  Direcciones IP"),
            ("user_agents", "🧭  User-Agents"),
            ("direcciones", "📍  Direcciones"),
            ("tarjetas", "💳  Tarjetas"),
            ("telefonos", "📱  Teléfonos"),
        ]
        for clave, texto in items_generadores:
            self._agregar_boton_nav(clave, texto)

        # Sección: Herramientas
        self._agregar_titulo_seccion("HERRAMIENTAS")
        items_herramientas = [
            ("run", "🪪  Calculadora RUN (SQL)"),
            ("qr", "🔳  Generador Código QR"),
        ]
        for clave, texto in items_herramientas:
            self._agregar_boton_nav(clave, texto)

        # Pie de barra lateral
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=14, pady=16)

        self.switch_tema = ctk.CTkSwitch(
            footer,
            text="Modo Oscuro",
            command=self._alternar_tema,
            font=ctk.CTkFont(size=12),
        )
        self.switch_tema.select()
        self.switch_tema.pack(anchor="w", padx=4, pady=(0, 10))

        ctk.CTkButton(
            footer,
            text="⭐ Apoyar al creador",
            fg_color="transparent",
            border_width=1,
            border_color="gray45",
            hover_color=("gray85", "gray25"),
            text_color=("gray15", "gray90"),
            height=34,
            command=lambda: web.open("https://github.com/vicenterc-dev"),
        ).pack(fill="x")

    def _agregar_titulo_seccion(self, titulo: str):
        ctk.CTkLabel(
            self.sidebar,
            text=titulo,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray60",
        ).pack(anchor="w", padx=20, pady=(12, 4))

    def _agregar_boton_nav(self, clave: str, texto: str):
        btn = ctk.CTkButton(
            self.sidebar,
            text=texto,
            anchor="w",
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color=("gray15", "gray88"),
            hover_color=("gray85", "gray25"),
            command=lambda c=clave: self.mostrar_vista(c),
        )
        btn.pack(fill="x", padx=12, pady=2)
        self.botones_nav[clave] = btn

    def _alternar_tema(self):
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def _construir_vistas(self):
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=24, pady=20)
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.contenedor.grid_rowconfigure(0, weight=1)

        self._crear_vista_generadores()
        self._crear_vista_run()
        self._crear_vista_qr()

    def mostrar_vista(self, clave: str):
        self.vista_actual = clave

        for k, btn in self.botones_nav.items():
            if k == clave:
                btn.configure(
                    fg_color=("#2563EB", "#1D4ED8"),
                    text_color="white",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("gray15", "gray88"),
                )

        self.frame_generadores.grid_forget()
        self.frame_run.grid_forget()
        self.frame_qr.grid_forget()

        if clave == "run":
            self.frame_run.grid(row=0, column=0, sticky="nsew")
            self._actualizar_lista_historial()
        elif clave == "qr":
            self.frame_qr.grid(row=0, column=0, sticky="nsew")
        else:
            self._configurar_vista_generador(clave)
            self.frame_generadores.grid(row=0, column=0, sticky="nsew")

    # ------------------------------------------------------------------
    # VISTA 1: GENERADORES FAKES (Reutilizable y limpia)
    # ------------------------------------------------------------------
    def _crear_vista_generadores(self):
        self.frame_generadores = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        self.frame_generadores.grid_columnconfigure(0, weight=1)
        self.frame_generadores.grid_rowconfigure(2, weight=1)

        # Cabecera
        header = ctk.CTkFrame(self.frame_generadores, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        self.lbl_gen_titulo = ctk.CTkLabel(
            header, text="", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_gen_titulo.pack(anchor="w")

        self.lbl_gen_subtitulo = ctk.CTkLabel(
            header, text="", font=ctk.CTkFont(size=13), text_color="gray65"
        )
        self.lbl_gen_subtitulo.pack(anchor="w")

        # Barra de controles
        controles = ctk.CTkFrame(self.frame_generadores, corner_radius=12)
        controles.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            controles, text="Cantidad:", font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(16, 8), pady=14)

        self.entry_cantidad = ctk.CTkEntry(controles, width=80, justify="center")
        self.entry_cantidad.insert(0, "5")
        self.entry_cantidad.pack(side="left", padx=(0, 16), pady=14)
        self.entry_cantidad.bind("<Return>", lambda _: self._ejecutar_generador())

        # Selector extra (para tarjetas o países)
        self.lbl_extra = ctk.CTkLabel(
            controles, text="Opción:", font=ctk.CTkFont(size=13, weight="bold")
        )
        self.combo_extra = ctk.CTkOptionMenu(controles, values=[""], width=170)

        ctk.CTkButton(
            controles,
            text="Generar",
            width=130,
            height=34,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._ejecutar_generador,
        ).pack(side="right", padx=16, pady=14)

        # Área de salida
        self.txt_resultados = ctk.CTkTextbox(
            self.frame_generadores,
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
        )
        self.txt_resultados.grid(row=2, column=0, sticky="nsew")

        # Barra inferior de acciones
        barra_inf = ctk.CTkFrame(self.frame_generadores, fg_color="transparent")
        barra_inf.grid(row=3, column=0, sticky="ew", pady=(12, 0))

        self.lbl_estado_gen = ctk.CTkLabel(
            barra_inf,
            text="Listo para generar.",
            font=ctk.CTkFont(size=12),
            text_color="gray65",
        )
        self.lbl_estado_gen.pack(side="left")

        ctk.CTkButton(
            barra_inf,
            text="Limpiar",
            width=95,
            height=32,
            fg_color="transparent",
            border_width=1,
            border_color="gray45",
            text_color=("gray15", "gray88"),
            hover_color=("gray85", "gray25"),
            command=self._limpiar_resultados,
        ).pack(side="right", padx=(8, 0))

        self.btn_copiar_gen = ctk.CTkButton(
            barra_inf,
            text="Copiar resultados",
            width=145,
            height=32,
            command=self._copiar_resultados,
        )
        self.btn_copiar_gen.pack(side="right")

    def _configurar_vista_generador(self, clave: str):
        info = {
            "ips": (
                "Generador de Direcciones IP",
                "Genera direcciones IPv4 aleatorias para pruebas de red.",
            ),
            "user_agents": (
                "Generador de User-Agents",
                "Genera cadenas User-Agent de distintos navegadores y sistemas.",
            ),
            "direcciones": (
                "Generador de Direcciones",
                "Crea direcciones postales ficticias en formato de una línea.",
            ),
            "tarjetas": (
                "Generador de Tarjetas Fakes",
                "Genera datos ficticios de tarjetas Visa y MasterCard para testing.",
            ),
            "telefonos": (
                "Generador de Teléfonos por País",
                "Genera números móviles con formato válido para Chile, España, Perú y Colombia.",
            ),
        }
        titulo, subtitulo = info[clave]
        self.lbl_gen_titulo.configure(text=titulo)
        self.lbl_gen_subtitulo.configure(text=subtitulo)

        self.lbl_extra.pack_forget()
        self.combo_extra.pack_forget()

        if clave == "tarjetas":
            self.lbl_extra.configure(text="Marca:")
            self.combo_extra.configure(values=["Ambas", "Visa", "MasterCard"])
            self.combo_extra.set("Ambas")
            self.lbl_extra.pack(side="left", padx=(0, 8), pady=14)
            self.combo_extra.pack(side="left", pady=14)
        elif clave == "telefonos":
            self.lbl_extra.configure(text="País:")
            self.combo_extra.configure(
                values=["Aleatorio", "Chile", "España", "Perú", "Colombia"]
            )
            self.combo_extra.set("Aleatorio")
            self.lbl_extra.pack(side="left", padx=(0, 8), pady=14)
            self.combo_extra.pack(side="left", pady=14)

        self._limpiar_resultados()

    def _ejecutar_generador(self):
        try:
            cantidad = int(self.entry_cantidad.get().strip())
            if cantidad <= 0 or cantidad > 500:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "Ingresa un número entero entre 1 y 500.",
            )
            return

        clave = self.vista_actual
        if clave == "ips":
            datos = self.generador.generar_ips(cantidad)
            texto = "\n".join(datos)
        elif clave == "user_agents":
            datos = self.generador.generar_user_agents(cantidad)
            texto = "\n\n".join(datos)
        elif clave == "direcciones":
            datos = self.generador.generar_direcciones(cantidad)
            texto = "\n".join(datos)
        elif clave == "tarjetas":
            tipo = self.combo_extra.get()
            datos = self.generador.generar_tarjetas(cantidad, tipo)
            separador = "\n" + ("─" * 46) + "\n"
            texto = separador.join(datos)
        elif clave == "telefonos":
            pais = self.combo_extra.get()
            datos = self.generador.generar_telefonos(cantidad, pais)
            texto = "\n".join(datos)
        else:
            return

        self.txt_resultados.delete("1.0", "end")
        self.txt_resultados.insert("1.0", texto)
        self.lbl_estado_gen.configure(text=f"✓ {cantidad} elemento(s) generado(s).")

    def _limpiar_resultados(self):
        self.txt_resultados.delete("1.0", "end")
        self.lbl_estado_gen.configure(text="Listo para generar.")

    def _copiar_resultados(self):
        contenido = self.txt_resultados.get("1.0", "end").strip()
        if not contenido:
            return
        self.clipboard_clear()
        self.clipboard_append(contenido)
        self.btn_copiar_gen.configure(text="✓ ¡Copiado!")
        self.after(1500, lambda: self.btn_copiar_gen.configure(text="Copiar resultados"))

    # ------------------------------------------------------------------
    # VISTA 2: CALCULADORA DE RUN (CON PERSISTENCIA SQLITE)
    # ------------------------------------------------------------------
    def _crear_vista_run(self):
        self.frame_run = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        self.frame_run.grid_columnconfigure(0, weight=1)
        self.frame_run.grid_rowconfigure(3, weight=1)

        # Cabecera
        header = ctk.CTkFrame(self.frame_run, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            header,
            text="Calculadora de Dígito Verificador (RUN)",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Calcula el dígito verificador con Módulo 11 y guarda automáticamente en SQLite.",
            font=ctk.CTkFont(size=13),
            text_color="gray65",
        ).pack(anchor="w")

        # Tarjeta de entrada
        card_input = ctk.CTkFrame(self.frame_run, corner_radius=12)
        card_input.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            card_input,
            text="RUN (sin DV):",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(side="left", padx=(16, 10), pady=16)

        self.entry_run = ctk.CTkEntry(
            card_input,
            placeholder_text="Ej: 12.345.678 o 12345678",
            width=230,
            height=36,
        )
        self.entry_run.pack(side="left", padx=(0, 12), pady=16)
        self.entry_run.bind("<Return>", lambda _: self._calcular_run_gui())

        ctk.CTkButton(
            card_input,
            text="Calcular y Guardar",
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._calcular_run_gui,
        ).pack(side="left", pady=16)

        # Tarjeta de resultado destacado
        card_res = ctk.CTkFrame(self.frame_run, corner_radius=12)
        card_res.grid(row=2, column=0, sticky="ew", pady=(0, 14))

        self.lbl_run_resultado = ctk.CTkLabel(
            card_res,
            text="RUN Completo: —",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_run_resultado.pack(side="left", padx=18, pady=16)

        self.btn_copiar_run = ctk.CTkButton(
            card_res,
            text="Copiar RUN",
            width=110,
            height=32,
            state="disabled",
            command=self._copiar_run,
        )
        self.btn_copiar_run.pack(side="right", padx=18, pady=16)

        self.lbl_run_db_status = ctk.CTkLabel(
            card_res,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#22C55E",
        )
        self.lbl_run_db_status.pack(side="right", padx=8, pady=16)

        # Historial SQLite
        historial_box = ctk.CTkFrame(self.frame_run, corner_radius=12)
        historial_box.grid(row=3, column=0, sticky="nsew")
        historial_box.grid_columnconfigure(0, weight=1)
        historial_box.grid_rowconfigure(1, weight=1)

        top_hist = ctk.CTkFrame(historial_box, fg_color="transparent")
        top_hist.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 6))

        ctk.CTkLabel(
            top_hist,
            text="Historial reciente en SQLite (historial_calculadora.db)",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(side="left")

        ctk.CTkButton(
            top_hist,
            text="Vaciar historial",
            width=115,
            height=28,
            fg_color="transparent",
            border_width=1,
            border_color="gray45",
            text_color=("gray15", "gray88"),
            hover_color=("gray85", "gray25"),
            command=self._vaciar_historial_run,
        ).pack(side="right")

        self.txt_historial_run = ctk.CTkTextbox(
            historial_box,
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
        )
        self.txt_historial_run.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 14))
        self.ultimo_run_formateado = ""

    def _calcular_run_gui(self):
        run_texto = self.entry_run.get().strip()
        try:
            dv = self.calculadora.obtener_dv(run_texto)
            run_limpio = run_texto.replace(".", "").replace("-", "")
            formateado = self.calculadora.formatear_run(run_limpio, dv)
            self.ultimo_run_formateado = formateado

            self.lbl_run_resultado.configure(text=f"RUN Completo: {formateado}")
            self.lbl_run_db_status.configure(text="✓ Guardado en SQLite")
            self.btn_copiar_run.configure(state="normal")
            self.entry_run.delete(0, "end")
            self._actualizar_lista_historial()
        except ValueError as err:
            messagebox.showerror("Error de validación", str(err))

    def _copiar_run(self):
        if not self.ultimo_run_formateado:
            return
        self.clipboard_clear()
        self.clipboard_append(self.ultimo_run_formateado)
        self.btn_copiar_run.configure(text="✓ ¡Copiado!")
        self.after(1500, lambda: self.btn_copiar_run.configure(text="Copiar RUN"))

    def _actualizar_lista_historial(self):
        registros = self.calculadora.obtener_historial(limite=30)
        self.txt_historial_run.configure(state="normal")
        self.txt_historial_run.delete("1.0", "end")

        if not registros:
            self.txt_historial_run.insert("1.0", "No hay registros guardados todavía.")
        else:
            lineas = []
            for reg_id, run_val, dv_val in registros:
                formateado = self.calculadora.formatear_run(run_val, dv_val)
                lineas.append(f"#{reg_id:<4} |  Sin puntos: {run_val}-{dv_val:<4} |  Formateado: {formateado}")
            self.txt_historial_run.insert("1.0", "\n".join(lineas))

        self.txt_historial_run.configure(state="disabled")

    def _vaciar_historial_run(self):
        if messagebox.askyesno(
            "Confirmar", "¿Deseas eliminar todos los registros del historial SQLite?"
        ):
            self.calculadora.limpiar_historial()
            self._actualizar_lista_historial()

    # ------------------------------------------------------------------
    # VISTA 3: GENERADOR DE CÓDIGO QR CON VISTA PREVIA
    # ------------------------------------------------------------------
    def _crear_vista_qr(self):
        self.frame_qr = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        self.frame_qr.grid_columnconfigure(0, weight=1)
        self.frame_qr.grid_rowconfigure(2, weight=1)

        # Cabecera
        header = ctk.CTkFrame(self.frame_qr, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        ctk.CTkLabel(
            header,
            text="Generador de Código QR",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Convierte enlaces o texto en un código QR con vista previa instantánea y exportación PNG.",
            font=ctk.CTkFont(size=13),
            text_color="gray65",
        ).pack(anchor="w")

        # Barra de entrada
        controles = ctk.CTkFrame(self.frame_qr, corner_radius=12)
        controles.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        controles.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            controles, text="Texto / URL:", font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, padx=(16, 10), pady=16)

        self.entry_qr_texto = ctk.CTkEntry(
            controles,
            placeholder_text="https://github.com/vicenterc-dev",
            height=36,
        )
        self.entry_qr_texto.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=16)
        self.entry_qr_texto.bind("<Return>", lambda _: self._generar_vista_previa_qr())

        ctk.CTkButton(
            controles,
            text="Generar QR",
            width=120,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._generar_vista_previa_qr,
        ).grid(row=0, column=2, padx=(0, 16), pady=16)

        # Tarjeta central de vista previa
        preview_card = ctk.CTkFrame(self.frame_qr, corner_radius=12)
        preview_card.grid(row=2, column=0, sticky="nsew")

        self.lbl_qr_preview = ctk.CTkLabel(
            preview_card,
            text="Escribe un texto arriba y presiona 'Generar QR'\npara ver la vista previa aquí.",
            font=ctk.CTkFont(size=13),
            text_color="gray60",
            width=260,
            height=260,
        )
        self.lbl_qr_preview.pack(expand=True, pady=(24, 12))

        self.btn_guardar_qr = ctk.CTkButton(
            preview_card,
            text="💾 Guardar imagen PNG...",
            width=200,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled",
            command=self._guardar_qr_png,
        )
        self.btn_guardar_qr.pack(pady=(0, 24))

    def _generar_vista_previa_qr(self):
        texto = self.entry_qr_texto.get().strip()
        if not texto:
            messagebox.showwarning("Dato vacío", "Ingresa un texto o enlace para generar el QR.")
            return

        try:
            qr_obj, imagen_pil = self.generador.crear_imagen_qr(texto, scale=8)
            self.qr_actual = qr_obj
            self.qr_ctk_image = ctk.CTkImage(
                light_image=imagen_pil,
                dark_image=imagen_pil,
                size=(250, 250),
            )
            self.lbl_qr_preview.configure(image=self.qr_ctk_image, text="")
            self.btn_guardar_qr.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Error al generar QR", str(e))

    def _guardar_qr_png(self):
        if self.qr_actual is None:
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar Código QR",
            defaultextension=".png",
            initialfile="codigo_qr.png",
            filetypes=[("Imagen PNG", "*.png")],
        )
        if not ruta:
            return

        try:
            self.qr_actual.png(ruta, scale=12)
            messagebox.showinfo("Guardado", f"Código QR guardado correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
