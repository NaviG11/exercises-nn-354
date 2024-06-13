import math
import random

def simulated_annealing(func, x0, T0, Tmin, alpha, max_iter):
    def get_neighbor(x):
        """Genera un vecino de x (esto depende del problema específico)"""
        return x + random.uniform(-0.1, 0.1)

    def acceptance_probability(delta_e, T):
        """Calcula la probabilidad de aceptación"""
        return math.exp(-delta_e / T)

    # Inicialización
    x_current = x0
    f_current = func(x_current)
    x_best = x_current
    f_best = f_current
    T = T0

    # Iteración
    for i in range(max_iter):
        if T < Tmin:
            break

        # Genera un nuevo vecino
        x_new = get_neighbor(x_current)
        f_new = func(x_new)

        # Calcula la diferencia de costo
        delta_e = f_new - f_current

        # Decide si acepta el nuevo estado
        if delta_e < 0 or acceptance_probability(delta_e, T) > random.random():
            x_current = x_new
            f_current = f_new

            # Actualiza la mejor solución encontrada
            if f_new < f_best:
                x_best = x_new
                f_best = f_new

        # Enfriamiento
        T *= alpha

    return x_best, f_best

# Definimos una función de costo de ejemplo (mínimo en x=0)
def cost_function(x):
    return (x - 2) ** 2

# Parámetros del algoritmo
x0 = 10            # Solución inicial
T0 = 1000          # Temperatura inicial
Tmin = 1           # Temperatura mínima
alpha = 0.9        # Factor de enfriamiento
max_iter = 1000    # Número máximo de iteraciones

# Ejecutamos el algoritmo de recocido simulado
best_solution, best_cost = simulated_annealing(cost_function, x0, T0, Tmin, alpha, max_iter)

print(f"Mejor solución encontrada: x = {best_solution}")
print(f"Coste de la mejor solución: f(x) = {best_cost}")
