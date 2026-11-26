import contextlib
import inspect
import io
import unittest
from unittest.mock import call, patch

from edulib.text import prints


class VelocidadesImpresionTests(unittest.TestCase):
    def test_velocidades_predeterminadas_siguen_una_progresion(self):
        valores = {
            prints.print_ultra_rapido: 0.001,
            prints.print_super_rapido: 0.01,
            prints.print_rapido: 0.03,
            prints.print_medio: 0.1,
            prints.print_lento: 0.2,
            prints.print_super_lento: 0.4,
            prints.print_ultra_lento: 0.6,
        }

        for funcion, esperado in valores.items():
            with self.subTest(funcion=funcion.__name__):
                self.assertEqual(inspect.signature(funcion).parameters["velocidad"].default, esperado)

    def test_variantes_con_secuencia_comparten_tiempos_coherentes(self):
        valores = {
            prints.print_ultra_rapido_y_secuencia: 0.001,
            prints.print_super_rapido_y_secuencia: 0.01,
            prints.print_rapido_y_secuencia: 0.03,
            prints.print_medio_y_secuencia: 0.1,
            prints.print_lento_y_secuencia: 0.2,
            prints.print_super_lento_y_secuencia: 0.4,
            prints.print_ultra_lento_y_secuencia: 0.6,
        }

        for funcion, esperado in valores.items():
            with self.subTest(funcion=funcion.__name__):
                parametros = inspect.signature(funcion).parameters
                self.assertEqual(parametros["velocidad_texto"].default, esperado)
                self.assertEqual(parametros["velocidad"].default, 0.8)
                self.assertEqual(parametros["duracion_segundos"].default, 5)

        for funcion in (prints.animar_secuencia, prints.print_y_animar_secuencia):
            with self.subTest(funcion=funcion.__name__):
                parametros = inspect.signature(funcion).parameters
                self.assertEqual(parametros["velocidad"].default, 0.8)
                self.assertEqual(parametros["duracion_segundos"].default, 5)

    def test_velocidad_personalizada_no_espera_en_la_prueba(self):
        salida = io.StringIO()
        with patch("edulib.text.prints.time.sleep") as dormir:
            with contextlib.redirect_stdout(salida):
                prints.print_ultra_rapido("ok", velocidad=0, end="!")

        self.assertEqual(salida.getvalue(), "ok!")
        self.assertEqual(dormir.call_args_list, [call(0), call(0)])

    def test_tiempos_invalidos_se_rechazan_antes_de_imprimir(self):
        entradas_invalidas = (-0.1, float("nan"), float("inf"), True, "0.1")
        for velocidad in entradas_invalidas:
            salida = io.StringIO()
            with self.subTest(velocidad=velocidad):
                with contextlib.redirect_stdout(salida):
                    with self.assertRaises((TypeError, ValueError)):
                        prints.print_rapido("texto", velocidad=velocidad)
                self.assertEqual(salida.getvalue(), "")

        for argumentos in (
            {"velocidad": float("nan")},
            {"duracion_segundos": float("inf")},
            {"velocidad_texto": True},
        ):
            with self.subTest(argumentos=argumentos):
                with patch("edulib.text.prints.time.sleep"):
                    with contextlib.redirect_stdout(io.StringIO()):
                        with self.assertRaises((TypeError, ValueError)):
                            prints.print_y_animar_secuencia("texto", **argumentos)


if __name__ == "__main__":
    unittest.main()
