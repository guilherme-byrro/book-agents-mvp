# 📚 Book Agents MVP

Sistema de agentes de IA para geração de conteúdo narrativo usando Ollama e Llama 3.1.

## ✨ Características

- 🤖 **Agentes Inteligentes**: Writer, Planner e Editor com IA
- 🔄 **Sistema Híbrido**: IA quando disponível, fallback rule-based sempre funcional
- 🌐 **Interface Web**: Interface Gradio moderna e intuitiva
- 📋 **Planos Dinâmicos**: Adaptação automática ao brief fornecido
- 🛠️ **Diagnóstico Integrado**: Script para troubleshooting do Ollama
- ⚡ **Recuperação Robusta**: Tratamento inteligente de timeouts e erros

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8+**
2. **Ollama** instalado e rodando
3. **Modelo Llama 3.1** (ou compatível)

### Setup

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/guilherme-byrro/book-agents-mvp.git
   cd book-agents-mvp
   ```

2. **Crie ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Ollama:**
   ```bash
   # Instalar modelo
   ollama pull llama3.1
   
   # Iniciar serviço
   ollama serve
   ```

## 🎯 Uso

### Interface Web (Recomendado)

```bash
python gradio_app.py
```

Acesse: http://localhost:7860

### Linha de Comando

```bash
python app.py --brief "Escreva um encontro tenso no MASP entre Ivana e Dr. Manoel, noite chuvosa."
```

### Diagnóstico

```bash
python diagnose_ollama.py
```

## 📁 Estrutura do Projeto

```
book-agents-mvp/
├── agents/
│   ├── writer.py      # Agente escritor com IA
│   ├── planner.py     # Agente planejador
│   └── editor.py      # Agente editor
├── engine/
│   └── llm.py         # Interface com Ollama
├── data/
│   ├── style_guide.md # Guia de estilo
│   └── canon/         # Dados do projeto
├── output/            # Cenas geradas
├── app.py            # Interface linha de comando
├── gradio_app.py     # Interface web
├── diagnose_ollama.py # Script de diagnóstico
├── config.yaml       # Configuração do modelo
└── requirements.txt  # Dependências
```

## ⚙️ Configuração

### config.yaml
```yaml
provider:
  name: ollama
  model: llama3.1  # ou llama3.1:8b para modelo menor
```

### Modelos Recomendados

- **llama3.1** - Qualidade máxima (requer mais RAM)
- **llama3.1:8b** - Equilibrio qualidade/performance
- **llama3.1:7b** - Mais rápido, menos RAM

## 🔧 Troubleshooting

### Ollama não conecta
```bash
# Verificar se está rodando
ollama list

# Iniciar serviço
ollama serve
```

### Timeout na geração
- Use modelo menor: `ollama pull llama3.1:8b`
- Feche outros programas pesados
- Aumente RAM disponível

### Modelo não encontrado
```bash
ollama pull llama3.1
```

## 🎨 Exemplos de Briefs

- "Escreva um encontro tenso no MASP entre Ivana e Dr. Manoel, noite chuvosa."
- "Crie uma cena de suspense em uma biblioteca antiga, com dois personagens discutindo um segredo."
- "Descreva um diálogo emotivo entre pai e filha em um café movimentado de São Paulo."
- "Escreva uma cena de ação em um metrô lotado durante o horário de rush."

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- [Ollama](https://ollama.ai/) - Plataforma de modelos locais
- [Gradio](https://gradio.app/) - Interface web para ML
- [Llama 3.1](https://llama.meta.com/) - Modelo de linguagem da Meta

---

**Desenvolvido com ❤️ usando IA e Python**
