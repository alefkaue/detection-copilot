# Detection Copilot

> 🚧 **Em construção**: projeto iniciado em novembro de 2026 e desenvolvido em público.

Um modelo de IA **local** (Qwen 4B via Ollama), **treinado** para transformar a descrição de um comportamento malicioso numa **regra de detecção Sigma**, e um juiz automático que testa cada regra antes de entregá-la:

1. **Sintaxe:** é uma regra Sigma válida?
2. **Detecção:** dispara no log real do ataque?
3. **Precisão:** fica quieta em logs normais?

A métrica principal é a porcentagem de regras que passam nos três testes, medida no modelo **sem treino** e depois de **cada rodada de treino**.

## Status

| Fase | Status |
|---|---|
| 0. Fundação | em andamento |
| 1. Dataset | — |
| 2. Juiz + linha de base | — |
| 3. Primeiro treino (LoRA) | — |
| 4. Análise de erros | — |
| 5. Produto (MCP + CLI) | — |
| 6. Lab ao vivo | — |

## Documentação

Tudo é registrado em [`docs/`](docs/README.md): diário de cada sessão, decisões de arquitetura (ADRs), fontes, dados dos experimentos e relatórios em PDF.

- [Abertura do projeto (PDF)](docs/relatorios/00-abertura-do-projeto.pdf)
- [Decisões](docs/decisoes/)
- [Diário](docs/diario/)

## Uso de IA no desenvolvimento

O projeto usa assistentes de IA (Claude Code e Codex) de forma declarada: arquitetura, revisão e tarefas de apoio. O núcleo (juiz de validação, dataset, treino e análise) é escrito por mim. Detalhes em [ADR-0003](docs/decisoes/ADR-0003-divisao-de-trabalho.md).

## Licença

Código sob [MIT](LICENSE). As regras de referência do [SigmaHQ](https://github.com/SigmaHQ/sigma) seguem a *Detection Rule License 1.1*, com a devida atribuição.
