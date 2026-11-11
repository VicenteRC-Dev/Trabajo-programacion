import sqlite3
from pathlib import Path

class CalculadoraRUN:
    def __init__(self):
        self.__secuencia = [2, 3, 4, 5, 6, 7]
        self.db_path = Path(__file__).with_name("historial_calculadora.db")
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.db_path) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial_calculadora (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run TEXT NOT NULL,
                    dv TEXT NOT NULL
                )
            """)

    def guardar_en_bd(self, run: str, dv: str):
        with sqlite3.connect(self.db_path) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO historial_calculadora (run, dv) VALUES (?, ?)",
                (run, dv)
            )

    def __calcular_modulo_11(self, run_limpio: str) -> str:
        run_reverso = str(run_limpio)[::-1]
        suma = 0
        indice_secuencia = 0

        for digito in run_reverso:
            suma += int(digito) * self.__secuencia[indice_secuencia]
            indice_secuencia += 1
            if indice_secuencia == len(self.__secuencia):
                indice_secuencia = 0

        resto = suma % 11
        dv_esperado = 11 - resto

        if dv_esperado == 11: return '0'
        elif dv_esperado == 10: return 'K'
        else: return str(dv_esperado)

    def obtener_dv(self, run: str) -> str:
        run_limpio = str(run).replace(".", "").replace("-", "")
        if not run_limpio.isdigit():
            raise ValueError("El RUN debe contener solo números.")
        
        dv = self.__calcular_modulo_11(run_limpio)
        self.guardar_en_bd(run_limpio, dv)
        return dv