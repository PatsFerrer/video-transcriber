from dotenv import load_dotenv
import os

load_dotenv()

def require_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"A variável de ambiente '{name}' não está definida no .env")
    return value

GROQ_API_KEY = require_env_var("GROQ_API_KEY")
GROQ_MODEL = require_env_var("GROQ_MODEL")
