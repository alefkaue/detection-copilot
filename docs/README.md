# Documentação do projeto

Registro de tudo o que acontece no projeto: decisões, experimentos, números, prints e relatórios.
É daqui que saem os posts do LinkedIn e o material para entrevistas.

## Estrutura

| Pasta | O que guarda | Quando atualizar |
|---|---|---|
| [`diario/`](diario/) | Um arquivo por sessão de trabalho: o que foi feito, problemas, decisões, próximos passos | Ao fim de cada sessão |
| [`decisoes/`](decisoes/) | ADRs (*Architecture Decision Records*): uma decisão importante por arquivo, com alternativas e motivo | Sempre que uma escolha difícil de desfazer for feita |
| [`pesquisa/`](pesquisa/) | Fontes lidas (artigos, ferramentas, datasets) com anotações | Ao pesquisar |
| [`dados/`](dados/) | Métricas e resultados em CSV/JSON (linha de base, cada rodada de treino…) | A cada experimento |
| [`prints/`](prints/) | Capturas de tela **já revisadas** (sem dados pessoais) | Durante as sessões |
| [`relatorios/`](relatorios/) | PDFs consolidados (abertura do projeto, fechamento de cada fase) | Ao fim de cada fase |

## Regras de privacidade (ler antes de publicar qualquer coisa)

Este é um projeto público de um profissional de segurança. **Nada sai do PC sem passar por esta lista:**

- [ ] Sem caminhos com nome de usuário (`C:\Users\<nome>\...`): troque por `~` ou `<projeto>`.
- [ ] Sem nome do computador, IP interno, MAC, SSID de Wi-Fi.
- [ ] Sem e-mail pessoal, tokens, chaves de API, cookies.
- [ ] Prints: só a janela relevante (nada de barra de tarefas, notificações, outras abas).
- [ ] Logs `.evtx`: **só de VM de laboratório**, nunca do PC real.
- [ ] Hardware descrito de forma genérica ("GPU AMD de 8 GB"), sem modelo exato.

O material bruto (gravações completas do terminal, prints sem corte) fica em `.privado/`,
que **não vai para o git** (está no `.gitignore`).

## Convenções

- **Datas** no formato `AAAA-MM-DD`.
- **Prints:** `prints/AAAA-MM-DD_fase-N_descricao.png` (ex.: `2026-11-09_fase-0_primeira-deteccao.png`).
- **Dados:** `dados/AAAA-MM-DD_experimento.csv`, sempre com um `.md` ao lado explicando as colunas.
- **Diário:** `diario/AAAA-MM-DD_dia-NN.md`.
- **Gravação do terminal:** no começo de cada sessão, rode `.\tools\iniciar-sessao.ps1`. Ele grava tudo em `.privado/terminal/`.
- **PDF:** `python tools/md2pdf.py <arquivo.md> docs/relatorios/<nome>.pdf`.

## Índice

- **Regras para agentes de IA e papéis:** [`AGENTS.md`](../AGENTS.md)
- **Quadro de tarefas e passagem de bastão:** [`TAREFAS.md`](TAREFAS.md)
- **Dia 00 (2026-11-08):** [escolha do projeto e checagem de viabilidade](diario/2026-11-08_dia-00.md)
- **ADR-0001:** [qual projeto construir](decisoes/ADR-0001-escolha-do-projeto.md)
- **ADR-0002:** [ferramentas e ambiente](decisoes/ADR-0002-ferramentas-e-ambiente.md)
- **ADR-0003:** [como o trabalho é dividido (Alef × Claude × Codex)](decisoes/ADR-0003-divisao-de-trabalho.md)
- **Fontes:** [pesquisa inicial](pesquisa/fontes.md)
- **Relatório:** [abertura do projeto (PDF)](relatorios/00-abertura-do-projeto.pdf)
