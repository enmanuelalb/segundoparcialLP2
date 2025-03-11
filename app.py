from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar productos desde CSV y agregar un ID automático
try:
    df = pd.read_csv("productos.csv")
    df.insert(0, "id", range(1, len(df) + 1))  # Agregar ID automático desde 1
    df.rename(columns={"nombre_producto": "nombre"}, inplace=True)  # Renombrar columna
    productos = df.to_dict(orient="records")
except Exception as e:
    print(f"Error al cargar productos.csv: {e}")
    productos = []

@app.route("/")
def index():
    return render_template("index.html", productos=productos)

@app.route("/productos")
def get_productos():
    return jsonify(productos)

@app.route("/productos/<int:producto_id>")
def get_producto(producto_id):
    producto = next((p for p in productos if p["id"] == producto_id), None)
    if producto:
        return render_template("producto.html", producto=producto)
    return "Producto no encontrado", 404

if __name__ == "__main__":
    app.run(debug=True)
