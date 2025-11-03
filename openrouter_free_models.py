# Назначение: получение списка бесплатных моделей с сайта OpenRouter.ai
#
import os
import json
import argparse
import requests
from dotenv import load_dotenv

# парсим аргументы командной строки
parser = argparse.ArgumentParser(description="Получение списка бесплатных моделей с OpenRouter.ai")
parser.add_argument("--save", nargs="?", const="models.json", default=None, metavar="FILENAME",
                    help="Сохранить ответ API в JSON файл (по умолчанию: models.json)")
args = parser.parse_args()

# загружаем токен из .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# отправляем запрос на OpenRouter
url = "https://openrouter.ai/api/v1/models"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(url, headers=headers)
response.raise_for_status() # добавляем проверку на ошибки запроса

# получаем данные ответа
response_data = response.json()
models = response_data.get("data", [])

# фильтруем только бесплатные модели
free_models_data = [m for m in models if m["name"].endswith("(free)")]

# сохраняем в файл, если указан аргумент --save
if args.save:
    with open(args.save, "w", encoding="utf-8") as f:
        json.dump(free_models_data, f, indent=2, ensure_ascii=False)
    print(f"Бесплатные модели сохранены в файл: {args.save} ({len(free_models_data)} моделей)\n")

# получаем отсортированный список FREE моделей для вывода в таблицу
free_models = sorted(
    [(m["name"], m["canonical_slug"], m["context_length"]) for m in free_models_data]
)

# красиво все выводим в виде таблицы
print(f"{'№':>3} | {'Название модели':45} | {'Код модели':45} | {'Контекст'}")
print("-" * 110)
for i, (name, slug, context) in enumerate(free_models, 1):
    print(f"{i:3} | {name:45} | {slug:45} | {context}")
