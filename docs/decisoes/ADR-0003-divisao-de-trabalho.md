# ADR-0003: Como o trabalho é dividido (humano × IA)

- **Status:** aceita (revisada em 2026-11-08 para detalhar o papel do Codex)
- **Data:** 2026-11-08

## Contexto

O projeto é construído com dois assistentes de IA, Claude Code e Codex, que têm **limites de uso** independentes. Para que o projeto represente o meu trabalho, e para que eu consiga defender cada parte numa entrevista técnica, a divisão precisa ser explícita. Também precisa estar escrita **num lugar que os dois agentes leiam**, para que um continue de onde o outro parou.

## Decisão

| Quem | Papel |
|---|---|
| **Eu (Alef)** | Decisões; escrevo o **núcleo**: juiz de validação, montagem e separação do dataset, treino e análise de erros; rodo experimentos; escrevo os textos públicos |
| **Claude Code** | **Mentor e arquiteto:** planeja as sessões, me guia passo a passo, explica, revisa meu código, pesquisa |
| **Codex** | **Executor de tarefas de apoio e segundo revisor.** Faz tarefas delimitadas marcadas para ele no quadro (scripts de coleta, testes, CI, hooks) e dá uma segunda opinião nas revisões. **Quando o limite do Claude acaba, o Codex assume o papel de mentor**, com as mesmas regras |

O que é **núcleo** e o que é **apoio** está listado em [`AGENTS.md`](../../AGENTS.md). Regra geral: a IA não escreve o núcleo. Ela explica, dá dicas, mostra trechos curtos de exemplo e revisa.

**Regra:** nenhum código entra no repositório sem que eu tenha lido e entendido.

### Mecanismos

- **`AGENTS.md`**: fonte única das regras. O Codex lê o arquivo nativamente; o Claude Code o importa via `CLAUDE.md`.
- **`docs/TAREFAS.md`**: quadro com responsável por tarefa e uma seção de **passagem de bastão**, atualizada ao fim de toda sessão (onde paramos e qual o próximo passo exato).
- **Branches:** o Codex trabalha em `codex/<tarefa>`; o merge em `main` é sempre meu, depois de revisar.
- **Diário** (`docs/diario/`): registra o que cada sessão produziu, o que deixa o processo transparente.

**Ritmo:** 2–3 horas por dia.

## Consequências

- O avanço é mais lento do que se a IA escrevesse tudo, mas o conhecimento fica comigo.
- A troca entre agentes não perde contexto, porque o estado fica nos arquivos, não na memória de uma conversa.
- Os commits saem só com a minha identidade; o uso de IA fica declarado aqui e no README.
