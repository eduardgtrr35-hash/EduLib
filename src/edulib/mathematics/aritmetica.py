import math
from collections.abc import Iterable
from numbers import Real


# ==========================================
# VALIDACIONES INTERNAS
# ==========================================
def _validar_numero(numero, nombre="numero"):
    """Comprueba que el valor sea un número real válido."""

    if isinstance(numero, bool) or not isinstance(numero, Real):
        raise TypeError(f"{nombre} debe ser un número real.")

    if isinstance(numero, float) and not math.isfinite(numero):
        raise ValueError(f"{nombre} debe ser un número finito.")

    return numero
def _validar_entero(numero, nombre="numero"):
    """Comprueba que el valor sea un número entero."""

    if isinstance(numero, bool) or not isinstance(numero, int):
        raise TypeError(f"{nombre} debe ser un número entero.")

    return numero

# ==========================================
# OPERACIONES BÁSICAS
# ==========================================
def sumar(*numeros):
    """Suma dos o más números."""

    if not numeros:
        raise ValueError("Debes proporcionar al menos un número.")

    for numero in numeros:
        _validar_numero(numero)

    return print(sum(numeros))
def restar(*numeros):
    """Resta dos o más números."""

    if not numeros:
        raise ValueError("Debes proporcionar al menos un número.")

    for numero in numeros:
        _validar_numero(numero)

    return print(numeros[0] - sum(numeros[1:]))
def multiplicar(*numeros):
    """Multiplica dos o más números."""

    if not numeros:
        raise ValueError("Debes proporcionar al menos un número.")

    resultado = 1

    for numero in numeros:
        _validar_numero(numero)
        resultado *= numero

    return print(resultado)
def dividir(*numeros):
    """Divide dos o más números."""

    if not numeros:
        raise ValueError("Debes proporcionar al menos un número.")

    for numero in numeros:
        _validar_numero(numero)

    resultado = numeros[0]
    for numero in numeros[1:]:
        if numero == 0:
            raise ZeroDivisionError("No se puede dividir entre cero.")
        resultado /= numero

    return resultado

# ==========================================
# POTENCIAS Y RAÍCES
# ==========================================
def potencia(base, exponente):
    """Eleva una base a un exponente."""

    _validar_numero(base, "base")
    _validar_numero(exponente, "exponente")

    if base == 0 and exponente < 0:
        raise ZeroDivisionError(
            "Cero no puede elevarse a un exponente negativo."
        )

    resultado = base ** exponente

    if isinstance(resultado, complex):
        raise ValueError(
            "El resultado no pertenece a los números reales."
        )

    return print(resultado)
def raiz(numero, indice):
    """
    Calcula una raíz de cualquier índice entero positivo.

    Ejemplos:
        raiz(81, 4)       -> 3
        raiz(32, 5)       -> 2
        raiz(1024, 10)    -> 2
        raiz(-27, 3)      -> -3
    """

    _validar_numero(numero)
    _validar_entero(indice, "indice")

    if indice <= 0:
        raise ValueError("El índice debe ser un entero positivo.")

    if numero < 0:

        if indice % 2 == 0:
            raise ValueError(
                "No existe una raíz real de índice par para un número negativo."
            )

        return -((-numero) ** (1 / indice))

    return print(numero ** (1 / indice))

# ==========================================
# OPERACIONES ESPECIALES
# ==========================================
def modulo(*numeros):
    """Obtiene el residuo de una división."""

    if not numeros:
        raise ValueError("Debes proporcionar al menos un número.")

    for numero in numeros:
        _validar_numero(numero)

    if numeros[1] == 0:
        raise ZeroDivisionError(
            "No se puede calcular módulo entre cero."
        )

    return print(numeros[0] % numeros[1])
def valor_absoluto(numero):
    """Devuelve el valor absoluto de un número."""

    _validar_numero(numero)

    return print(abs(numero))
def factorial(numero):
    """Calcula el factorial de un entero no negativo."""

    _validar_entero(numero)

    if numero < 0:
        raise ValueError(
            "El factorial no admite números negativos."
        )

    return print(math.factorial(numero))

# ==========================================
# DIVISIBILIDAD
# ==========================================
def mcd(*numeros):
    """Calcula el máximo común divisor de dos o más enteros."""

    if len(numeros) < 2:
        raise ValueError(
            "Debes proporcionar al menos dos números."
        )

    for numero in numeros:
        _validar_entero(numero)

    return print(math.gcd(*numeros))
def mcm(*numeros):
    """Calcula el mínimo común múltiplo de dos o más enteros."""

    if len(numeros) < 2:
        raise ValueError(
            "Debes proporcionar al menos dos números."
        )

    for numero in numeros:
        _validar_entero(numero)

    return print(math.lcm(*numeros))

# ==========================================
# REDONDEO Y PROMEDIOS
# ==========================================
def redondear(numero, decimales=0):
    """Redondea un número a la cantidad indicada de decimales."""

    _validar_numero(numero)
    _validar_entero(decimales, "decimales")

    return print(round(numero, decimales))
def truncar(numero):
    """Elimina la parte decimal de un número."""

    _validar_numero(numero)

    return print(math.trunc(numero))
def promedio(numeros):
    """Calcula el promedio de una colección de números."""

    if isinstance(numeros, (str, bytes)) or not isinstance(numeros, Iterable):
        raise TypeError(
            "Debes proporcionar una colección de números."
        )

    numeros = list(numeros)

    if not numeros:
        raise ValueError(
            "La colección no puede estar vacía."
        )

    for numero in numeros:
        _validar_numero(numero)

    return print(sum(numeros) / len(numeros))
