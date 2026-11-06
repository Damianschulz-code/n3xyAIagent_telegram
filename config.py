import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_base_url: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    ai_model: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    system_prompt: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are a helpful, clear, and professional assistant. "
        "Answer in the same language as the user.",
    )
    database_path: str = os.getenv("DATABASE_PATH", "data/bot.db")
    history_limit: int = int(os.getenv("HISTORY_LIMIT", "16"))
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "3500"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "700"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
