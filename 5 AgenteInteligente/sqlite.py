import sqlite3

# Crear y conectar a la base de datos
conn = sqlite3.connect('productos.db')
c = conn.cursor()

# Crear una tabla
c.execute('''
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT NOT NULL
)
''')

# Insertar datos de ejemplo
productos = [
    (1, 'Producto A', 10.99, 'Categoria 1'),
    (2, 'Producto B', 12.49, 'Categoria 2'),
    (3, 'Producto C', 9.99, 'Categoria 1'),
    (4, 'Producto D', 11.99, 'Categoria 3')
]

c.executemany('INSERT INTO productos VALUES (?, ?, ?, ?)', productos)
conn.commit()
