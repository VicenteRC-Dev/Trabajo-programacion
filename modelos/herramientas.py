import time
import random
import string
import webbrowser as web
import pyqrcode
from colorama import Fore
from faker import Faker
import os
from modelos.calculadora_run import CalculadoraRUN

def colores():
    a = Fore.YELLOW
    r = Fore.RED
    v = Fore.GREEN
    m = Fore.MAGENTA
    c = Fore.CYAN
    z = Fore.BLUE
    g = Fore.LIGHTBLACK_EX
    
    reset = Fore.RESET
    
    return a, r, v, m, c, z, g, reset

a, r, v, m, c, z, g, reset = colores()
class Herramientas:
    def __init__(self):
        self.fake = Faker()
        self.calculadora = CalculadoraRUN()
        self.logo = f"""
{z}╔{g}══════════════════════════════════════════════════════════════════════════{z}╗
{a}║                                                                          ║
{a}║                                 {g}^~^  {a},{a}                                   ║
{a}║                                {g}({a}'{g}Y{a}'{g}) ){a}                                   ║
{a}║                                {g}/   \/{c}  {a}KDZ{c}  {g}__QQ{a}                         ║
{a}║                               {g}(\|||/){c}      {g}(_)_">{a}                        ║
{a}║                                           {g}/{a}                              ║
{a}║                                                                          ║
{a}║                                                                          ║
{a}║                        {r}Herramientas y generadores.{a}                       ║
{a}║                                   {g}v2.0                                   {a}║
{a}║                                 {g}2023/2026{a}                                ║
{a}║                                                                          ║
{z}╚{g}══════════════════════════════════════════════════════════════════════════{z}╝{reset}
"""
    def limpiar_pantalla(self):
        os.system("cls" if os.name == "nt" else "clear")

    def menu_principal(self):
        while True:
            self.limpiar_pantalla()
            print(self.logo)
            print("Recuerda usar [s/n] o seguir las instrucciones al generar algo!\n")
            print("    [1] Generadores fakes.")
            print("    [2] Herramientas (Incluye Calculadora RUN con SQL).")
            print("    [3] Apoyar al creador.")
            print("    [4] Salir.")
            
            opcion = input("\n>> ").strip()
            
            if opcion == '1':
                self.menu_generadores()
            elif opcion == '2':
                self.menu_herramientas()
            elif opcion == '3':
                web.open("https://github.com/vicenterc-dev")
                time.sleep(2)
            elif opcion == '4':
                self.limpiar_pantalla()
                print("¡Adiós!")
                break
            else:
                print("No existe esa opción XD")
                time.sleep(2)

    def menu_generadores(self):
        while True:
            self.limpiar_pantalla()
            print(self.logo)
            print("    [1] Generador de IPs.")
            print("    [2] Generador de nombres.")
            print("    [3] Generador de user-agents fakes.")
            print("    [4] Generador de direcciones fakes.")
            print("    [5] Generador de tarjetas fakes.")
            print("    [6] Generador de numeros fakes.")
            print("    [7] Regresar.")
            
            opcion = input("\n>> ").strip()
            
            if opcion == '1':
                self.generar_ips()
            elif opcion == '2':
                self.generar_nombres()
            elif opcion == '3':
                self.generar_user_agents()
            elif opcion == '4':
                self.generar_direcciones()
            elif opcion == '5':
                self.menu_tarjetas()
            elif opcion == '6':
                self.generar_telefonos()
            elif opcion == '7':
                break

    def _pedir_cantidad(self):
        print(self.logo)
        try:
            return int(input("Ingresa una cantidad: "))
        except ValueError:
            print("Cantidad inválida.")
            time.sleep(1)
            return 0

    def generar_ips(self):
        self.limpiar_pantalla()
        cantidad = self._pedir_cantidad()
        if cantidad <= 0: return
        print()
        for _ in range(cantidad):
            print(f"====> {self.fake.ipv4()}")
            time.sleep(0.2)
        
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_ips()

    def generar_nombres(self):
        self.limpiar_pantalla()
        cantidad = self._pedir_cantidad()
        if cantidad <= 0: return
        print()
        for _ in range(cantidad):
            print(f"====> {self.fake.name()}")
            time.sleep(0.2)
            
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_nombres()

    def generar_user_agents(self):
        self.limpiar_pantalla()
        cantidad = self._pedir_cantidad()
        if cantidad <= 0: return
        print()
        for _ in range(cantidad):
            ww = "".join(random.choices(string.digits, k=10))
            Faker.seed(ww)
            print(self.fake.user_agent())
            print()
            time.sleep(0.2)
            
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_user_agents()

    def generar_direcciones(self):
        self.limpiar_pantalla()
        cantidad = self._pedir_cantidad()
        if cantidad <= 0: return
        print()
        for _ in range(cantidad):
            pq = "".join(random.choices(string.digits, k=10))
            Faker.seed(pq)
            print(self.fake.address())
            print()
            time.sleep(0.2)
            
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_direcciones()

    def menu_tarjetas(self):
        while True:
            self.limpiar_pantalla()
            print(f"""
{self.logo}
    [1] Visa
    [2] MasterCard
    [3] Regresar
""")
            op = input(">> ").strip()
            if op == '1':
                self.generar_visa()
            elif op == '2':
                self.generar_mastercard()
            elif op == '3':
                break

    def generar_visa(self):
        self.limpiar_pantalla()
        cantidad = self._pedir_cantidad()
        if cantidad <= 0: return
        rip = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        
        for _ in range(cantidad):
            qq = "".join(random.choices(string.digits, k=15))
            qw = random.choice(rip)
            pqpq = "".join(random.choices(string.digits, k=3))
            qr = random.randint(24, 30)
            wqwq = self.fake.street_address()
            yt = self.fake.name()
            print(f"""
Marca: visa
Numero: 4{qq}
Titular: {yt}
Vencimiento: {qw}/20{qr}
Direccion: {wqwq}
CCV: {pqpq}
""")
            time.sleep(0.2)
            
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_visa()

    def generar_mastercard(self):
        self.limpiar_pantalla()
        cantidad = self._pedir_cantidad()
        if cantidad <= 0: return
        rip = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        for _ in range(cantidad):
            qq = random.randint(51, 55)
            oo = "".join(random.choices(string.digits, k=14))
            yt = "".join(random.choices(string.digits, k=3))
            tr = random.randint(24, 30)
            pq = self.fake.name()
            er = random.choice(rip)
            uy = self.fake.street_address()
            print(f"""
Marca: MasterCard
Numero: {qq}{oo}
Titular: {pq}
Vencimiento: {er}/20{tr}
direccion: {uy}
CVV: {yt}
""")
            time.sleep(0.2)
            
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_mastercard()


    def generar_telefonos(self):
        while True:
            self.limpiar_pantalla()
            print(self.logo)

            print("""
             Menú para elegir el país
    Seleccione el país para generar los números

    [1] Chile
    [2] España
    [3] Perú
    [4] Colombia
    [5] Aleatorio (Mezclados)
    [6] Salir
        """)

            opcion = input("Elige una opción: ").strip()

            opciones_validas = {
            "1": "Chile",
            "2": "España",
            "3": "Perú",
            "4": "Colombia",
            "5": "Aleatorio",
            "6": "salir"
            }

            if opcion not in opciones_validas:
                print("\nOpción no válida.")
                time.sleep(1.5)
                continue

            pais_elegido = opciones_validas[opcion]
            self.limpiar_pantalla()

            if pais_elegido == "salir":
                self.menu_generadores()
                return

            cantidad = self._pedir_cantidad()

            if cantidad <= 0:
                continue

            print(f"\nGenerando {cantidad} número(s) para {pais_elegido}:\n")

            paises_disponibles = [
            "Chile",
            "España",
            "Perú",
            "Colombia"
            ]

            for _ in range(cantidad):

                pais_actual = (
                    random.choice(paises_disponibles)
                    if pais_elegido == "Aleatorio"
                    else pais_elegido
                )

                if pais_actual == "Chile":
                    numero = (
                        f"+56 9 {random.randint(1000, 9999)} "
                        f"{random.randint(1000, 9999)}"
                    )

                elif pais_actual == "España":
                    inicio = random.choice([6, 7])
                    numero = (
                        f"+34 {inicio}{random.randint(10, 99)} "
                        f"{random.randint(100, 999)} "
                        f"{random.randint(100, 999)}"
                    )

                elif pais_actual == "Perú":
                    numero = (
                        f"+51 9{random.randint(10, 99)} "
                        f"{random.randint(100, 999)} "
                        f"{random.randint(100, 999)}"
                    )

                elif pais_actual == "Colombia":
                    numero = (
                        f"+57 3{random.randint(0, 5)}"
                        f"{random.randint(0, 9)} "
                        f"{random.randint(100, 999)} "
                        f"{random.randint(1000, 9999)}"
                    )

                print(f"{pais_actual}: {numero}")
                time.sleep(0.1)

            print("\nGeneración completada.")
            while True:
                volver = input(
                    "\n¿Deseas volver a generar números? (S/N): "
                ).strip().lower()

                if volver in ("s", "si", "sí"):
                    break

                elif volver in ("n", "no"):
                    self.menu_generadores()
                    return

                else:
                    print("Respuesta no válida. Escribe S o N.")


    def menu_herramientas(self):
        while True:
            self.limpiar_pantalla()
            print(f"""
{self.logo}
    [1] Calculadora de RUN (Con Persistencia SQL)
    [2] De texto a codigo qr.
    [3] Regresar.
""")
            dd = input(">> ").strip()
            if dd == '1':
                self.ejecutar_calculadora_run()
            elif dd == '2':
                self.generar_qr()
            elif dd == '3':
                break

    def ejecutar_calculadora_run(self):
        self.limpiar_pantalla()
        print(self.logo)
        print("=== Calculadora de Dígito Verificador (RUN) con SQLite ===")
        print("Ingresa 'salir' para regresar.\n")
        
        while True:
            run_input = input("Ingresa el RUN sin dígito verificador: ").strip()
            if run_input.lower() == 'salir':
                break
            try:
                dv = self.calculadora.obtener_dv(run_input)
                print(f"-> RUN Completo: {run_input}-{dv}")
                print("[✓] Guardado en la base de datos SQLite correctamente.\n")
            except ValueError as error:
                print(f"Error: {error}\n")

    def generar_qr(self):
        self.limpiar_pantalla()
        print(self.logo)
        s_text = input('Ingresa un texto: ').strip()
        n_img = input('Ingresa el nombre de la imagen: ').strip()
        
        if not s_text or not n_img:
            print("Datos incompletos.")
            time.sleep(1.5)
            return
            
        d = f"{n_img}.png"
        try:
            url = pyqrcode.create(s_text)
            url.png(d, scale=60)
            print(f"[✓] QR guardado como '{d}'")
            try:
                url.show()
            except Exception:
                pass
        except Exception as e:
            print(f"Error al generar QR: {e}")
            
        if input("Deseas volver a generar?: ").lower().strip() == "s":
            self.generar_qr()