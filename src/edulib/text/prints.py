"""Funciones relacionadas con velocidades de lectura y escritura."""

import math
import time
from numbers import Real


def _validar_tiempo(valor, nombre):
    """Valida que un intervalo sea real, finito y no negativo."""

    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise TypeError(f"{nombre} debe ser un número real.")

    if not math.isfinite(valor):
        raise ValueError(f"{nombre} debe ser un número finito.")

    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo.")


def print_ultra_rapido(*args, velocidad=0.001, end="\n"):
    """Imprime texto a velocidad ultra rápida."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_super_rapido(*args, velocidad=0.01, end="\n"):
    """Imprime texto a velocidad súper rápida."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_rapido(*args, velocidad=0.03, end="\n"):
    """Imprime texto a velocidad rápida."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_medio(*args, velocidad=0.1, end="\n"):
    """Imprime texto a velocidad media."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_lento(*args, velocidad=0.2, end="\n"):
    """Imprime texto lentamente."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_super_lento(*args, velocidad=0.4, end="\n"):
    """Imprime texto a velocidad súper lenta."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_ultra_lento(*args, velocidad=0.6, end="\n"):
    """Imprime texto a velocidad ultra lenta."""
    _validar_tiempo(velocidad, "velocidad")
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)

def animar_secuencia(mensaje_base, secuencia=("", ".", "..", "..."), velocidad=0.8, duracion_segundos=5):
    """
    Anima una secuencia de estados en la misma línea.

    Args:
        mensaje_base: Texto fijo antes de la animación.
        secuencia: Estados que se alternarán.
        velocidad: Tiempo entre cada cambio.
        duracion_segundos: Duración total de la animación.
    """

    if not secuencia:
        raise ValueError("La secuencia no puede estar vacía.")

    _validar_tiempo(velocidad, "velocidad")
    _validar_tiempo(duracion_segundos, "duracion_segundos")

    tiempo_inicio = time.monotonic()
    i = 0

    while time.monotonic() - tiempo_inicio < duracion_segundos:
        estado_actual = secuencia[i % len(secuencia)]

        print(
            f"\r{mensaje_base}{estado_actual}\033[K",
            end="",
            flush=True
        )

        time.sleep(velocidad)
        i += 1

    print()

def print_y_animar_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.1,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base lentamente y luego anima una secuencia."""
    if not secuencia:
        raise ValueError("La secuencia no puede estar vacía.")

    _validar_tiempo(velocidad, "velocidad")
    _validar_tiempo(duracion_segundos, "duracion_segundos")
    _validar_tiempo(velocidad_texto, "velocidad_texto")

    for caracter in str(mensaje_base):
        print(caracter, end="", flush=True)
        time.sleep(velocidad_texto)

    tiempo_inicio = time.monotonic()
    i = 0

    while time.monotonic() - tiempo_inicio < duracion_segundos:
        estado_actual = secuencia[i % len(secuencia)]
        print(
            f"\r{mensaje_base}{estado_actual}\033[K",
            end="",
            flush=True
        )
        time.sleep(velocidad)
        i += 1

    print()
def print_ultra_rapido_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.001,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad ultra rápida y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
def print_super_rapido_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.01,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad súper rápida y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
def print_rapido_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.03,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad rápida y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
def print_medio_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.1,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad media y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
def print_lento_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.2,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad lenta y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
def print_super_lento_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.4,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad súper lenta y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
def print_ultra_lento_y_secuencia(
    mensaje_base,
    secuencia=("", ".", "..", "..."),
    velocidad_texto=0.6,
    velocidad=0.8,
    duracion_segundos=5,
):
    """Escribe el mensaje base a velocidad ultra lenta y anima una secuencia."""
    return print_y_animar_secuencia(
        mensaje_base,
        secuencia,
        velocidad_texto,
        velocidad,
        duracion_segundos,
    )
