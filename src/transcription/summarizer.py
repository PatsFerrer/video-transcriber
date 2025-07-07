from config import GROQ_MODEL
from .groq_client import client


def summarize_text(text: str, verbose: bool = False) -> str:
    """
    Chama a API do Groq para resumir um texto.
    Args:
        text (str): Texto a ser resumido.
        verbose (bool): Se True, mostra o progresso da geração.
    Returns:
        str: Resumo gerado.
    """
    system_prompt = """Você é um especialista em avaliação de entrevistas técnicas para desenvolvedores.

    IMPORTANTE - ERROS DE TRANSCRIÇÃO:
    A resposta do candidato foi obtida através de transcrição automática, que pode conter erros, especialmente em termos técnicos.
    Ao avaliar, considere possíveis erros de transcrição e foque no entendimento conceitual demonstrado.

    Seu papel é analisar e resumir respostas de candidatos, focando em:

    1. Principais conceitos técnicos mencionados
    2. Nível de profundidade do conhecimento demonstrado
    3. Clareza e estrutura da explicação
    4. Exemplos práticos ou casos de uso citados
    5. Possíveis mal-entendidos ou confusões conceituais

    Ao resumir, mantenha:
    - Objetividade na análise
    - Foco nos pontos técnicos relevantes
    - Identificação clara de pontos fortes e fracos
    - Linguagem profissional e técnica
    - Brevidade sem perder informações cruciais

    Evite:
    - Julgamentos pessoais
    - Informações redundantes
    - Detalhes não técnicos irrelevantes
    """

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": text},
        ],
        temperature=0.3,  # Baixa temperatura para respostas mais consistentes
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    summary = ""
    for chunk in response:
        part = chunk.choices[0].delta.content or ""
        summary += part
        if verbose:
            print(part, end="")
    return summary
