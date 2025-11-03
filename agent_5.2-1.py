import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

# загружаем переменные из файла .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

# создаём память агента в базе данных SQLite
db = SqliteDb(db_file="data.db")

# создаём агента с подключенной памятью
agent = Agent(
    model=OpenRouter(id=id_model),      # подключение модели
    session_id="dialog",                # уникальный id сессии для сохранения диалога
    db=db,                              # подключаем память
    add_history_to_context=True,        # разрешаем запоминание новых сообщений
    num_history_runs=10,                # число прошлых сообщений для генерации ответа (0 - все сообщения)
)

# запускаем диалог
if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content)