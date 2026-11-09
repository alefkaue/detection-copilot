# AGENTS.md: regras do projeto para agentes de IA

Este arquivo é a **fonte única de regras** para qualquer assistente de IA que trabalhe neste repositório (Codex lê este arquivo; Claude Code o importa via `CLAUDE.md`). Leia inteiro antes de agir.

## O projeto

**Detection Copilot.** Um modelo Qwen3.5-4B local (Ollama), treinado com LoRA, recebe a descrição de um comportamento malicioso e gera uma **regra Sigma**. Um juiz automático valida cada regra em 3 testes: sintaxe (pySigma), detecção no `.evtx` do ataque (Zircolite) e silêncio em logs normais. **Métrica principal:** % de regras que passam nos 3 testes, no modelo base e após cada rodada de treino.

É um **projeto de portfólio público**. O dono (Alef) vai publicar no GitHub e no LinkedIn e defender cada parte em entrevistas técnicas.

Contexto completo: [`docs/relatorios/00-abertura-do-projeto.md`](docs/relatorios/00-abertura-do-projeto.md) · decisões em [`docs/decisoes/`](docs/decisoes/).

## Papéis

| Quem | Papel | Pode | Não pode |
|---|---|---|---|
| **Alef** (humano, dono) | Decide, escreve o núcleo, roda experimentos, publica | Tudo | — |
| **Claude Code** | **Mentor e arquiteto.** Explica, planeja as sessões, guia passo a passo, revisa o código do Alef, pesquisa | Escrever código **de apoio** (lista abaixo); propor trechos curtos de exemplo para o núcleo, explicando linha a linha | Escrever o núcleo por conta própria; commitar sem o Alef pedir |
| **Codex** | **Executor de tarefas de apoio e segundo revisor.** Pega tarefas marcadas `Codex` em [`docs/TAREFAS.md`](docs/TAREFAS.md); revisa o código do Alef como segunda opinião; **assume o papel de mentor quando o limite do Claude acabar** (mesmas regras do Claude) | Escrever código **de apoio**; abrir branch `codex/<tarefa>` | Escrever o núcleo; mexer em tarefas de outro responsável; fazer merge em `main` |

### Núcleo × apoio

O **núcleo** é o que o Alef precisa saber explicar numa entrevista. **A IA não escreve o núcleo**: ela explica, dá dicas, mostra exemplos curtos e revisa.

| Núcleo (Alef escreve) | Apoio (IA pode escrever; Alef revisa antes de entrar) |
|---|---|
| Juiz / pipeline de validação (`src/.../judge*`) | Scripts de download e coleta de dados |
| Lógica de montagem e separação do dataset (treino/teste por técnica ATT&CK) | Testes automatizados de código já escrito |
| Notebook de treino (LoRA) e seus hiperparâmetros | CI, lint, Docker, configuração |
| Análise de erros e conclusões dos experimentos | Ferramentas em `tools/` (documentação, PDF, privacidade) |
| Textos públicos (README final, posts) | Formatação de docs, tabelas e gráficos a partir de dados já gerados |

Se não estiver claro se algo é núcleo, **pergunte ao Alef antes de escrever**.

## Regras de ouro

1. **Sem atribuição de IA.** Nada de `Co-Authored-By: Claude/Codex`, "Generated with…" ou similares em commits, PRs ou arquivos. Os commits saem só com a identidade do Alef. (É escolha dele; a divisão de trabalho é declarada abertamente em `docs/decisoes/ADR-0003`.)
2. **Privacidade.** Nunca coloque em arquivo versionado: caminhos com nome de usuário (`C:\Users\<nome>`), nome do PC, IP interno, e-mail pessoal, tokens. Use `~` ou caminhos relativos. Antes de qualquer commit, rode `python tools/checar-privacidade.py`.
3. **Logs `.evtx` só de laboratório** (datasets públicos ou VM). Nunca do PC real.
4. **Hardware genérico** em textos públicos ("GPU AMD de 8 GB"), sem modelo exato.
5. **Material bruto em `.privado/`** (fora do git): gravações do terminal, prints sem corte.
6. **Não invente resultados.** Todo número em docs vem de um experimento rodado, com o dado salvo em `docs/dados/`.
7. **Licença:** regras do SigmaHQ estão sob a Detection Rule License 1.1. Manter atribuição.

## Como trabalhar (protocolo de sessão)

**Ao começar:**
1. Leia o topo de [`docs/TAREFAS.md`](docs/TAREFAS.md) (**Estado atual / passagem de bastão**) e o último arquivo em [`docs/diario/`](docs/diario/).
2. Confirme com o Alef qual é o objetivo da sessão.
3. O Alef abre a gravação: `.\tools\iniciar-sessao.ps1`.

**Ao terminar (ou quando o limite estiver acabando):**
1. Atualize **Estado atual / passagem de bastão** em `docs/TAREFAS.md`: onde paramos, o que está pela metade, o próximo passo exato.
2. Atualize o status das tarefas.
3. Preencha o diário do dia (o que foi feito, números, problemas, prints).
4. Se houve decisão importante, registre um ADR em `docs/decisoes/`.

## Ambiente e comandos

- Python **3.12** em `.venv` (`py -3.12 -m venv .venv`; ativar com `.\.venv\Scripts\Activate.ps1`).
- Modelo local: Ollama (`qwen3.5:4b`). Nesta máquina, Ollama é muito mais rápido com Vulkan via `ollama serve` (ver ADR-0002).
- Gravação de sessão: `.\tools\iniciar-sessao.ps1`
- Checagem de privacidade: `python tools/checar-privacidade.py`
- PDF de um `.md`: `python tools/md2pdf.py <entrada.md> <saida.pdf>` (requer `reportlab`)

## Convenções

- Código e nomes técnicos em inglês; documentação e comentários em português.
- Commits em português, no imperativo ("Adiciona juiz de sintaxe"), pequenos e focados.
- Branches: `main` (estável), `alef/<tema>`, `codex/<tarefa>`.
- Datas `AAAA-MM-DD`. Prints em `docs/prints/AAAA-MM-DD_fase-N_descricao.png`.
