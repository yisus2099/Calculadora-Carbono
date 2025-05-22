from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Función para guardar resultados en un archivo JSON
def guardar_resultado(usuario, resultado):
    data = {}
    if os.path.exists("resultados.json"):
        with open("resultados.json", "r") as file:
            data = json.load(file)
    if usuario not in data:
        data[usuario] = []
    data[usuario].append(resultado)
    with open("resultados.json", "w") as file:
        json.dump(data, file, indent=4)

# Función para leer historial de un usuario
def leer_historial(usuario):
    if os.path.exists("resultados.json"):
        with open("resultados.json", "r") as file:
            data = json.load(file)
            return data.get(usuario, [])
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    recomendacion = None
    usuario = None
    historial = []
    if request.method == "POST":
        try:
            usuario = request.form["usuario"]
            km = float(request.form["kilometros"])
            transporte = request.form["transporte"]

            emisiones = {
                "auto": 0.21,
                "moto": 0.09,
                "metro": 0.04,
                "bus": 0.05,
                "avion": 0.25,
                "bici": 0.0
            }

            huella = km * emisiones.get(transporte, 0.21)
            resultado = f"Tu huella de carbono semanal es de {huella:.2f} kg CO₂ usando {transporte}."
            guardar_resultado(usuario, resultado)
            historial = leer_historial(usuario)

            # Recomendaciones personalizadas
            if huella > 100:
                recomendacion = "Te recomendamos reducir el uso de transporte individual y optar por medios más sostenibles como bicicleta o metro."
            elif huella > 50:
                recomendacion = "Intenta combinar viajes o usar transporte público más seguido."
            else:
                recomendacion = "¡Excelente! Tu impacto es bajo. Sigue así."
        except ValueError:
            resultado = "Por favor, ingresa un número válido."
    return render_template("index.html", resultado=resultado, recomendacion=recomendacion, historial=historial, usuario=usuario)

if __name__ == "__main__":
    app.run(debug=True)
