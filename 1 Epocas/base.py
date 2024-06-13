import random
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Cargar el dataset de Iris
iris = load_iris()
X = iris.data
y = iris.target

# Normalizar las características
scaler = StandardScaler()
X = scaler.fit_transform(X)

# One-hot encoding de las etiquetas
encoder = OneHotEncoder(sparse_output=False)
y = encoder.fit_transform(y.reshape(-1, 1))

# Inicializar los parámetros de la red neuronal
input_size = X.shape[1]
hidden_size = 5  # Número de neuronas en la capa oculta
output_size = y.shape[1]
learning_rate = 0.4

# Inicializar los pesos y sesgos
W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

# Funciones de activación y sus derivadas
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# Función de pérdida (entropía cruzada)
def cross_entropy_loss(y_true, y_pred):
    return -np.mean(np.sum(y_true * np.log(y_pred + 1e-9), axis=1))

# Función de predicción
def predict(X, W1, b1, W2, b2):
    z1 = np.dot(X, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = softmax(z2)
    return np.argmax(a2, axis=1)

# Entrenamiento de la red neuronal
epochs = 10
epoch = 0
perfect_accuracy = False
# Entrenamiento de la red neuronal
for epoch in range(epochs):
    # Forward propagation
    z1 = np.dot(X, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = softmax(z2)

    # Cálculo del error
    loss = cross_entropy_loss(y, a2)

    # Backpropagation
    d_a2 = a2 - y
    d_W2 = np.dot(a1.T, d_a2)
    d_b2 = np.sum(d_a2, axis=0, keepdims=True)

    d_a1 = np.dot(d_a2, W2.T) * sigmoid_derivative(a1)
    d_W1 = np.dot(X.T, d_a1)
    d_b1 = np.sum(d_a1, axis=0, keepdims=True)

    # Actualización de los pesos y sesgos
    W2 -= learning_rate * d_W2
    b2 -= learning_rate * d_b2
    W1 -= learning_rate * d_W1
    b1 -= learning_rate * d_b1

    # Mostrar el error cada 100 épocas
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss}")

# Evaluación de la red neuronal
def predict(X):
    z1 = np.dot(X, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = softmax(z2)
    return np.argmax(a2, axis=1)

predictions = predict(X)
accuracy = np.mean(predictions == np.argmax(y, axis=1))
print(f"Accuracy: {accuracy * 100:.2f}%")