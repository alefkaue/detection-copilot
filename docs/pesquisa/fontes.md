# Fontes: pesquisa inicial (2026-11-08)

## Artigos

| Fonte | O que importa para este projeto |
|---|---|
| [OpenSOC-AI (arXiv 2604.26217)](https://arxiv.org/pdf/2604.26217) | LoRA no TinyLlama-1.1B para classificar logs e mapear ATT&CK; grande ganho com só ~450 exemplos de treino. Datasets e pesos publicados |
| [Fine-tuning de SLMs em logs multi-fonte (arXiv 2606.18190)](https://arxiv.org/pdf/2606.18190) | Qwen2.5-1.5B, Llama-3.2-3B e Phi-4-Mini com LoRA em 870 sessões rotuladas com ATT&CK; o treino melhorou todos os modelos em todas as métricas |
| [From Texts to Rules (USENIX Security 2026)](https://www.usenix.org/conference/usenixsecurity26/presentation/cai) | Gera regras Sigma a partir de relatórios de ameaça; LLMs genéricos falham por falta de conhecimento do domínio. **Referência principal** |
| [CORTEX (NeurIPS 2025)](https://neurips.cc/virtual/2025/137134) | Agentes colaborativos para triagem de alertas; menos falsos positivos que um agente único |
| [CyberLLM-FINDS (arXiv 2601.06779)](https://arxiv.org/pdf/2601.06779) | Fine-tuning por instruções + RAG + grafo para avaliação MITRE |
| [RedShell (arXiv 2604.11506)](https://arxiv.org/pdf/2604.11506) | LoRA com Unsloth em dataset pequeno; alerta sobre **desbalanceamento de táticas** entre treino e teste |
| [Workflow > tamanho do modelo](https://www.pulse.bot/ai/news/what-researchers-learned-about-building-an-llm-security-workflow-81e1c298-e7e1-4557-a91b-9c9987ce0ab4/) | LLM sem estrutura perdeu todos os alertas maliciosos; com consultas guiadas e *guardrails*, 93% de detecção |
| [Agentes LLM na triagem SOC N1](https://www.utupub.fi/items/52a15c8a-63ac-41bf-8f22-fc38690bfb29/full) | Avaliação de agentes no processo de triagem nível 1 |

## Modelos e treino

| Fonte | Nota |
|---|---|
| [Unsloth: fine-tuning do Qwen3.5](https://unsloth.ai/docs/models/qwen3.5/fine-tune) | Suporte oficial; 4B em LoRA bf16 cabe em ~10 GB; QLoRA não recomendado; exige `transformers` v5 |
| [Unsloth: Qwen3.5-4B GGUF](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF) | Versões quantizadas para o Ollama |
| [Guia passo a passo Qwen3.5-4B + Unsloth](https://ai-hpc.github.io/ai-hardware-engineer-roadmap/Phase%203%20-%20Artificial%20Intelligence/Track%20B%20-%20Agentic%20AI%20and%20ML%20Engineering/5.%20LLM%20Application%20Development/Qwen3.5-4B%20Unsloth%20Fine-Tuning/Guide/) | Roteiro de terceiros |
| [Adapter LoRA Qwen2.5-7B para Sigma](https://huggingface.co/jjhoada/qwen2.5-7b-sigma-generation-lora) | **Trabalho comparável:** 3.110 exemplos do SigmaHQ, 96% de JSON válido. Usa modelo 7B; o nosso é 4B, com validação por execução real |

## Ferramentas

| Fonte | Nota |
|---|---|
| [Zircolite](https://www.Github.com/wagga40/Zircolite) | Sigma YAML direto sobre `.evtx` (desde a v2.20.0); aceita pipelines do pySigma |
| [Chainsaw + Sigma](https://savitar.gitbook.io/mynotes/certifications-and-notes/blue-team/cdsa/yara-and-sigma-for-soc-analysts/hunting-evil-with-sigma-chainsaw-edition) | Alternativa em Rust; `chainsaw lint` valida regras |
| [Hayabusa rules](https://www.github.com/Yamato-Security/hayabusa-rules) | Inclui `.evtx` de exemplo para testar regras |

## Projetos open source relacionados (SOC com IA)

- [Wazuh MCP Server](https://mcpservers.org/servers/gensecaihq/wazuh-mcp-server): funciona com Qwen via Ollama, pode rodar sem internet
- [Security MCP Server Suite](https://solomonneas.dev/projects/security-mcp-servers): inclui Suricata
- [AiSOC](https://pasqualepillitteri.it/en/news/28903/aisoc-open-source-soc-ai-agents-github-en): plataforma SOC open source com MCP
- [Lab de triagem SOC com IA (blog)](https://desvert.github.io/blog/2026/03/04/building-an-ai-assisted-soc-triage-lab.html)
- [Wazuh AI SOC Lab (blog)](https://0xgunn.github.io/blog/project---wazuh-ai-soc-lab)
- [Tópico alert-triage no GitHub](https://github.com/topics/alert-triage)
