import random
import heapq
import networkx as nx
import matplotlib.pyplot as plt
# Número de nodos en el grafo
num_nodes = 5

# Función para inicializar un grafo aleatorio
# Función para inicializar el grafo con valores específicos
def initialize_graph():
    graph = [
        [0, 7, 9, 8, 20],
        [7, 0, 10, 11, 4],
        [9, 10, 0, 15, 5],
        [8, 11, 15, 0, 17],
        [20, 4, 5, 17, 0]
    ]
    return graph

grafo = initialize_graph()
print(grafo)
# Función para calcular la distancia mínima desde start_node a todos los demás nodos usando Dijkstra
def fitness(graph, start_node):
    num_nodes = len(graph)
    distances = {node: float('inf') for node in range(num_nodes)}  # Inicializar distancias como infinito
    distances[start_node] = 0
    priority_queue = [(0, start_node)]  # Cola de prioridad (distancia, nodo)
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        # Si la distancia actual es mayor que la almacenada, se omite el cálculo
        if current_distance > distances[current_node]:
            continue
        # Explorar los nodos adyacentes
        for neighbor in range(num_nodes):
            if graph[current_node][neighbor] > 0:  # Solo considerar nodos adyacentes
                distance = current_distance + graph[current_node][neighbor]
                # Actualizar la distancia si encontramos un camino más corto
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
    print("Distancias: ", distances)
    return sum(distances.values())  # Retornar la suma de todas las distancias mínimas
start_node = 0
total_distance = fitness(grafo, start_node)
print("Distancia total: ",total_distance)
# # Función para realizar el crossover de dos grafos
def crossover(parent1, parent2):
    # Un crossover basado en puntos de corte
    cutoff = random.randint(1, num_nodes - 1)
    child = parent1[:cutoff] + parent2[cutoff:]
    return child

# # Función para mutar un grafo
def mutate(graph):
    mutated_graph = [row[:] for row in graph]  # Copiar el grafo original
    row = random.randint(0, num_nodes - 1)
    col = random.randint(0, num_nodes - 1)
    mutated_graph[row][col] = random.randint(1, 10)  # Mutación de peso de arista aleatorio
    return mutated_graph
mutacion = mutate(grafo)
print("Mutación: ", mutacion)
# Función del algoritmo genético para encontrar el mejor grafo
def genetic_algorithm(num_generations, population_size, start_node):
    population = []

    # Generar población inicial de grafos
    for _ in range(population_size):
        individual = initialize_graph()
        population.append(individual)

    # Evolución de la población
    for generation in range(num_generations):
        # Calcular fitness para cada individuo en la población
        fitness_scores = []
        for individual in population:
            fitness_score = fitness(individual, start_node)
            if fitness_score is not None:  # Asegurarse de que el fitness no sea None
                fitness_scores.append((fitness_score, individual))

        # Ordenar la población por fitness (en orden ascendente si es una función de costo)
        fitness_scores.sort(key=lambda x: x[0])  # Ordenar por el primer elemento (fitness)

        # Selección de los mejores individuos (usando elitismo)
        selected_individuals = [individual for _, individual in fitness_scores[:population_size]]

        # Reproducción y mutación
        new_population = []
        while len(new_population) < population_size:
            if selected_individuals:
                parent1 = random.choice(selected_individuals)
                parent2 = random.choice(selected_individuals)

                # Crossover
                child = crossover(parent1, parent2)

                # Mutación
                if random.random() < 0.5:  # Probabilidad de mutación del 50%
                    child = mutate(child)

                new_population.append(child)
            else:
                # En caso de que selected_individuals esté vacío, generar un nuevo individuo
                new_individual = initialize_graph()
                new_population.append(new_individual)

        population = new_population

    # Devolver el mejor individuo (grafo) encontrado
    best_individual = min(fitness_scores, key=lambda x: x[0])[1]
    return best_individual

if __name__ == "__main__":
    num_generations = 100
    population_size = 50
    start_node = 0  # Nodo inicial para el problema específico

    best_graph = genetic_algorithm(num_generations, population_size, start_node)
    print("Mejor grafo encontrado:")
    for row in best_graph:
        print(row)
    print("Distancia total:", fitness(best_graph, start_node))

    # Visualización del mejor grafo encontrado
    G = nx.Graph()
    for i in range(num_nodes):
        for j in range(num_nodes):
            if best_graph[i][j] > 0:
                G.add_edge(chr(65 + i), chr(65 + j), weight=best_graph[i][j])

    pos = nx.spring_layout(G)  # Posiciones de los nodos para dibujar el grafo de manera más ordenada

    # Dibujar nodos y etiquetas
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2)

    # Dibujar etiquetas de pesos de las aristas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Mejor grafo encontrado")
    plt.axis('off')
    plt.show()