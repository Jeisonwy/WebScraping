from flask import Flask, render_template, jsonify, request
import subprocess, os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-scraper", methods=["POST"])
def run_scraper():
    try:
        data = request.get_json()
        max_iterations = str(data.get("maxIterations", 10))  # Valor por defecto

        # Ejecuta el script con el parámetro
        subprocess.run(["python", "main.py", max_iterations], check=True)

        return jsonify({"status": "ok", "message": f"Scraper ejecutado correctamente con {max_iterations} Pokémones"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
