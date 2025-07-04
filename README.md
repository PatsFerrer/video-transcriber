# POC - Transcrição de Áudio de Vídeos

Este projeto é uma Prova de Conceito (POC) para extração e transcrição de áudio de vídeos com foco em entender como automatizar a geração de resumos com IA.

## Funcionalidades

- Extração de áudio de arquivos de vídeo
- Transcrição de áudio para texto com Whisper
- Captura de frames do vídeo
- Geração de resumo automático com LLM via Groq API

## Melhorias Recentes

- A transcrição agora **detecta automaticamente o idioma** falado no vídeo. Isso melhora a precisão em vídeos que contêm uma mistura de português e inglês.
- Separação do código em módulos reutilizáveis para facilitar manutenção e testes.

## Configuração do Ambiente

1. Crie um ambiente virtual:
```bash
python -m venv venv
```

2. Ative o ambiente virtual:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
.
├── input/              # Pasta para arquivos de vídeo de entrada
├── output/             # Pasta para transcrições, áudio extraído e frames
├── src/                # Código principal (main.py)
├── transcription/      # Módulos de transcrição, resumo e Groq API
├── tests/              # Testes unitários
├── config.py           # Configurações globais (ex: diretórios, modelo)
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

## Como Usar

1. Coloque seu arquivo de vídeo na pasta `input/`
2. Execute o script principal:
```bash
python src/main.py
```
3. A transcrição e o resumo serão salvos automaticamente na pasta `output/`

## Desenvolvimento

Para executar os testes:
```bash
pytest tests/
```
