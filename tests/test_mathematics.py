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
        with self.assertRaises(ValueError):
            aritmetica.sumar()
        with self.assertRaises(ValueError):
            aritmetica.dividir()
        with self.assertRaises(ValueError):
            aritmetica.dividir(5)
        with self.assertRaises(ZeroDivisionError):
            aritmetica.dividir(5, 0)
        with self.assertRaises(ZeroDivisionError):
            aritmetica.modulo(5, 0)
        with self.assertRaises(ValueError):
            aritmetica.sumar(float("inf"))

    def test_potencias_raices_y_factorial_en_limites(self):
        self.assertEqual(aritmetica.potencia(0, 0), 1)
        self.assertEqual(aritmetica.raiz(0, 3), 0)
        self.assertAlmostEqual(aritmetica.raiz(-27, 3), -3)
        self.assertEqual(aritmetica.factorial(0), 1)

        with self.assertRaises(ZeroDivisionError):
            aritmetica.potencia(0, -1)
        with self.assertRaises(ValueError):
            aritmetica.potencia(-1, 0.5)
        with self.assertRaises(ValueError):
            aritmetica.raiz(-16, 2)
        with self.assertRaises(ValueError):
            aritmetica.raiz(16, 0)
        with self.assertRaises(TypeError):
            aritmetica.raiz(16, True)
        with self.assertRaises(ValueError):
            aritmetica.factorial(-1)
        with self.assertRaises(TypeError):
            aritmetica.factorial(3.0)

    def test_divisibilidad_promedios_y_redondeo_validan_entradas(self):
        for funcion in (aritmetica.mcd, aritmetica.mcm):
            with self.subTest(funcion=funcion.__name__):
                with self.assertRaises(ValueError):
                    funcion(5)
                with self.assertRaises(TypeError):
                    funcion(5, True)

        self.assertEqual(aritmetica.promedio(iter([2, 4])), 3)
        with self.assertRaises(ValueError):
            aritmetica.promedio([])
        with self.assertRaises(TypeError):
            aritmetica.promedio("123")
        with self.assertRaises(TypeError):
            aritmetica.promedio([1, False])
        with self.assertRaises(TypeError):
            aritmetica.redondear(1.2, True)
        with self.assertRaises(ValueError):
            aritmetica.truncar(float("inf"))


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

    def test_gramatica_permitida_y_funciones_matematicas(self):
        from edulib.mathematics import algebra

        self.assertEqual(algebra.evaluar_expresion("sin(pi / 2)"), 1)
        self.assertEqual(algebra.evaluar_expresion("sqrt(9)"), 3)
        self.assertEqual(algebra.evaluar_expresion("abs(-4)"), 4)
        self.assertEqual(algebra.simplificar_expresion("E**0"), 1)

    def test_parser_rechaza_sintaxis_no_permitida_y_entradas_complejas(self):
        from edulib.mathematics import algebra

        expresiones_invalidas = (
            "x.__class__",
            "[x for x in (1,)]",
            "lambda: 1",
            "unknown_function(x)",
            "sin(x, y)",
            "sin(x, extra=1)",
            "x % 2",
            "oo",
            "1e999",
            "__import__('os')",
            "__import__('builtins').print('UNSAFE')",
        )
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            for expresion in expresiones_invalidas:
                with self.subTest(expresion=expresion):
                    with self.assertRaises(ValueError):
                        algebra.simplificar_expresion(expresion)
        self.assertEqual(salida.getvalue(), "")

        with self.assertRaises(ValueError):
            algebra.simplificar_expresion("x" * 1001)
        with self.assertRaises(ValueError):
            algebra.simplificar_expresion(" + ".join(["x"] * 101))
        with self.assertRaises(ValueError):
            algebra.simplificar_expresion("-" * 51 + "x")

    def test_parser_rechaza_exponentes_numericos_excesivos(self):
        from edulib.mathematics import algebra

        with self.assertRaises(ValueError):
            algebra.simplificar_expresion("9**999999999")
        with self.assertRaises(ValueError):
            algebra.elevar_expresion("x", 1001)

    def test_expansion_rechaza_complejidad_combinatoria(self):
        from edulib.mathematics import algebra

        variables = " + ".join(f"x{indice}" for indice in range(30))
        expresion = f"({variables})**100"
        with self.assertRaisesRegex(ValueError, "términos"):
            algebra.expandir_expresion(expresion)


if __name__ == "__main__":
    unittest.main()
