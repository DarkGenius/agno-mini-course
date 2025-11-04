import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from dotenv import load_dotenv

# загружаем переменные из файла .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

# локальный эмбеддер Agno на базе SentenceTransformers
embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",                  # лёгкая и быстрая модель для эмбеддинга по умолчанию
)

# используем LanceDB как локальную векторную базу с гибридным поиском
vector_db = LanceDb(
    table_name="text_documents",            # имя таблицы для эмбеддингов
    uri="lancedb_storage",                  # локальная папка/URI для LanceDB
    search_type=SearchType.hybrid,          # гибридный поиск: по смыслу + по ключевым словам
    embedder=embedder                       # подключаем эмбеддер
)

# создание knowledge - объекта базы знаний
knowledge = Knowledge(vector_db=vector_db)

# добавляем в базу знаний файл
knowledge.add_content(path="rag_data\\history.txt")

# создаем агента со знаниями
agent = Agent(
    model=OpenRouter(id=id_model),      # подключение модели
    knowledge=knowledge,                # подключаем базу знаний
    search_knowledge=True,              # разрешаем ее использование
    debug_mode=False                    # выключаем режим отладки (по умолчанию)
)

# запрос и получение ответа
print(agent.run("В каком городе проходила первая конференция Agno и сколько стран в ней участвовало?").content)