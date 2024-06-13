import math
import random

# Definición de la clase Grafo para representar las ciudades y distancias
class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.edges = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight  # Assume undirected graph

    def get_distance(self, u, v):
        return self.edges[u][v]

# Función para generar un vecino intercambiando dos ciudades en el recorrido
def get_neighbor(path):
    idx1, idx2 = random.sample(range(len(path)), 2)
    path[idx1], path[idx2] = path[idx2], path[idx1]
    return path

# Función para calcular la longitud total del recorrido
def total_distance(path, graph):
    total = 0.0
    num_cities = len(path)
    for i in range(num_cities):
        total += graph.get_distance(path[i], path[(i + 1) % num_cities])
    return total

# Función de recocido simulado para TSP
def simulated_annealing_TSP(graph, T0, Tmin, alpha, max_iter):
    num_cities = graph.num_vertices
    current_path = list(range(num_cities))  # Recorrido inicial: [0, 1, 2, ..., num_cities-1]
    random.shuffle(current_path)  # Barajar el recorrido inicial

    best_path = current_path[:]
    min_distance = total_distance(best_path, graph)

    T = T0
    iteration = 0

    while T > Tmin and iteration < max_iter:
        new_path = get_neighbor(current_path[:])
        new_distance = total_distance(new_path, graph)
        delta_distance = new_distance - min_distance

        if delta_distance < 0 or random.random() < math.exp(-delta_distance / T):
            current_path = new_path[:]
            min_distance = new_distance

        if new_distance < min_distance:
            best_path = new_path[:]
            min_distance = new_distance

        T *= alpha
        iteration += 1

    return best_path, min_distance

# Ejemplo de uso
if __name__ == "__main__":
    # Creamos un grafo con 5 ciudades y definimos las distancias entre ellas
    num_cities = 5
    graph = Graph(num_cities)
    graph.add_edge(0, 1, 2.0)  # Ciudad 0 - Ciudad 1, distancia 2.0
    graph.add_edge(0, 2, 4.0)  # Ciudad 0 - Ciudad 2, distancia 4.0
    graph.add_edge(0, 3, 1.0)  # Ciudad 0 - Ciudad 3, distancia 1.0
    graph.add_edge(0, 4, 3.0)  # Ciudad 0 - Ciudad 4, distancia 3.0
    graph.add_edge(1, 2, 3.0)  # Ciudad 1 - Ciudad 2, distancia 3.0
    graph.add_edge(1, 3, 2.0)  # Ciudad 1 - Ciudad 3, distancia 2.0
    graph.add_edge(1, 4, 2.5)  # Ciudad 1 - Ciudad 4, distancia 2.5
    graph.add_edge(2, 3, 1.5)  # Ciudad 2 - Ciudad 3, distancia 1.5
    graph.add_edge(2, 4, 2.0)  # Ciudad 2 - Ciudad 4, distancia 2.0
    graph.add_edge(3, 4, 3.5)  # Ciudad 3 - Ciudad 4, distancia 3.5
    print(graph.edges)
    # Parámetros del algoritmo
    T0 = 100.0          # Temperatura inicial
    Tmin = 1.0          # Temperatura mínima
    alpha = 0.9         # Factor de enfriamiento
    max_iter = 1000     # Número máximo de iteraciones

    # Ejecutamos el algoritmo de recocido simulado
    best_path, min_distance = simulated_annealing_TSP(graph, T0, Tmin, alpha, max_iter)

    # Mostramos los resultados
    print(f"Mejor recorrido encontrado: {best_path}")
    print(f"Longitud del mejor recorrido: {min_distance}")
