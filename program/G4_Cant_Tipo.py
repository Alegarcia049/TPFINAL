import matplotlib.pyplot as plt
import seaborn as sns # type: ignore

import matplotlib.pyplot as plt
import seaborn as sns

# Inicializar el diccionario fuera del bucle
dicc = {}

with open('Cantidad_tipo_ult_gen.csv', mode='r') as archivo:
    archivo.readline()  # Ignorar la primera línea (encabezado)
    for linea in archivo:
        elements = linea.strip().split(',')
        if len(elements) == 2:  # Asegurarse de que hay un par tipo, valor
            tipo, valor = elements[0], int(elements[1])
            dicc[tipo] = dicc.get(tipo, 0) + valor

# Ordenar el diccionario por valor (cantidad) en orden descendente
dicc_ordenado = dict(sorted(dicc.items(), key=lambda item: item[1], reverse=True))

# Extraer tipos de Pokémon y sus cantidades en listas separadas
tipos = list(dicc_ordenado.keys())
cantidades = list(dicc_ordenado.values())

# Obtener una paleta de colores pastel
colores = sns.color_palette("pastel", len(tipos))

# Gráfico de barras horizontales
plt.figure(figsize=(10, 8))
plt.barh(tipos, cantidades, color=colores)
plt.xlabel('Cantidad')
plt.ylabel('Tipo de Pokémon')
plt.title('Cantidad de Pokémon por Tipo')
plt.tight_layout()
plt.show()