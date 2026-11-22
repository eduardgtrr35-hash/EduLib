try:
    import sympy as sp
except ImportError:
    sp = None


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
def _convertir_expresion(expresion, nombre="expresion"):
    """Convierte una entrada válida en una expresión simbólica."""

    _verificar_sympy()

    if isinstance(expresion, bool):
        raise TypeError(f"{nombre} no puede ser un valor booleano.")

    if isinstance(expresion, str):
        if not expresion.strip():
            raise ValueError(f"{nombre} no puede estar vacío.")

    elif not isinstance(expresion, (sp.Basic, int, float)):
        raise TypeError(
            f"{nombre} debe ser una cadena, un número o una expresión simbólica."
        )

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

    return print(resultado.subs(sustituciones_convertidas))
def simplificar_expresion(expresion):
    """Simplifica una expresión algebraica."""

    expresion = _convertir_expresion(expresion)

    return print(sp.simplify(expresion))
def expandir_expresion(expresion):
    """Desarrolla productos y potencias algebraicas."""

    expresion = _convertir_expresion(expresion)

    return  print(sp.expand(expresion))
def factorizar_expresion(expresion):
    """Factoriza una expresión algebraica."""

    expresion = _convertir_expresion(expresion)

    return print(sp.factor(expresion))
def sustituir_variable(expresion, variable, valor):
    """
    Sustituye una variable por un valor o expresión.

    Ejemplo:
        sustituir_variable("x**2 + 3*x", "x", 2) -> 10
    """

    expresion = _convertir_expresion(expresion)
    simbolo = _convertir_variable(variable)
    valor = _convertir_expresion(valor, "valor")

    return print(expresion.subs(simbolo, valor))

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

    return print(sorted(
        [str(variable) for variable in variables]
    ))
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

    return print(int(grado))

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

    return print(sp.expand(sum(expresiones)))
def restar_expresiones(a, b):
    """Resta una expresión algebraica de otra."""

    a = _convertir_expresion(a, "a")
    b = _convertir_expresion(b, "b")

    return print(sp.expand(a - b))
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

    return print(sp.expand(resultado))
def dividir_expresiones(a, b):
    """Divide una expresión algebraica entre otra."""

    a = _convertir_expresion(a, "a")
    b = _convertir_expresion(b, "b")

    if b == 0:
        raise ZeroDivisionError(
            "No se puede dividir entre una expresión igual a cero."
        )

    return print(sp.cancel(a / b))
def elevar_expresion(base, exponente):
    """Eleva una expresión algebraica a una potencia."""

    base = _convertir_expresion(base, "base")
    exponente = _convertir_expresion(exponente, "exponente")

    return print(sp.expand(base ** exponente))

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

    return print(list(sp.Add.make_args(sp.expand(expresion))))
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

    return print(polinomio.all_coeffs())