"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
import pandas as pd


def pregunta_01(ruta_archivo="files/input/clusters_report.txt"):
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    # Leer todas las líneas del archivo
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Quitar salto de línea al final de cada línea
    lineas = [linea.rstrip() for linea in lineas]

    # Omitir las cuatro primeras líneas de encabezado
    cuerpo = lineas[4:]

    # Reconstruir filas lógicas (cada cluster puede ocupar varias líneas)
    filas_crudas = []
    fila_actual = ""

    for linea in cuerpo:
        # Una nueva fila comienza cuando la línea arranca con un número de cluster
        if re.match(r"\s*\d+\s+", linea):
            if fila_actual:
                filas_crudas.append(fila_actual)
            fila_actual = linea
        else:
            # Continuación de la fila anterior
            fila_actual += " " + linea

    # Añadir la última fila acumulada si existe
    if fila_actual:
        filas_crudas.append(fila_actual)

    registros = []
    for fila in filas_crudas:
        # Separar en bloques usando dos o más espacios como separador
        partes = re.split(r"\s{2,}", fila.strip())

        if len(partes) < 4:
            continue

        # Columna 1: número de cluster
        cluster = int(partes[0])

        # Columna 2: cantidad de palabras clave
        cantidad = int(partes[1])

        # Columna 3: porcentaje (reemplazar coma por punto y quitar %)
        porcentaje_str = partes[2].replace("%", "").replace(",", ".")
        porcentaje = float(porcentaje_str)

        # Columna 4: principales palabras clave
        # Unir todo lo que queda, limpiar espacios y punto final
        palabras_brutas = " ".join(partes[3:])
        # Quitar punto final (y otros puntos residuales)
        palabras_brutas = palabras_brutas.replace(".", "")
        # Normalizar espacios en blanco
        palabras_limpias = re.sub(r"\s+", " ", palabras_brutas).strip()

        registros.append(
            [cluster, cantidad, porcentaje, palabras_limpias]
        )

    columnas = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    df = pd.DataFrame(registros, columns=columnas)
    return df


if __name__ == "__main__":
    resultado = pregunta_01()
    print(resultado.head())