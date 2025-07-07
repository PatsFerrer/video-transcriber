from typing import Dict, List, Optional
import os
import json
from dataclasses import dataclass

@dataclass
class JobQuestion:
    question: str
    expected_answer: str
    weight: float = 1.0

@dataclass
class JobPosition:
    name: str
    questions: List[JobQuestion]

    @classmethod
    def from_dict(cls, data: Dict) -> 'JobPosition':
        """
        Cria uma instância de JobPosition a partir de um dicionário.
        """
        questions = [
            JobQuestion(
                question=q["question"],
                expected_answer=q["expected_answer"],
                weight=q.get("weight", 1.0)
            )
            for q in data.get('questions', [])
        ]
        return cls(
            name=data['name'],
            questions=questions
        )

def extract_job_position(filename: str) -> Optional[str]:
    """
    Extrai o nome da vaga do nome do arquivo.
    Exemplo: 'candidato_joao_frontend_q1.mp4' -> 'frontend'
    """
    try:
        # Remove a extensão e split por underscore
        parts = os.path.splitext(filename)[0].split('_')
        # A vaga está antes do _qN
        for i, part in enumerate(parts):
            if part.startswith('q') and part[1:].isdigit():
                return parts[i-1].lower()
        return None
    except Exception:
        return None

def load_job_questions(job_position: str) -> Optional[JobPosition]:
    """
    Carrega as questões para uma determinada vaga.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    questions_path = os.path.join(
        base_dir, 
        'data', 
        'job_positions', 
        f'{job_position}.json'
    )
    
    try:
        with open(questions_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return JobPosition.from_dict(data)
    except FileNotFoundError:
        print(f"Arquivo de questões não encontrado para a vaga: {job_position}")
        return None
    except Exception as e:
        print(f"Erro ao carregar questões da vaga {job_position}: {str(e)}")
        return None 