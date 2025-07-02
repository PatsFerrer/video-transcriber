from typing import Dict, List, Optional
import json
import os
from dataclasses import dataclass, asdict

from .job_matcher import JobPosition, extract_job_position, load_job_questions
from .answer_evaluator import AnswerEvaluator, EvaluationResult

@dataclass
class QuestionEvaluation:
    question: str
    transcribed_answer: str
    expected_answer: str
    score: float
    feedback: str

@dataclass
class InterviewEvaluation:
    candidate_name: str
    job_position: str
    evaluations: List[QuestionEvaluation]
    average_score: float

    def to_dict(self) -> Dict:
        return asdict(self)

    def save_to_json(self, output_dir: str) -> str:
        """Salva a avaliação em JSON e retorna o caminho do arquivo"""
        output_path = os.path.join(
            output_dir,
            f"evaluation_{self.candidate_name}_{self.job_position}.json"
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
            
        return output_path

class InterviewEvaluator:
    def __init__(self):
        self.answer_evaluator = AnswerEvaluator()

    def extract_candidate_name(self, filename: str) -> str:
        """Extrai o nome do candidato do nome do arquivo"""
        parts = os.path.splitext(filename)[0].split('_')
        # Assume que o nome está entre 'candidato' e a vaga
        return parts[1]

    def evaluate_interview(
        self,
        video_filename: str,
        transcription: str,
        output_dir: str
    ) -> Optional[str]:
        """
        Avalia uma entrevista completa e salva os resultados.
        
        Args:
            video_filename: Nome do arquivo de vídeo
            transcription: Texto transcrito da entrevista
            output_dir: Diretório para salvar a avaliação
            
        Returns:
            Caminho do arquivo JSON com os resultados ou None se houver erro
        """
        # Extrai informações do nome do arquivo
        job_position = extract_job_position(video_filename)
        if not job_position:
            print(f"Não foi possível extrair a vaga do arquivo: {video_filename}")
            return None

        # Carrega as questões da vaga
        job_data = load_job_questions(job_position)
        if not job_data:
            return None

        # Avalia cada questão
        evaluations = []
        total_score = 0.0

        for question in job_data.questions:
            # Por enquanto, vamos usar a transcrição completa para cada pergunta
            # TODO: Implementar separação inteligente das respostas por pergunta
            result = self.answer_evaluator.evaluate_answer(
                transcribed_answer=transcription,
                question=question.question,
                expected_answer=question.expected_answer
            )
            
            evaluations.append(QuestionEvaluation(
                question=question.question,
                transcribed_answer=transcription,
                expected_answer=question.expected_answer,
                score=result.score,
                feedback=result.feedback
            ))
            
            total_score += result.score

        # Calcula a média das notas
        average_score = total_score / len(job_data.questions) if job_data.questions else 0.0

        # Cria o resultado final
        evaluation = InterviewEvaluation(
            candidate_name=self.extract_candidate_name(video_filename),
            job_position=job_position,
            evaluations=evaluations,
            average_score=average_score
        )

        # Salva e retorna o caminho do arquivo
        return evaluation.save_to_json(output_dir) 