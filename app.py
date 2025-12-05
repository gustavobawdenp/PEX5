from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
from functools import wraps
import csv
from io import StringIO

from database import init_db
import models
import unicodedata

def normalizar(texto):
    if not texto:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()

# Cria app Flask apontando para a pasta 'frontend'
app = Flask(
    __name__,
    template_folder="frontend",       # onde estão os HTML
    static_folder="frontend/static"   # onde estão CSS/JS
)
CORS(app)

# Inicializa banco ao iniciar o app
init_db()

# ============================
# AUTENTICAÇÃO (token antigo)
# ============================
ADMIN_TOKEN = "segredo-super-admin"

def exigir_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != ADMIN_TOKEN:
            return jsonify({"erro": "Acesso não autorizado"}), 401
        return f(*args, **kwargs)
    return wrapper

# ============================
# ROTAS DE FRONTEND
# ============================

# Página inicial
@app.route("/")
def inicio():
    return render_template("selecionar_disciplina.html")  # página inicial

# ============================
# ROTAS DE CRUD
# ============================

@app.route("/questoes", methods=["POST"])
@exigir_token
def criar():
    data = request.json
    campos_obrigatorios = [
        "enunciado", "alternativa_a", "alternativa_b",
        "alternativa_c", "alternativa_d", "correta",
        "disciplina", "dificuldade"
    ]
    for campo in campos_obrigatorios:
        if campo not in data or data[campo].strip() == "":
            return jsonify({"erro": f"Campo obrigatório ausente: {campo}"}), 400
    if data["correta"] not in ["A", "B", "C", "D"]:
        return jsonify({"erro": "O campo 'correta' deve ser apenas A, B, C ou D"}), 400

    models.criar_questao(data)
    return jsonify({"mensagem": "Questão criada com sucesso!"})


@app.route("/questoes", methods=["GET"])
def listar():
    filtros = {}
    if "disciplina" in request.args:
        filtros["disciplina"] = normalizar(request.args["disciplina"])

    questoes = models.listar_questoes(filtros)
    resultado = []
    for q in questoes:
        if "disciplina" in filtros:
            if normalizar(q["disciplina"]) != filtros["disciplina"]:
                continue
        resultado.append(dict(q))
    return jsonify(resultado)


@app.route("/questoes/<int:id>", methods=["GET"])
def buscar(id):
    q = models.buscar_questao(id)
    if q:
        return jsonify(dict(q))
    return jsonify({"erro": "Questão não encontrada"}), 404


@app.route("/questoes/<int:id>", methods=["PUT"])
@exigir_token
def atualizar(id):
    data = request.json
    models.atualizar_questao(id, data)
    return jsonify({"mensagem": "Questão atualizada!"})


@app.route("/questoes/<int:id>", methods=["DELETE"])
@exigir_token
def deletar(id):
    models.deletar_questao(id)
    return jsonify({"mensagem": "Questão removida!"})


# ============================
# EXPORTAÇÃO CSV
# ============================

@app.route("/exportar", methods=["GET"])
def exportar_csv():
    disciplina = request.args.get("disciplina", None)
    filtros = {}
    if disciplina:
        filtros["disciplina"] = disciplina

    questoes = models.listar_questoes(filtros)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "enunciado", "alternativa_a", "alternativa_b",
        "alternativa_c", "alternativa_d", "correta",
        "disciplina", "dificuldade"
    ])
    for q in questoes:
        writer.writerow([
            q["id"], q["enunciado"], q["alternativa_a"], q["alternativa_b"],
            q["alternativa_c"], q["alternativa_d"], q["correta"],
            q["disciplina"], q["dificuldade"]
        ])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=questoes.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True)
