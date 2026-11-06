import os
import aiosqlite
from datetime import datetime, timezone

class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    async def initialize(self) -> None:
        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    created_at TEXT NOT NULL
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            await db.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_user_id_id "
                "ON messages(user_id, id)"
            )
            await db.commit()

    async def ensure_user(self, user_id: int) -> None:
        now = datetime.now(timezone.utc).isoformat()
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users(user_id, created_at) VALUES (?, ?)",
                (user_id, now),
            )
            await db.commit()

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO messages(user_id, role, content, created_at) "
                "VALUES (?, ?, ?, ?)",
                (user_id, role, content, now),
            )
            await db.commit()

    async def get_history(self, user_id: int, limit: int) -> list[dict[str, str]]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute(
                "SELECT role, content FROM messages "
                "WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            )
            rows = await cursor.fetchall()
        rows.reverse()
        return [{"role": role, "content": content} for role, content in rows]

    async def clear_history(self, user_id: int) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
            await db.commit()
