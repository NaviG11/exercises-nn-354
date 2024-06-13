import sqlite3

class AgenteBusqueda:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def buscar_productos(self, categoria=None, precio_min=None, precio_max=None):
        query = 'SELECT * FROM productos WHERE 1=1'
        params = []

        if categoria:
            query += ' AND categoria = ?'
            params.append(categoria)

        if precio_min:
            query += ' AND precio >= ?'
            params.append(precio_min)

        if precio_max:
            query += ' AND precio <= ?'
            params.append(precio_max)

        self.c.execute(query, params)
        return self.c.fetchall()

    def comparar_productos(self, producto1, producto2):
        diferencias = {}
        for key in producto1.keys():
            if producto1[key] != producto2[key]:
                diferencias[key] = (producto1[key], producto2[key])
        return diferencias
    def encontrar_mejor_producto(self):
        query = '''
        SELECT * FROM productos
        WHERE precio < 10
        AND categoria = 'Categoria 1'
        ORDER BY precio DESC
        LIMIT 1
        '''
        self.c.execute(query)
        return self.c.fetchone()

# Crear una instancia del agente
agente = AgenteBusqueda('productos.db')
mejor_producto = agente.encontrar_mejor_producto()
print("--- mejor producto ---")

# Búsqueda de ejemplo
print("--- buscar productos por la categoria 1 ---")
resultados = agente.buscar_productos(categoria='Categoria 1', precio_max=11.00)
for producto in resultados:
    print(producto)
