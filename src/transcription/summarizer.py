from config import GROQ_MODEL
from .groq_client import client

def summarize_text(text: str) -> str:
    """
    Chama a API do Groq para resumir um texto.
    Args:
        text (str): Texto a ser resumido.
    Returns:
        str: Resumo gerado.
    """
    response = client.chat.completions.create(
      model=GROQ_MODEL,
      messages=[
          {
              "role": "system",
              "content": "Você é um assistente de IA que resume textos longos em um resumo conciso e informativo.",
          },
          {"role": "user", "content": text},
      ],
      temperature=0.7,
      max_completion_tokens=1024,
      top_p=1,
      stream=True,
      stop=None,
  )

    summary = ""
    for chunk in response:
        summary += chunk.choices[0].delta.content or ""
        print(chunk.choices[0].delta.content or "", end="")
    
    return summary
