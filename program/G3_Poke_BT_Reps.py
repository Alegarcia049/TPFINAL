import matplotlib.pyplot as plt

# Diversidad de pokemones en última generación
conteo_pokemones = {}

with open('Best_teams_x_generation.csv', mode='r') as archivo:
    next(archivo)  # Salta la cabecera si existe
    for linea in archivo:
        # Separar los valores de la línea CSV
        valores = linea.strip().split(',')
        if int(valores[0]) == 50:  # Convertir a entero para comparar correctamente
            nombres = valores[3:]  # Incluir el 'Starter' en el conteo
    
            # Contar la cantidad de veces que se repite cada nombre
            for nombre in nombres:
                nombre_limpio = nombre.strip()  # Limpiar espacios y saltos de línea
                if nombre_limpio in conteo_pokemones:
                    conteo_pokemones[nombre_limpio] += 1
                else:
                    conteo_pokemones[nombre_limpio] = 1

pokemones = [i for i in conteo_pokemones.keys()]
cantidad = [j for j in conteo_pokemones.values()]

# Encuentra el valor máximo en 'cantidad' y suma un poco para el límite superior
max_cantidad = max(cantidad) + 2

ticks = range(0, max_cantidad, max(1, max_cantidad // 10))  # Asegura al menos 1 de paso

# Paleta de colores pastel
colores_pastel = ['#ffd1dc', '#ff9aa2', '#ffb7b2', '#ffdac1', '#e2f0cb', '#b5ead7', '#c7ceea']

# Gráfico de barras horizontales con colores pastel
plt.barh(pokemones, cantidad, color=colores_pastel[:len(pokemones)])

# Ajustar los ticks del eje X
plt.xticks(ticks)

# Mostrar el gráfico
plt.xlabel('Count')
plt.ylabel('Pokemon')
plt.title('Pokemon count in best team')
plt.show()