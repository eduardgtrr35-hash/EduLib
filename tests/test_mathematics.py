import contextlib
import io
import unittest

from edulib.mathematics import aritmetica


class AritmeticaTests(unittest.TestCase):
    def test_operaciones_devueltas_sin_imprimir(self):
        casos = (
            (aritmetica.sumar, (2, 3), 5),
            (aritmetica.restar, (10, 2, 3), 5),
            (aritmetica.multiplicar, (2, 3, 4), 24),
            (aritmetica.dividir, (20, 2, 5), 2),
            (aritmetica.potencia, (2, 3), 8),
            (aritmetica.raiz, (81, 4), 3),
            (aritmetica.modulo, (17, 5), 2),
            (aritmetica.valor_absoluto, (-4,), 4),
            (aritmetica.factorial, (5,), 120),
            (aritmetica.mcd, (12, 18), 6),
            (aritmetica.mcm, (4, 6), 12),
            (aritmetica.redondear, (3.14159, 2), 3.14),
            (aritmetica.truncar, (3.9,), 3),
            (aritmetica.promedio, ([2, 4, 6],), 4),
        )
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            for funcion, argumentos, esperado in casos:
                with self.subTest(funcion=funcion.__name__):
                    self.assertEqual(funcion(*argumentos), esperado)
        self.assertEqual(salida.getvalue(), "")

    def test_modulo_exige_exactamente_dos_argumentos(self):
        for argumentos in ((), (5,), (5, 2, 1)):
            with self.subTest(argumentos=argumentos):
                with self.assertRaises(ValueError):
                    aritmetica.modulo(*argumentos)

    def test_validacion_numerica_y_division_por_cero(self):
        with self.assertRaises(TypeError):
            aritmetica.sumar(True, 1)
        with self.assertRaises(ZeroDivisionError):
            aritmetica.dividir(5, 0)
        with self.assertRaises(ZeroDivisionError):
            aritmetica.modulo(5, 0)


try:
    import sympy as sp
except ImportError:
    sp = None


@unittest.skipIf(sp is None, "SymPy es opcional; instala el extra 'math'.")
class AlgebraTests(unittest.TestCase):
    def test_funciones_algebraicas_devuelven_resultados(self):
        from edulib.mathematics import algebra

        x = sp.Symbol("x")
        casos = (
            (algebra.evaluar_expresion, ("x + 2",), {"x": 3}, sp.Integer(5)),
            (algebra.simplificar_expresion, ("x + x",), {}, 2 * x),
            (algebra.expandir_expresion, ("(x + 1)**2",), {}, x**2 + 2*x + 1),
            (algebra.factorizar_expresion, ("x**2 - 1",), {}, (x - 1)*(x + 1)),
            (algebra.sustituir_variable, ("x**2", "x", 3), {}, sp.Integer(9)),
            (algebra.grado_expresion, ("x**3 + 1",), {}, 3),
            (algebra.sumar_expresiones, ("x", "2*x"), {}, 3*x),
            (algebra.restar_expresiones, ("3*x", "x"), {}, 2*x),
            (algebra.multiplicar_expresiones, ("x + 1", "x - 1"), {}, x**2 - 1),
            (algebra.dividir_expresiones, ("x**2 - 1", "x - 1"), {}, x + 1),
            (algebra.elevar_expresion, ("x + 1", 2), {}, x**2 + 2*x + 1),
        )
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            for funcion, argumentos, keywords, esperado in casos:
                with self.subTest(funcion=funcion.__name__):
                    self.assertEqual(funcion(*argumentos, **keywords), esperado)
            self.assertEqual(algebra.identificar_variables("y + x"), ["x", "y"])
            self.assertEqual(algebra.obtener_terminos("x + 1"), [sp.Integer(1), x])
            self.assertEqual(algebra.coeficientes_polinomio("2*x**2 + 3*x"), [2, 3, 0])
        self.assertEqual(salida.getvalue(), "")

    def test_validacion_de_expresiones_y_division_por_cero(self):
        from edulib.mathematics import algebra

        with self.assertRaises(TypeError):
            algebra.evaluar_expresion("x", {True: 2})
        with self.assertRaises(ZeroDivisionError):
            algebra.dividir_expresiones("x", 0)


if __name__ == "__main__":
    unittest.main()
