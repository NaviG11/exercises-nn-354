import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Cargar el dataset Iris desde sklearn
iris = load_iris()
X = iris.data
y = iris.target.reshape(-1, 1)

# Preprocesamiento
scaler = StandardScaler()
X = scaler.fit_transform(X)

encoder = OneHotEncoder(sparse_output=False)
y = encoder.fit_transform(y)

# Inicialización de pesos
input_size = 4
hidden_size = 5
output_size = 3

np.random.seed(42)  # Para reproducibilidad
weights_input_hidden = np.random.rand(input_size, hidden_size) - 0.5
weights_hidden_output = np.random.rand(hidden_size, output_size) - 0.5
bias_hidden = np.random.rand(hidden_size) - 0.5
bias_output = np.random.rand(output_size) - 0.5

learning_rate = 0.2

# Función de activación
def step_function(x):
    return np.where(x >= 0, 1, 0)

# Entrenamiento
epochs = 1000

for epoch in range(epochs):
    for i in range(X.shape[0]):
        # Propagación hacia adelante
        hidden_input = np.dot(X[i], weights_input_hidden) + bias_hidden
        hidden_output = step_function(hidden_input)
        final_input = np.dot(hidden_output, weights_hidden_output) + bias_output
        final_output = step_function(final_input)
        # Error (MSE)
        error = y[i] - final_output
        # Retropropagación
        d_output = error
        d_hidden = d_output.dot(weights_hidden_output.T) * (hidden_output * (1 - hidden_output))
        # Actualización de pesos y biases
        weights_hidden_output += learning_rate * np.outer(hidden_output, d_output)
        bias_output += learning_rate * d_output
        weights_input_hidden += learning_rate * np.outer(X[i], d_hidden)
        bias_hidden += learning_rate * d_hidden

# Evaluación
def predict(X):
    hidden_input = np.dot(X, weights_input_hidden) + bias_hidden
    hidden_output = step_function(hidden_input)
    final_input = np.dot(hidden_output, weights_hidden_output) + bias_output
    final_output = step_function(final_input)
    return final_output

# Predicciones en el dataset completo
predictions = predict(X)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y, axis=1)

accuracy = np.mean(predicted_classes == true_classes)
print(f"Precisión: {accuracy * 100:.2f}%")
