// listar_questoes.js

// Pega a disciplina da URL
const disciplina = new URLSearchParams(window.location.search).get("disciplina");

// Função para carregar e exibir as questões
async function carregarQuestoes() {
    try {
        const questoes = await listarQuestoes(disciplina);
        const lista = document.getElementById("lista");
        lista.innerHTML = "";

        if (!questoes || questoes.length === 0) {
            lista.innerHTML = "<p>Sem questões para esta disciplina.</p>";
            return;
        }

        // Cria container para cada questão
        questoes.forEach((q) => {
            const div = document.createElement("div");
            div.className = "questao-item";
            div.style.border = "1px solid #ccc";
            div.style.padding = "10px";
            div.style.marginBottom = "15px";
            div.style.borderRadius = "8px";
            div.style.backgroundColor = "#f9f9f9";

            // Monta lista de alternativas
            const alternativas = ["A", "B", "C", "D"].map((letra) => {
                const texto = q[`alternativa_${letra.toLowerCase()}`];
                if (q.correta === letra) {
                    return `<li><strong>${letra}) ${texto}</strong></li>`;
                } else {
                    return `<li>${letra}) ${texto}</li>`;
                }
            }).join("");

            div.innerHTML = `
                <p><strong>ID:</strong> ${q.id}</p>
                <p><strong>Enunciado:</strong> ${q.enunciado}</p>
                <ul style="list-style-type:none; padding-left:0;">
                    ${alternativas}
                </ul>
                <p><strong>Disciplina:</strong> ${q.disciplina}</p>
                <p><strong>Dificuldade:</strong> ${q.dificuldade}</p>
            `;

            lista.appendChild(div);
        });
    } catch (erro) {
        console.error("Erro ao carregar questões:", erro);
        document.getElementById("lista").innerHTML =
            "<p>Erro ao carregar questões. Tente novamente mais tarde.</p>";
    }
}

// Carrega as questões assim que a página abre
carregarQuestoes();
