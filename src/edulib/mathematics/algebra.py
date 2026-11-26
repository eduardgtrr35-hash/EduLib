import ast
import math

try:
    import sympy as sp
except ImportError:
    sp = None

_MAXIMO_EXPONENTE_NUMERICO = 1000
_MAXIMO_TERMINOS_EXPANSION = 10_000


# ==========================================
# VALIDACIONES INTERNAS
# ==========================================

def _verificar_sympy():
    """Comprueba que SymPy esté instalado."""

    if sp is None:
        raise ImportError(
            "Esta función requiere SymPy. "
            "Instálalo con: python -m pip install sympy"
        )


def _validar_limite_exponente(exponente, nombre):
    """Evita exponentes numéricos que puedan disparar cálculos excesivos."""

    if not exponente.is_number:
        return

    try:
        exponente_excesivo = bool(
            sp.Abs(exponente) > _MAXIMO_EXPONENTE_NUMERICO
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{nombre} contiene un exponente numérico no válido."
        ) from error

    if exponente_excesivo:
        raise ValueError(
            f"{nombre} excede el exponente máximo permitido "
            f"({_MAXIMO_EXPONENTE_NUMERICO})."
        )


def _estimar_terminos_expansion(expresion):
    """Estima de forma conservadora los términos de una expansión algebraica."""

    nodos_visitados = 0
    limite = _MAXIMO_TERMINOS_EXPANSION

    def estimar(nodo, profundidad=0):
        nonlocal nodos_visitados
        nodos_visitados += 1
        if nodos_visitados > 5000 or profundidad > 100:
            return limite + 1

        if nodo.is_Add:
            total = 0
            for termino in nodo.args:
                total += estimar(termino, profundidad + 1)
                if total > limite:
                    return limite + 1
            return max(total, 1)

        if nodo.is_Mul:
            total = 1
            for factor in nodo.args:
                cantidad = estimar(factor, profundidad + 1)
                if cantidad > limite or total > limite // cantidad:
                    return limite + 1
                total *= cantidad
            return total

        if nodo.is_Pow:
            exponente = nodo.exp
            if exponente.is_Integer and exponente.is_nonnegative:
                potencia = int(exponente)
                if potencia == 0:
                    return 1

                terminos_base = estimar(nodo.base, profundidad + 1)
                if terminos_base > limite:
                    return limite + 1
                if terminos_base <= 1:
                    return 1
                if potencia >= limite:
                    return limite + 1

                return min(
                    math.comb(terminos_base + potencia - 1, potencia),
                    limite + 1,
                )

        return 1

    return estimar(expresion)


def _validar_complejidad_expansion(expresion, nombre):
    """Rechaza expansiones cuya cantidad estimada de términos sea excesiva."""

    estimacion = _estimar_terminos_expansion(expresion)
    if estimacion > _MAXIMO_TERMINOS_EXPANSION:
        raise ValueError(
            f"{nombre} produciría más de "
            f"{_MAXIMO_TERMINOS_EXPANSION} términos al expandirse."
        )


def _convertir_expresion(expresion, nombre="expresion"):
    """Convierte una entrada válida en una expresión simbólica."""

    _verificar_sympy()

    if isinstance(expresion, bool):
        raise TypeError(f"{nombre} no puede ser un valor booleano.")

    if isinstance(expresion, str):
        if not expresion.strip():
            raise ValueError(f"{nombre} no puede estar vacío.")

        if len(expresion) > 1000:
            raise ValueError(f"{nombre} excede el límite de longitud permitido.")

        resultado = _analizar_expresion(expresion, nombre)

    elif not isinstance(expresion, (sp.Basic, int, float)):
        raise TypeError(
            f"{nombre} debe ser una cadena, un número o una expresión simbólica."
        )
    else:
        try:
            resultado = sp.sympify(expresion)
        except (sp.SympifyError, SyntaxError, TypeError, ValueError) as error:
            raise ValueError(
                f"No se pudo interpretar {nombre}."
            ) from error

    if resultado.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        raise ValueError(
            f"{nombre} contiene valores matemáticos no válidos."
        )

    return resultado


def _analizar_expresion(texto, nombre):
    """Analiza una expresión con una gramática matemática permitida."""

    funciones = {
        "sqrt": (sp.sqrt, 1),
        "sin": (sp.sin, 1),
        "cos": (sp.cos, 1),
        "tan": (sp.tan, 1),
        "asin": (sp.asin, 1),
        "acos": (sp.acos, 1),
        "atan": (sp.atan, 1),
        "sinh": (sp.sinh, 1),
        "cosh": (sp.cosh, 1),
        "tanh": (sp.tanh, 1),
        "exp": (sp.exp, 1),
        "log": (sp.log, (1, 2)),
        "Abs": (sp.Abs, 1),
        "abs": (sp.Abs, 1),
    }
    constantes = {"pi": sp.pi, "E": sp.E, "I": sp.I}
    nombres_no_finitos = {"oo", "zoo", "nan", "inf", "Infinity"}
    operadores = {
        ast.Add: lambda izquierda, derecha: izquierda + derecha,
        ast.Sub: lambda izquierda, derecha: izquierda - derecha,
        ast.Mult: lambda izquierda, derecha: izquierda * derecha,
        ast.Div: lambda izquierda, derecha: izquierda / derecha,
        ast.Pow: lambda izquierda, derecha: izquierda ** derecha,
    }

    try:
        arbol = ast.parse(texto, mode="eval")
    except (SyntaxError, ValueError, RecursionError) as error:
        raise ValueError(f"No se pudo interpretar {nombre}.") from error

    nodos_visitados = 0

    def convertir(nodo, profundidad=0):
        nonlocal nodos_visitados
        nodos_visitados += 1
        if nodos_visitados > 200 or profundidad > 50:
            raise ValueError(f"{nombre} excede la complejidad permitida.")

        if isinstance(nodo, ast.Expression):
            return convertir(nodo.body, profundidad + 1)

        if isinstance(nodo, ast.Constant):
            valor = nodo.value
            if isinstance(valor, bool) or not isinstance(valor, (int, float, complex)):
                raise ValueError(f"{nombre} contiene un valor no permitido.")
            if isinstance(valor, float) and not math.isfinite(valor):
                raise ValueError(f"{nombre} debe contener números finitos.")
            if isinstance(valor, complex) and not (
                math.isfinite(valor.real) and math.isfinite(valor.imag)
            ):
                raise ValueError(f"{nombre} debe contener números finitos.")
            return sp.sympify(valor)

        if isinstance(nodo, ast.Name):
            if nodo.id in nombres_no_finitos:
                raise ValueError(f"{nombre} contiene valores matemáticos no válidos.")
            if nodo.id in constantes:
                return constantes[nodo.id]
            if nodo.id in funciones:
                raise ValueError(
                    f"La función {nodo.id} debe llamarse con argumentos explícitos."
                )
            return sp.Symbol(nodo.id)

        if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, (ast.UAdd, ast.USub)):
            valor = convertir(nodo.operand, profundidad + 1)
            return valor if isinstance(nodo.op, ast.UAdd) else -valor

        if isinstance(nodo, ast.BinOp):
            operacion = operadores.get(type(nodo.op))
            if operacion is None:
                raise ValueError(f"{nombre} contiene un operador no permitido.")
            izquierda = convertir(nodo.left, profundidad + 1)
            derecha = convertir(nodo.right, profundidad + 1)
            if isinstance(nodo.op, ast.Pow) and derecha.is_number:
                _validar_limite_exponente(derecha, nombre)
            return operacion(izquierda, derecha)

        if isinstance(nodo, ast.Call):
            if not isinstance(nodo.func, ast.Name) or nodo.func.id not in funciones:
                raise ValueError(f"{nombre} contiene una función no permitida.")
            if nodo.keywords:
                raise ValueError(f"{nombre} no admite argumentos nombrados.")
            funcion, cantidad = funciones[nodo.func.id]
            cantidades_validas = (
                cantidad if isinstance(cantidad, tuple) else (cantidad,)
            )
            if len(nodo.args) not in cantidades_validas:
                raise ValueError(
                    f"La función {nodo.func.id} recibió una cantidad de argumentos no válida."
                )
            argumentos = [convertir(arg, profundidad + 1) for arg in nodo.args]
            return funcion(*argumentos)

        raise ValueError(f"{nombre} contiene una construcción no permitida.")

    try:
        return convertir(arbol)
    except (SyntaxError, TypeError, ValueError, RecursionError) as error:
        if isinstance(error, ValueError) and str(error).startswith(nombre):
            raise
        raise ValueError(f"No se pudo interpretar {nombre}: {error}") from error
def _convertir_variable(variable):
    """Convierte el nombre de una variable en un símbolo."""

    _verificar_sympy()

    if isinstance(variable, sp.Symbol):
        return variable

    if not isinstance(variable, str):
        raise TypeError("La variable debe ser una cadena o un símbolo.")

    if not variable.strip() or not variable.isidentifier():
        raise ValueError("El nombre de la variable no es válido.")

    return sp.Symbol(variable)

# ==========================================
# EVALUACIÓN Y TRANSFORMACIÓN
# ==========================================
def evaluar_expresion(expresion, valores=None, **variables):
    """
    Evalúa una expresión sustituyendo sus variables.

    Ejemplos:
        evaluar_expresion("x + 5", {"x": 3}) -> 8
        evaluar_expresion("x**2 + y", x=2, y=4) -> 8
    """

    resultado = _convertir_expresion(expresion)

    sustituciones = {}

    if valores is not None:
        if not isinstance(valores, dict):
            raise TypeError("valores debe ser un diccionario.")

        sustituciones.update(valores)

    sustituciones.update(variables)

    sustituciones_convertidas = {}

    for variable, valor in sustituciones.items():
        simbolo = _convertir_variable(variable)
        valor_convertido = _convertir_expresion(valor, "valor")
        sustituciones_convertidas[simbolo] = valor_convertido

    return resultado.subs(sustituciones_convertidas)
def simplificar_expresion(expresion):
    """Simplifica una expresión algebraica."""

    expresion = _convertir_expresion(expresion)

    return sp.simplify(expresion)
def expandir_expresion(expresion):
    """Desarrolla productos y potencias algebraicas."""

    expresion = _convertir_expresion(expresion)
    _validar_complejidad_expansion(expresion, "La expresión")

    return sp.expand(expresion)
def factorizar_expresion(expresion):
    """Factoriza una expresión algebraica."""

    expresion = _convertir_expresion(expresion)

    return sp.factor(expresion)
def sustituir_variable(expresion, variable, valor):
    """
    Sustituye una variable por un valor o expresión.

    Ejemplo:
        sustituir_variable("x**2 + 3*x", "x", 2) -> 10
    """

    expresion = _convertir_expresion(expresion)
    simbolo = _convertir_variable(variable)
    valor = _convertir_expresion(valor, "valor")

    return expresion.subs(simbolo, valor)

# ==========================================
# ANÁLISIS DE EXPRESIONES
# ==========================================
def identificar_variables(expresion):
    """
    Identifica las variables de una expresión.

    Devuelve una lista de nombres ordenados alfabéticamente.
    """

    expresion = _convertir_expresion(expresion)

    variables = expresion.free_symbols

    return sorted(
        [str(variable) for variable in variables]
    )
def grado_expresion(expresion, variable=None):
    """
    Obtiene el grado de una expresión respecto a una variable.

    Si no se especifica la variable, la expresión debe
    contener como máximo una variable.

    Ejemplos:
        grado_expresion("3*x**4 + 2*x") -> 4
        grado_expresion("x**2 + y**3", "y") -> 3
    """

    expresion = _convertir_expresion(expresion)

    if variable is None:
        variables = expresion.free_symbols

        if len(variables) > 1:
            raise ValueError(
                "La expresión contiene varias variables. "
                "Debes especificar una."
            )

        if len(variables) == 0:
            return 0

        variable = next(iter(variables))

    else:
        variable = _convertir_variable(variable)

    try:
        grado = sp.degree(expresion, variable)

    except sp.PolynomialError as error:
        raise ValueError(
            "No se pudo determinar el grado polinómico."
        ) from error

    if grado is sp.S.NegativeInfinity:
        raise ValueError(
            "El grado de la expresión cero no está definido."
        )

    return int(grado)

# ==========================================
# OPERACIONES ENTRE EXPRESIONES
# ==========================================
def sumar_expresiones(*expresiones):
    """Suma dos o más expresiones algebraicas."""

    if len(expresiones) < 2:
        raise ValueError(
            "Debes proporcionar al menos dos expresiones."
        )

    expresiones = [
        _convertir_expresion(expresion)
        for expresion in expresiones
    ]

    resultado = sum(expresiones)
    _validar_complejidad_expansion(resultado, "La suma")
    return sp.expand(resultado)
def restar_expresiones(a, b):
    """Resta una expresión algebraica de otra."""

    a = _convertir_expresion(a, "a")
    b = _convertir_expresion(b, "b")

    resultado = a - b
    _validar_complejidad_expansion(resultado, "La resta")
    return sp.expand(resultado)
def multiplicar_expresiones(*expresiones):
    """Multiplica dos o más expresiones algebraicas."""

    if len(expresiones) < 2:
        raise ValueError(
            "Debes proporcionar al menos dos expresiones."
        )

    expresiones = [
        _convertir_expresion(expresion)
        for expresion in expresiones
    ]

    resultado = sp.prod(expresiones)
    _validar_complejidad_expansion(resultado, "El producto")

    return sp.expand(resultado)
def dividir_expresiones(a, b):
    """Divide una expresión algebraica entre otra."""

    a = _convertir_expresion(a, "a")
    b = _convertir_expresion(b, "b")

    if b == 0:
        raise ZeroDivisionError(
            "No se puede dividir entre una expresión igual a cero."
        )

    return sp.cancel(a / b)
def elevar_expresion(base, exponente):
    """Eleva una expresión algebraica a una potencia."""

    base = _convertir_expresion(base, "base")
    exponente = _convertir_expresion(exponente, "exponente")
    _validar_limite_exponente(exponente, "exponente")
    resultado = base ** exponente
    _validar_complejidad_expansion(resultado, "La potencia")

    return sp.expand(resultado)

# ==========================================
# EXTRACCIÓN DE INFORMACIÓN
# ==========================================
def obtener_terminos(expresion):
    """
    Separa una expresión en sus términos.

    Ejemplo:
        obtener_terminos("3*x**2 + 5*x - 7")
    """

    expresion = _convertir_expresion(expresion)
    _validar_complejidad_expansion(expresion, "La expresión")

    return list(sp.Add.make_args(sp.expand(expresion)))
def coeficientes_polinomio(expresion, variable=None):
    """
    Obtiene los coeficientes de un polinomio.

    Los devuelve desde el término de mayor grado
    hasta el término independiente.
    """

    expresion = _convertir_expresion(expresion)

    if variable is None:
        variables = expresion.free_symbols

        if len(variables) != 1:
            raise ValueError(
                "Debes especificar una variable cuando "
                "la expresión no contiene exactamente una."
            )

        variable = next(iter(variables))

    else:
        variable = _convertir_variable(variable)

    try:
        polinomio = sp.Poly(expresion, variable)

    except sp.PolynomialError as error:
        raise ValueError(
            "La expresión no es un polinomio válido "
            "respecto a la variable indicada."
        ) from error

    return polinomio.all_coeffs()
