"""Funciones relacionadas con velocidades de lectura y escritura."""

import time
def print_ultra_rapido(*args, velocidad=0.001, end="\n"):
    """Imprime texto a velocidad ultra rápida."""
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_super_rapido(*args, velocidad=0.01, end="\n"):
    """Imprime texto a velocidad súper rápida."""
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_rapido(*args, velocidad=0.03, end="\n"):
    """Imprime texto a velocidad rápida."""
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_medio(*args, velocidad=0.6, end="\n"):
    """Imprime texto a velocidad media."""
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_lento(*args, velocidad=0.1, end="\n"):
    """Imprime texto lentamente."""
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_super_lento(*args, velocidad=0.2, end="\n"):
    """Imprime texto a velocidad súper lenta."""
    texto = " ".join(map(str, args))

    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(velocidad)

    print(end=end, flush=True)
def print_ultra_lento(*args, velocidad=0.4, end="\n"):
    """Imprime texto a velocidad ultra lenta."""
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

    if velocidad < 0:
        raise ValueError("La velocidad no puede ser negativa.")

    if duracion_segundos < 0:
        raise ValueError("La duración no puede ser negativa.")

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
