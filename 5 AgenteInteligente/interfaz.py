from flask import Flask, request, jsonify
import sqlite3
import agente
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('productos.db')
    conn.row_factory = sqlite3.Row
    return conn
#/buscar?categoria=Categoria%1
@app.route('/buscar', methods=['GET'])
def buscar():
    categoria = request.args.get('categoria')
    #precio_min = request.args.get('precio_min')
    #precio_max = request.args.get('precio_max')

    conn = get_db_connection()
    agente = agente.AgenteBusqueda('productos.db')
    resultados = agente.buscar_productos(categoria)
    conn.close()

    return jsonify(resultados)
#/comparar?id1=1&id2=2
@app.route('/comparar', methods=['GET'])
def comparar():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM productos WHERE id = ?', (id1,))
    producto1 = dict(c.fetchone())
    c.execute('SELECT * FROM productos WHERE id = ?', (id2,))
    producto2 = dict(c.fetchone())
    conn.close()

    diferencias = agente.comparar_productos(producto1, producto2)
    return jsonify(diferencias)

if __name__ == '__main__':
    app.run()
