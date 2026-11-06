import httpx
from config import Settings

class AIClient:
    """Small client for APIs compatible with the OpenAI Chat Completions format."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.http = httpx.AsyncClient(
            base_url=settings.ai_base_url.rstrip("/") + "/",
            timeout=httpx.Timeout(45.0, connect=10.0),
            headers={
                "Authorization": f"Bearer {settings.ai_api_key}",
                "Content-Type": "application/json",
            },
        )

    async def complete(self, history: list[dict[str, str]]) -> str:
        if not self.settings.ai_api_key:
            raise RuntimeError("AI_API_KEY is not configured")

        messages = [{"role": "system", "content": self.settings.system_prompt}]
        messages.extend(history)

        response = await self.http.post(
            "chat/completions",
            json={
                "model": self.settings.ai_model,
                "messages": messages,
                "temperature": self.settings.temperature,
                "max_tokens": self.settings.max_tokens,
            },
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        if not content:
            raise RuntimeError("AI provider returned an empty response")
        return str(content).strip()

    async def close(self) -> None:
        await self.http.aclose()
