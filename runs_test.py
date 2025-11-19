"""Script para ejecutar la prueba de corridas arriba/abajo de la media.

Lee un archivo CSV localizado en el mismo directorio (por defecto
``datos_corridas.csv``) con una columna llamada ``valor`` y evalúa si
la secuencia cumple con la hipótesis de aleatoriedad en torno a la
media mediante la prueba de corridas. Los resultados se muestran en
consola usando tablas de texto.
"""
from __future__ import annotations

import csv
import math
import os
from typing import Iterable, List, Tuple


def read_values(csv_path: str) -> List[float]:
    """Lee valores numéricos de un CSV con una columna ``valor``.

    Args:
        csv_path: Ruta al archivo CSV a cargar.

    Returns:
        Lista de valores ``float``.

    Raises:
        FileNotFoundError: si no existe el archivo en disco.
        ValueError: si el CSV no tiene la columna ``valor`` o algún
            registro no es numérico.
    """

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or "valor" not in reader.fieldnames:
            raise ValueError(
                "El CSV debe incluir una columna llamada 'valor'."
            )

        values: List[float] = []
        for row in reader:
            try:
                values.append(float(row["valor"]))
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "Todos los registros de la columna 'valor' deben ser numéricos."
                ) from exc

    if not values:
        raise ValueError("El archivo CSV no contiene datos en 'valor'.")

    return values


def count_runs(binary_sequence: Iterable[int]) -> int:
    """Cuenta corridas consecutivas (cambios de signo) en una secuencia binaria.

    Una corrida se define como un grupo contiguo de valores iguales; por
    ejemplo, ``1 1 0 0 1`` contiene tres corridas: ``[1 1]``, ``[0 0]`` y
    ``[1]``.
    """

    iterator = iter(binary_sequence)
    try:
        previous = next(iterator)
    except StopIteration:
        return 0

    runs = 1
    for value in iterator:
        if value != previous:
            runs += 1
            previous = value
    return runs


def runs_test_above_below_mean(values: List[float]) -> Tuple[int, int, int, float, float, float]:
    """Calcula la prueba de corridas arriba/abajo de la media.

    Args:
        values: Lista de valores numéricos.

    Returns:
        Una tupla con ``(corridas, n_arriba, n_abajo, media, z, p_valor)``.
    """

    mean = sum(values) / len(values)
    binary_sequence = [1 if value >= mean else 0 for value in values]

    n_arriba = sum(binary_sequence)
    n_abajo = len(values) - n_arriba

    runs = count_runs(binary_sequence)

    expected_runs = ((2 * n_arriba * n_abajo) / (n_arriba + n_abajo)) + 1
    variance_runs = (
        (2 * n_arriba * n_abajo * (2 * n_arriba * n_abajo - n_arriba - n_abajo))
        / (((n_arriba + n_abajo) ** 2) * (n_arriba + n_abajo - 1))
    )

    standard_deviation = math.sqrt(variance_runs)
    z_score = (runs - expected_runs) / standard_deviation
    # p-valor bicaudal usando la función de error complementaria.
    p_value = math.erfc(abs(z_score) / math.sqrt(2))

    return runs, n_arriba, n_abajo, mean, z_score, p_value


def render_table(headers: List[str], rows: List[Iterable[str]]) -> str:
    """Construye una tabla de texto simple con columnas alineadas."""

    # Ancho por columna
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(str(cell)))

    def format_row(row: Iterable[str]) -> str:
        return " | ".join(str(cell).ljust(widths[idx]) for idx, cell in enumerate(row))

    header_line = format_row(headers)
    separator = "-+-".join("-" * width for width in widths)
    body = "\n".join(format_row(row) for row in rows)
    return f"{header_line}\n{separator}\n{body}"


def main() -> None:
    """Ejecuta la prueba de corridas con los datos del CSV local."""

    csv_path = os.path.join(os.path.dirname(__file__), "datos_corridas.csv")

    try:
        values = read_values(csv_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error al leer el CSV: {error}")
        return

    runs, n_arriba, n_abajo, mean, z_score, p_value = runs_test_above_below_mean(values)

    resumen = [
        ("Total de datos", len(values)),
        ("Media muestral", f"{mean:.4f}"),
        ("Valores arriba de la media", n_arriba),
        ("Valores abajo de la media", n_abajo),
    ]

    print("\n=== Resumen de datos ===")
    print(render_table(["Métrica", "Valor"], resumen))

    resultados = [
        ("Corridas observadas", runs),
        ("Corridas esperadas", f"{((2 * n_arriba * n_abajo) / (n_arriba + n_abajo)) + 1:.4f}"),
        ("Varianza de corridas", f"{(2 * n_arriba * n_abajo * (2 * n_arriba * n_abajo - n_arriba - n_abajo)) / (((n_arriba + n_abajo) ** 2) * (n_arriba + n_abajo - 1)):.4f}"),
        ("Estadístico Z", f"{z_score:.4f}"),
        ("p-valor (bicaudal)", f"{p_value:.4f}"),
    ]

    print("\n=== Prueba de corridas arriba/abajo de la media ===")
    print(render_table(["Resultado", "Valor"], resultados))

    # Nivel de significancia tradicional del 5%
    z_critico = 1.96
    cumple_prueba = abs(z_score) < z_critico

    mensaje = (
        "Los datos CUMPLEN con la hipótesis de aleatoriedad"
        if cumple_prueba
        else "Los datos NO cumplen con la hipótesis de aleatoriedad"
    )

    print("\n=== Validación ===")
    print(mensaje)


if __name__ == "__main__":
    main()
