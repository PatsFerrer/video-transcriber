from typing import Dict
from dataclasses import dataclass
from config import GROQ_MODEL
from transcription.groq_client import client

@dataclass
class EvaluationResult:
    score: float
    feedback: str

class AnswerEvaluator:
    def evaluate_answer(
        self, 
        transcribed_answer: str, 
        question: str, 
        expected_answer: str
    ) -> EvaluationResult:
        """
        Avalia uma resposta transcrita comparando com a resposta esperada usando IA.
        
        Args:
            transcribed_answer: Resposta transcrita do candidato
            question: Pergunta original
            expected_answer: Resposta esperada/ideal
            
        Returns:
            EvaluationResult com nota (0-10) e feedback
        """
        prompt = f"""Você é um avaliador especialista que analisa respostas de candidatos em entrevistas técnicas.

Pergunta original: "{question}"

Resposta esperada: "{expected_answer}"

Resposta do candidato (transcrita): "{transcribed_answer}"

Compare a resposta do candidato com a resposta esperada e forneça:
1. Uma nota de 0 a 10, onde:
   - 0-2: Resposta totalmente incorreta ou fora do contexto
   - 3-4: Resposta parcialmente relacionada, mas com graves falhas
   - 5-6: Resposta básica, mas aceitável
   - 7-8: Boa resposta, com alguns pontos de melhoria
   - 9-10: Excelente resposta, completa e precisa
   
2. Um feedback construtivo explicando:
   - Pontos positivos da resposta
   - O que faltou ou poderia ser melhorado
   - Por que a nota foi atribuída

Retorne APENAS um JSON com este formato exato:
{{"score": float, "feedback": "string"}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um avaliador técnico especialista."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Baixa temperatura para respostas mais consistentes
            max_completion_tokens=1024
        )

        try:
            # Converte a resposta para JSON
            import json
            result = json.loads(response.choices[0].message.content)
            
            return EvaluationResult(
                score=float(result["score"]),
                feedback=result["feedback"]
            )
        except Exception as e:
            print(f"Erro ao processar resposta da IA: {str(e)}")
            # Retorna uma avaliação de erro
            return EvaluationResult(
                score=0.0,
                feedback="Erro ao avaliar resposta. Por favor, tente novamente."
            ) 