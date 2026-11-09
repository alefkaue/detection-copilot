# ADR-0001: Qual projeto construir

- **Status:** aceita
- **Data:** 2026-11-08

## Contexto

Quero um projeto de longo prazo (~2 meses, 2–3 h/dia) que:
- seja de **segurança defensiva**, a área em que atuo;
- use o modelo **Qwen local** (Ollama) e inclua **treino de verdade** (fine-tuning);
- produza resultados **mensuráveis** para mostrar em portfólio e LinkedIn;
- caiba no hardware: GPU AMD de 8 GB para inferência e Colab grátis para treino.

## Alternativas consideradas

| Opção | Prós | Contras |
|---|---|---|
| **Copiloto de Detection Engineering** (relatório → regra Sigma) | Métrica objetiva (a regra dispara no log do ataque?); dataset público grande (SigmaHQ); função muito demandada; o antes × depois do treino fica claro | Precisa de pipeline de validação; logs normais para medir falso positivo têm de ser gerados |
| Analista SOC nível 1 (Wazuh + Suricata) | Muito completo; parece trabalho real de SOC | Mais infraestrutura (SIEM, IDS, VMs); treino menos central; gabarito mais difícil |
| Detector de golpes PT-BR | Nicho brasileiro; dataset próprio seria contribuição original | Dataset precisa ser construído do zero; avaliação mais subjetiva |
| Revisor de segurança de código | Bom para AppSec/DevSecOps | Muitas ferramentas prontas; menos diferenciado |

## Decisão

**Copiloto de Detection Engineering.** O modelo recebe a descrição de um comportamento malicioso e gera uma regra Sigma, que é validada automaticamente em três testes:

1. **Sintaxe:** é Sigma válido (pySigma)?
2. **Detecção:** dispara no log `.evtx` do ataque correspondente (Zircolite)?
3. **Precisão:** fica quieta em logs normais (sem falso positivo)?

**Métrica principal:** porcentagem de regras que passam nos três testes, medida no modelo base (linha de base) e depois de cada rodada de treino.

## Consequências

- O primeiro trabalho pesado é o **juiz** (o pipeline de validação), não o modelo. Sem juiz, não há como medir o treino.
- O projeto pode crescer depois para o Analista SOC: as regras geradas alimentariam um SIEM.
- Atribuição obrigatória ao SigmaHQ (DRL 1.1) no README e no modelo publicado.
