from typing import Dict, List, Optional, Tuple
import json
import os
import re
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

    @classmethod
    def from_dict(cls, data: Dict) -> 'QuestionEvaluation':
        """Cria uma instância de QuestionEvaluation a partir de um dicionário"""
        return cls(
            question=data['question'],
            transcribed_answer=data['transcribed_answer'],
            expected_answer=data['expected_answer'],
            score=data['score'],
            feedback=data['feedback']
        )

@dataclass
class InterviewEvaluation:
    candidate_name: str
    job_position: str
    evaluations: List[QuestionEvaluation]
    average_score: float

    @classmethod
    def from_dict(cls, data: Dict) -> 'InterviewEvaluation':
        """Cria uma instância de InterviewEvaluation a partir de um dicionário"""
        evaluations = [
            QuestionEvaluation.from_dict(eval_data) 
            for eval_data in data['evaluations']
        ]
        return cls(
            candidate_name=data['candidate_name'],
            job_position=data['job_position'],
            evaluations=evaluations,
            average_score=data['average_score']
        )

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

    def update_evaluation(self, new_evaluation: QuestionEvaluation) -> bool:
        """
        Atualiza ou adiciona uma nova avaliação à lista de avaliações.
        Retorna True se atualizou uma existente, False se adicionou nova.
        """
        # Procura por uma avaliação existente com a mesma pergunta
        for i, eval_item in enumerate(self.evaluations):
            if eval_item.question == new_evaluation.question:
                self.evaluations[i] = new_evaluation
                return True
                
        # Se não encontrou, adiciona nova avaliação
        self.evaluations.append(new_evaluation)
        return False

    def update_average_score(self):
        """Atualiza a média das notas"""
        if not self.evaluations:
            self.average_score = 0.0
        else:
            total_score = sum(e.score for e in self.evaluations)
            self.average_score = total_score / len(self.evaluations)

class InterviewEvaluator:
    def __init__(self):
        self.answer_evaluator = AnswerEvaluator()

    def parse_video_filename(self, filename: str) -> Tuple[str, str, int]:
        """
        Extrai informações do nome do arquivo de vídeo.
        Formato esperado: candidato_nome_cargo_q{numero}.mp4
        Exemplo: candidato_joao_frontend_q1.mp4
        
        Returns:
            Tuple[nome_candidato, cargo, numero_questao]
        """
        try:
            # Remove a extensão
            base_name = os.path.splitext(filename)[0]
            
            # Extrai o número da questão
            match = re.search(r'_q(\d+)$', base_name)
            if not match:
                raise ValueError(f"Número da questão não encontrado no arquivo: {filename}")
            question_number = int(match.group(1))
            
            # Remove o sufixo _qN
            parts = base_name[:match.start()].split('_')
            if len(parts) < 3:
                raise ValueError(f"Nome do arquivo inválido: {filename}")
            
            # O nome do candidato é o segundo elemento
            candidate_name = parts[1]
            
            # A vaga é o elemento antes do _qN
            job_position = parts[-1]
            
            return candidate_name, job_position, question_number
            
        except Exception as e:
            raise ValueError(f"Erro ao processar nome do arquivo {filename}: {str(e)}")

    def process_single_answer(
        self,
        video_filename: str,
        transcription: str,
        job_data: JobPosition,
        question_number: int
    ) -> Optional[QuestionEvaluation]:
        """
        Processa uma única resposta de vídeo.
        
        Args:
            video_filename: Nome do arquivo de vídeo
            transcription: Texto transcrito da resposta
            job_data: Dados da vaga com questões
            question_number: Número da questão (1-based)
            
        Returns:
            QuestionEvaluation ou None se houver erro
        """
        try:
            # Ajusta o índice para 0-based
            question_idx = question_number - 1
            
            if question_idx < 0 or question_idx >= len(job_data.questions):
                print(f"Número de questão inválido: {question_number}")
                return None
                
            question_data = job_data.questions[question_idx]
            
            # Avalia a resposta
            result = self.answer_evaluator.evaluate_answer(
                transcribed_answer=transcription,
                question=question_data.question,
                expected_answer=question_data.expected_answer
            )
            
            return QuestionEvaluation(
                question=question_data.question,
                transcribed_answer=transcription,
                expected_answer=question_data.expected_answer,
                score=result.score,
                feedback=result.feedback
            )
            
        except Exception as e:
            print(f"Erro ao processar resposta: {str(e)}")
            return None

    def evaluate_interview(
        self,
        video_filename: str,
        transcription: str,
        output_dir: str
    ) -> Optional[str]:
        """
        Avalia uma resposta individual e atualiza/cria o arquivo de avaliação.
        
        Args:
            video_filename: Nome do arquivo de vídeo (ex: candidato_joao_frontend_q1.mp4)
            transcription: Texto transcrito da resposta
            output_dir: Diretório para salvar a avaliação
            
        Returns:
            Caminho do arquivo JSON com os resultados ou None se houver erro
        """
        try:
            # Extrai informações do nome do arquivo
            candidate_name, job_position, question_number = self.parse_video_filename(video_filename)
            
            # Carrega as questões da vaga
            job_data = load_job_questions(job_position)
            if not job_data:
                print(f"Não foi possível carregar as questões para a vaga: {job_position}")
                return None
            
            # Processa a resposta individual
            evaluation = self.process_single_answer(
                video_filename,
                transcription,
                job_data,
                question_number
            )
            if not evaluation:
                return None
            
            # Tenta carregar avaliação existente ou cria nova
            output_path = os.path.join(
                output_dir,
                f"evaluation_{candidate_name}_{job_position}.json"
            )
            
            if os.path.exists(output_path):
                try:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        current_eval = InterviewEvaluation.from_dict(data)
                except Exception as e:
                    print(f"Erro ao carregar avaliação existente: {str(e)}")
                    return None
            else:
                # Cria nova avaliação
                current_eval = InterviewEvaluation(
                    candidate_name=candidate_name,
                    job_position=job_position,
                    evaluations=[],
                    average_score=0.0
                )
            
            # Atualiza ou adiciona a nova avaliação
            current_eval.update_evaluation(evaluation)
            
            # Atualiza a média
            current_eval.update_average_score()
            
            # Salva o resultado
            return current_eval.save_to_json(output_dir)
            
        except Exception as e:
            print(f"Erro ao avaliar entrevista: {str(e)}")
            return None 