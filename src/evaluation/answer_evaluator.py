from typing import Dict
from dataclasses import dataclass
import json
from config import GROQ_MODEL
from transcription.groq_client import client


@dataclass
class EvaluationResult:
    score: float
    feedback: str


class AnswerEvaluator:
    def sanitize_text(self, text: str) -> str:
        """
        Sanitiza o texto para uso seguro no prompt.
        Remove ou escapa caracteres que podem causar problemas no JSON.
        """
        # Remove caracteres de controle e normaliza quebras de linha
        cleaned = text.replace("\\", "\\\\").replace('"', '\\"')
        return cleaned.strip()

    def evaluate_answer(
        self, transcribed_answer: str, question: str, expected_answer: str
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
        # Sanitiza os textos
        safe_question = self.sanitize_text(question)
        safe_expected = self.sanitize_text(expected_answer)
        safe_answer = self.sanitize_text(transcribed_answer)

        prompt = f"""Você é um avaliador especialista que analisa respostas de candidatos em entrevistas técnicas.

        Pergunta original: "{safe_question}"

        Resposta esperada: "{safe_expected}"

        Resposta do candidato (transcrita): "{safe_answer}"

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

        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um avaliador técnico especialista.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,  # Baixa temperatura para respostas mais consistentes
                max_completion_tokens=1024,
            )

            # Verifica se a resposta é válida
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Resposta vazia do modelo")

            # Tenta fazer o parse do JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Erro no JSON retornado pelo modelo: {content}")
                raise e

            # Valida os campos necessários
            if "score" not in result or "feedback" not in result:
                raise ValueError(
                    f"Resposta do modelo não contém os campos necessários: {result}"
                )

            return EvaluationResult(
                score=float(result["score"]), feedback=result["feedback"]
            )

        except Exception as e:
            print(f"Erro ao processar resposta da IA: {str(e)}")
            # Retorna uma avaliação de erro
            return EvaluationResult(
                score=0.0,
                feedback=f"Erro ao avaliar resposta: {str(e)}. Por favor, tente novamente.",
            )
