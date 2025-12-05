from database import get_db
import unicodedata

# Função para normalizar texto (remover acentos, espaços extras e minúsculas)
def normalizar_texto(texto):
    if not texto:
        return ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()

def criar_questao(data):
    db = get_db()
    try:
        query = """
            INSERT INTO questoes 
            (enunciado, alternativa_a, alternativa_b, alternativa_c, alternativa_d, correta, disciplina, dificuldade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.execute(query, (
            data["enunciado"],
            data["alternativa_a"],
            data["alternativa_b"],
            data["alternativa_c"],
            data["alternativa_d"],
            data["correta"],
            data["disciplina"],
            data["dificuldade"]
        ))
        db.commit()
    finally:
        db.close()

def listar_questoes(filtros=None):
    db = get_db()
    filtros = filtros or {}
    query = "SELECT * FROM questoes WHERE 1=1"
    args = []

    # FILTRO POR DISCIPLINA (normalizado)
    if "disciplina" in filtros and filtros["disciplina"]:
        disciplinas = db.execute("SELECT * FROM questoes").fetchall()
        # Filtra manualmente para garantir normalização
        resultado = []
        for q in disciplinas:
            if normalizar_texto(q["disciplina"]) == normalizar_texto(filtros["disciplina"]):
                resultado.append(q)
        db.close()
        # FILTRO POR DIFICULDADE opcional
        if "dificuldade" in filtros and filtros["dificuldade"]:
            resultado = [q for q in resultado if q["dificuldade"] == filtros["dificuldade"]]
        return resultado

    # Se não houver filtro de disciplina
    if "dificuldade" in filtros and filtros["dificuldade"]:
        query += " AND dificuldade = ?"
        args.append(filtros["dificuldade"])

    try:
        return db.execute(query, args).fetchall()
    finally:
        db.close()

def buscar_questao(id):
    db = get_db()
    try:
        return db.execute("SELECT * FROM questoes WHERE id = ?", (id,)).fetchone()
    finally:
        db.close()

def atualizar_questao(id, data):
    db = get_db()
    try:
        query = """
            UPDATE questoes SET enunciado=?, alternativa_a=?, alternativa_b=?, alternativa_c=?, alternativa_d=?, correta=?, disciplina=?, dificuldade=?
            WHERE id=?
        """
        db.execute(query, (
            data["enunciado"],
            data["alternativa_a"],
            data["alternativa_b"],
            data["alternativa_c"],
            data["alternativa_d"],
            data["correta"],
            data["disciplina"],
            data["dificuldade"],
            id
        ))
        db.commit()
    finally:
        db.close()

def deletar_questao(id):
    db = get_db()
    try:
        db.execute("DELETE FROM questoes WHERE id = ?", (id,))
        db.commit()
    finally:
        db.close()
