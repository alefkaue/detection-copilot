# ADR-0002: Ferramentas e ambiente

- **Status:** aceita (revisar ao fim da Fase 2)
- **Data:** 2026-11-08

## Decisões

| Item | Escolha | Por quê | Alternativas |
|---|---|---|---|
| Linguagem | **Python 3.12** | Bibliotecas de segurança e ML demoram a suportar o Python mais novo; o 3.12 é o mais compatível | 3.13 e 3.14 (instalados, mas com risco de faltar *wheels*) |
| Formato das regras | **Sigma** | Padrão aberto, convertido para qualquer SIEM (Splunk, Elastic, Sentinel…); mais de 3.000 regras públicas | Regras nativas de um SIEM (prendem a um fornecedor) |
| Validação de sintaxe | **pySigma** | Biblioteca oficial do projeto Sigma | Validação manual por schema |
| Execução das regras em logs | **Zircolite** | Python, lê Sigma YAML direto, roda sobre `.evtx` | Chainsaw, Hayabusa (Rust; bons, mas mais difíceis de integrar num pipeline Python) |
| Regras de referência | **SigmaHQ** | Maior repositório público, mantido pela comunidade | — |
| Logs de ataque | **EVTX-ATTACK-SAMPLES** (+ amostras do Hayabusa) | `.evtx` reais de técnicas ATT&CK conhecidas | Gerar todos em lab (fica para a Fase 6) |
| Modelo | **Qwen3.5-4B** via Ollama | Já roda localmente (~65 tokens/s com Vulkan); suportado pela Unsloth | `qwen3:4b` (mais lento: ignora `think=False`) |
| Treino | **Unsloth + LoRA bf16 no Google Colab** | GPU AMD no Windows não treina; a Unsloth suporta o Qwen3.5-4B no Colab grátis (~10 GB) e exporta GGUF | QLoRA (não recomendado para o Qwen3.5); Kaggle (alternativa ao Colab) |

## Pontos de atenção

- O Qwen3.5 exige `transformers` v5 no treino.
- Depois de exportar para GGUF, **manter o mesmo chat template e o mesmo token de fim**. Segundo a documentação, é a causa mais comum de queda de qualidade.
- No Colab com T4, a primeira compilação dos kernels do Qwen3.5 é lenta. Isso é esperado.
