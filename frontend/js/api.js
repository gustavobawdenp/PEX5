const API_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:5000"
    : "https://pex5.onrender.com";
// TOKEN ADMIN – necessário para operações administrativas
const TOKEN = "segredo-super-admin";

/**
 * LISTAR QUESTÕES
 * @param {string|null} filtroDisciplina
 */
async function listarQuestoes(filtroDisciplina = null) {
    let url = `${API_URL}/questoes`;
    if (filtroDisciplina) {
        url += `?disciplina=${encodeURIComponent(filtroDisciplina)}`;
    }

    const resposta = await fetch(url);
    if (!resposta.ok) {
        throw new Error(`Erro ao listar questões: ${resposta.statusText}`);
    }
    return resposta.json();
}

/**
 * CRIAR QUESTÃO – requer token
 */
async function criarQuestao(questao) {
    const resposta = await fetch(`${API_URL}/questoes`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": TOKEN
        },
        body: JSON.stringify(questao)
    });

    if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.erro || "Falha ao criar questão");
    }
    return resposta.json();
}

/**
 * EDITAR QUESTÃO – requer token
 */
async function editarQuestao(id, questao) {
    const resposta = await fetch(`${API_URL}/questoes/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": TOKEN
        },
        body: JSON.stringify(questao)
    });

    if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.erro || "Falha ao editar questão");
    }
    return resposta.json();
}

/**
 * DELETAR QUESTÃO – requer token
 */
async function deletarQuestao(id) {
    const resposta = await fetch(`${API_URL}/questoes/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": TOKEN
        }
    });

    if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.erro || "Falha ao deletar questão");
    }
    return resposta.json();
}

/**
 * BUSCAR QUESTÃO POR ID – não requer token
 */
async function buscarQuestao(id) {
    const resposta = await fetch(`${API_URL}/questoes/${id}`);
    if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.erro || "Questão não encontrada");
    }
    return resposta.json();
}
