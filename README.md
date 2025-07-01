# POC - Transcrição de Áudio de Vídeos

Este projeto é uma Prova de Conceito (POC) para extração e transcrição de áudio de vídeos.

## Funcionalidades

- Extração de áudio de arquivos de vídeo
- Transcrição de áudio para texto
- Captura de frames do vídeo

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
├── output/            # Pasta para transcrições e frames
├── src/              # Código fonte
├── tests/            # Testes unitários
├── requirements.txt  # Dependências do projeto
└── README.md        # Este arquivo
```

## Como Usar

1. Coloque seu arquivo de vídeo na pasta `input/`
2. Execute o script principal:
```bash
python src/main.py
```
3. A transcrição será salva na pasta `output/`

## Desenvolvimento

Para executar os testes:
```bash
pytest tests/
```
