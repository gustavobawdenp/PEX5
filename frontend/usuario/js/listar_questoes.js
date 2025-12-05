console.log("JS CARREGOU!");

async function carregarQuestoes() {
    const params = new URLSearchParams(window.location.search);
    const disciplina = params.get("disciplina");

    console.log("Disciplina enviada:", disciplina);  // DEBUG

    document.getElementById("titulo").innerHTML = `Questões de ${disciplina}`;

    const questoes = await listarQuestoes({ disciplina });

    console.log("Resposta da API:", questoes);  // DEBUG

    const div = document.getElementById("lista");
    div.innerHTML = "";

    if (!questoes.length) {
        div.innerHTML = "<p>Sem questões para esta disciplina.</p>";
        return;
    }

    questoes.forEach((q, i) => {
        const bloco = document.createElement("div");
        bloco.className = "questao-card";

        bloco.innerHTML = `
            <h3>Questão ${i + 1}</h3>
            <p><strong>${q.enunciado}</strong></p>

            <p>A) ${q.alternativa_a}</p>
            <p>B) ${q.alternativa_b}</p>
            <p>C) ${q.alternativa_c}</p>
            <p>D) ${q.alternativa_d}</p>

            <p><strong>Correta:</strong> ${q.correta}</p>
        `;

        div.appendChild(bloco);
    });
}

carregarQuestoes();
