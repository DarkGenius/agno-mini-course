import os, sys
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools

# загружаем переменные из файла .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

# создаем агента
agent = Agent(model=OpenRouter(id=id_model),    # подключение модели,
              description="Ты отвечаешь используя актуальные данные из интернета",  # а вот и цель агента!
              tools=[
                  DuckDuckGoTools(),            # инструмент поиска DuckDuckGo
                  Newspaper4kTools(),           # чтение статей в интернете
                  CalculatorTools(),            # калькулятор для точных вычислений
                  YFinanceTools()               # финансовые инструменты от Yahoo
              ],
              debug_mode=True)

# получение ответа
# print(agent.run("Сколько сейчас стоит акция Apple?").content)
print(agent.run("Сколько стоит биткоин прямо сейчас?").content)