import matplotlib.pyplot as plt

# Datos
with open('mejor_equipo_stats.csv', mode='r') as archivo:
    pokemones=[]
    stats=[]
    archivo.readline()  # Ignorar la primera línea
    for linea in archivo:
        # Separar los valores de la línea CSV
        valores = linea.strip().split(',')
        nombre=valores.pop(0)
        pokemones.append(nombre)
        stats.append([float(valor) for valor in valores])

datos1 = stats[0]
datos2 = stats[1]
datos3 = stats[2]
datos4 = stats[3]
datos5 = stats[4]
datos6 = stats[5]

labels = ['Max Hp', 'Attack', 'Defense', 'Sp.Attack', 'Sp.Defense', 'Speed']  # Etiquetas para cada vértice
num_vars = len(labels)

# Calcular ángulos
angles = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
angles += angles[:1]  # Añadir el primer ángulo al final para cerrar el círculo

# Añadir el primer valor al final para cerrar el círculo para cada conjunto de datos
datos1 += datos1[:1]
datos2 += datos2[:1]
datos3 += datos3[:1]
datos4 += datos4[:1]
datos5 += datos5[:1]
datos6 += datos6[:1]

# Crear el gráfico de radar
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Rellenar el área para cada conjunto de datos con diferentes colores
ax.fill(angles, datos1, color='blue', alpha=0.25, label=pokemones[0])
ax.fill(angles, datos2, color='green', alpha=0.25, label=pokemones[1])
ax.fill(angles, datos3, color='red', alpha=0.25, label=pokemones[2])
ax.fill(angles, datos4, color='purple', alpha=0.25, label=pokemones[3])
ax.fill(angles, datos5, color='orange', alpha=0.25, label=pokemones[4])
ax.fill(angles, datos6, color='cyan', alpha=0.25, label=pokemones[5])

# Etiquetas
ax.set_yticklabels([])  # Sin etiquetas en los ejes radiales
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=12)

# Mostrar leyenda en una posición fuera del gráfico
ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1))

plt.show()