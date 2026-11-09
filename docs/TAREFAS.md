# Quadro de tarefas

## Estado atual / passagem de bastão

> **Atualize esta seção ao fim de toda sessão.** É o que o próximo agente (ou o próprio Alef amanhã) lê primeiro.

- **Data:** 2026-11-08
- **Fase:** 0 (fundação). Terreno pronto; trabalho de verdade começa na próxima sessão.
- **Onde paramos:**
  - Repositório git criado (identidade noreply do Alef) e publicado no GitHub: `alefkaue/detection-copilot`.
  - `.venv` com Python 3.12 criado (vazio, sem dependências instaladas ainda).
  - Docs, papéis (`AGENTS.md`) e ferramentas de documentação prontos.
- **Próximo passo exato (sessão com Alef + Claude + Codex):**
  1. **Codex** faz **F0-03** (script de download do SigmaHQ e do EVTX-ATTACK-SAMPLES) na branch `codex/f0-03-download`. Alef revisa.
  2. **Alef** faz **F0-04** (primeira detecção com o Zircolite), guiado pelo Claude, **com print**.
- **Bloqueios:** nenhum.

## Legenda

Responsável: **Alef** · **Claude** · **Codex** · Status: `a fazer` · `fazendo` · `revisão` · `feito`

Tarefas de **núcleo** são sempre do Alef (ver `AGENTS.md`). Codex só pega tarefas marcadas como dele.

## Fase 0: fundação

| ID | Tarefa | Responsável | Status | Notas |
|---|---|---|---|---|
| F0-00 | Planejamento, pesquisa e sistema de documentação | Claude | feito | `docs/`, ADRs 0001–0003, PDF de abertura |
| F0-01 | `git init`, identidade noreply do repo, `.venv` com Python 3.12 | Claude | feito | Feito pelo Claude a pedido do Alef (setup, não é núcleo) |
| F0-02 | Primeiro commit (docs + regras) e repositório público no GitHub | Claude | feito | Privacidade checada antes do push |
| F0-03 | Script que baixa o SigmaHQ e o EVTX-ATTACK-SAMPLES para `external/` (fora do git), com versão/commit fixos | Codex | a fazer | Apoio. Registrar origem e licença de cada fonte em `docs/pesquisa/datasets.md` |
| F0-04 | Instalar o Zircolite e rodar **uma** regra Sigma sobre **um** `.evtx` de ataque | Alef | a fazer | Primeira detecção. **Tirar print** |
| F0-05 | Hook de pre-commit que roda `checar-privacidade.py` | Codex | a fazer | Apoio |
| F0-06 | Diário do dia, print revisado e post #1 no LinkedIn ("começando o projeto") | Alef | a fazer | Claude pode revisar o texto |

## Fase 1: dataset (detalhar ao concluir a Fase 0)

| ID | Tarefa | Responsável | Status | Notas |
|---|---|---|---|---|
| F1-01 | Explorar o SigmaHQ: quantas regras por logsource / técnica ATT&CK | Alef | a fazer | Notebook de exploração |
| F1-02 | Definir o formato do exemplo de treino (entrada → regra) | Alef | a fazer | Núcleo. Registrar em ADR |
| F1-03 | Separação treino/teste por técnica ATT&CK | Alef | a fazer | Núcleo |
| F1-04 | Testes automatizados do gerador de dataset | Codex | a fazer | Apoio, depois que F1-02/03 existirem |
