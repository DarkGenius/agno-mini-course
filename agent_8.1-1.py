import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

# загружаем переменные из файла .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

# создаём память агента в базе данных SQLite
db = SqliteDb(db_file="data_fin.db")

# локальный эмбеддер Agno на базе SentenceTransformers
embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",          # модель для эмбеддинга по умолчанию
)

# используем LanceDB как локальную векторную базу с гибридным поиском
vector_db = LanceDb(
    table_name="text_documents",    # имя таблицы для эмбеддингов
    uri="knowledge_fin",            # локальная папка/URI для LanceDB
    search_type=SearchType.hybrid,  # гибридный поиск: по смыслу + по ключевым словам
    embedder=embedder               # подключаем эмбеддер
)

# создание knowledge - объекта базы знаний
knowledge = Knowledge(vector_db=vector_db)

# добавляем в базу знаний книгу "Алиса в Стране Чудес" :)
knowledge.add_content(
    url="https://gist.githubusercontent.com/phillipj/4944029/raw/75ba2243dd5ec2875f629bf5d79f6c1e4b5a8b46/alice_in_wonderland.txt",
    skip_if_exists=True
)

# создаем агента со знаниями и инструментами
agent = Agent(model=OpenRouter(id=id_model),
              description="Ты - дружелюбный помощник, который при необходимости пользуется интернетом",
              tools=[
                  DuckDuckGoTools(),       # инструмент поиска DuckDuckGo
                  Newspaper4kTools(),      # чтение страниц в интернете
                  CalculatorTools(),       # калькулятор для точных вычислений
                  YFinanceTools()          # финансовые инструменты от Yahoo
              ],
              session_id="advance agent",  # уникальный id сессии для сохранения диалога
              db=db,                       # подключаем память
              add_history_to_context=True, # добавляем новые сообщения в контекст и запоминаем их
              num_history_runs=0,          # 0 - при ответе используем все сообщения
              knowledge=knowledge,         # подключаем базу знаний (файл с книгой)
              search_knowledge=True,       # разрешаем использование знаний в ответе
              )

# запускаем диалог
if __name__ == "__main__":
    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content.strip())

# Задай агенту следующие вопросы по порядку:
#
# 1. Привет! Меня зовут Максим, а кто ты?
# 2. Я увлекаюсь темой ИИ и занимаюсь созданием ИИ-агентов на Python.
# 3. Расскажи, ты знаешь настоящее имя Алисы из книги из твоей базы знаний?
# 4. Найди какой сейчас курс биткоина?
# 5. Расскажи кратко о чем эта статья https://habr.com/ru/amp/publications/950566/ ?
# 6. Исходя из наших разговоров расскажи, что ты обо мне знаешь.
