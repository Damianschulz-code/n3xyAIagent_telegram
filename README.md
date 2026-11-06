# N3XY AI Agent

A portfolio-ready Telegram AI assistant built with Python, Aiogram 3, SQLite, and an OpenAI-compatible API.

## Features

- Telegram bot interface with `/start`, `/help`, `/about`, and `/reset`
- AI-powered text conversations
- Per-user conversation history stored in SQLite
- Configurable system prompt, model, temperature, and token limit
- OpenAI-compatible API endpoint configuration
- Docker and Docker Compose support
- Environment-based secrets (no API keys committed to Git)

## Requirements

- Python 3.12+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- An API key from an OpenAI-compatible AI provider

## Run locally

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/n3xy-ai-agent.git
   cd n3xy-ai-agent
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows PowerShell
   # .venv\\Scripts\\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Add your `TELEGRAM_BOT_TOKEN` and `AI_API_KEY` to `.env`.
   Never commit `.env` or share your API keys.

5. Start the bot:

   ```bash
   python bot.py
   ```

## Run with Docker

```bash
cp .env.example .env
# Edit .env and add your credentials
docker compose up --build -d
docker compose logs -f
```

Stop the service:

```bash
docker compose down
```

## Configuration

| Variable | Description | Default |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | — |
| `AI_API_KEY` | AI provider API key | — |
| `AI_BASE_URL` | OpenAI-compatible API base URL | `https://api.openai.com/v1` |
| `AI_MODEL` | Model identifier | `gpt-4o-mini` |
| `SYSTEM_PROMPT` | Agent's behavior instructions | Helpful assistant |
| `HISTORY_LIMIT` | Number of recent messages sent as context | `16` |
| `MAX_MESSAGE_LENGTH` | Maximum accepted user message length | `3500` |
| `MAX_TOKENS` | Maximum generated tokens | `700` |
| `TEMPERATURE` | Response creativity | `0.7` |
| `DATABASE_PATH` | SQLite database location | `data/bot.db` |

## Project structure

```text
n3xy-ai-agent/
├── ai_client.py       # AI provider integration
├── bot.py             # Telegram handlers and application entry point
├── config.py          # Environment configuration
├── database.py        # SQLite persistence
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env.example
├── .gitignore
└── README.md
```

## Architecture

1. Telegram updates are received by Aiogram polling.
2. The bot stores the user's message in SQLite.
3. Recent conversation history is loaded and sent to the configured AI API.
4. The assistant response is stored and returned to Telegram.

## Security notes

- Secrets are loaded from environment variables.
- `.env` and the SQLite database are excluded from Git.
- Do not expose bot tokens or AI API keys in screenshots, logs, or source code.
- For production use, add per-user quotas, abuse monitoring, backups, and webhook deployment behind HTTPS.

## License

MIT — see [LICENSE](LICENSE).
