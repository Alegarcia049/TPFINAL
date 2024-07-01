import matplotlib.pyplot as plt

# 1. Crear los datos
cantidad=[]
epoca=[]
with open('Cantidad_pokemones_x_gen.csv', mode='r') as archivo:
    for linea in archivo:

        # Separar los valores de la línea CSV
        valores = linea.split(',')

        x=valores.pop(0)
        epoca.append(x)
        # Extraer solo los nombres (saltando cada segundo elemento, que son los números)
        nombres = []
        for i in range(1, len(valores), 2):
            nombres.append(valores[i])

        # Contar la cantidad de nombres distintos sin usar set
        nombres_distintos = []
        for nombre in nombres:
            if nombre not in nombres_distintos:
                nombres_distintos.append(nombre)

        cantidad.append(len(nombres_distintos))

# 2. Crear el gráfico de líneas
plt.plot(epoca, cantidad)

# 3. Personalizar los valores del eje x
plt.xticks([0, 10, 20, 30, 40, 50])

# 4. Personalizar los valores del eje y
plt.yticks([0, 50, 100, 150, 200, 250])

# Etiquetas y título
plt.xlabel('Epochs')
plt.ylabel('Diversity')
plt.title('Diversity vs Epochs')

# Mostrar el gráfico
plt.grid(True)
plt.show()