import os, sys, json
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from dotenv import load_dotenv

# загружаем переменные из файла .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Ошибка: в файле .env отсутствует OPENAI_API_KEY")
id_model = os.getenv("ID_MODEL") or sys.exit("Ошибка: в файле .env отсутствует ID_MODEL")

def main():
    # создаем агента
    agent = Agent(model=OpenRouter(id=id_model))

    while question := input("User: ").strip():
        print("AI  :", agent.run(question).content)

def test_models():
    # читаем список моделей из файла
    with open("models.json", "r", encoding="utf-8") as f:
        models = json.load(f)

    # тестируем каждую модель
    question = "Привет! Какой сегодня день?"

    for i, model in enumerate(models, 1):
        model_id = model.get("id") or model.get("canonical_slug")
        model_name = model.get("name", "Unknown")

        print(f"\n{'='*80}")
        print(f"[{i}/{len(models)}] Тестирование модели: {model_name}")
        print(f"ID модели: {model_id}")
        print(f"{'='*80}")

        try:
            # создаем агента для текущей модели
            agent = Agent(model=OpenRouter(id=model_id))

            # задаем вопрос
            print(f"Вопрос: {question}")
            response = agent.run(question)
            print(f"Ответ: {response.content}")

        except Exception as e:
            print(f"Ошибка при тестировании модели: {e}")


# запускаем диалог
if __name__ == "__main__":
    # main()
    test_models()