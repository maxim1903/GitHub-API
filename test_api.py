import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_USER = os.getenv('GITHUB_USER')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')

if not all([GITHUB_USER, GITHUB_TOKEN, REPO_NAME]):
    raise ValueError("Не все переменные окружения установлены. Проверьте файл .env.")

GITHUB_API_URL = "https://api.github.com/user/repos"


headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}


def create_repo():
    response = requests.post(
        GITHUB_API_URL,
        json={"name": REPO_NAME, "private": False},
        headers=headers
    )
    return response

def repo_exists():
    response = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}",
        headers=headers
    )
    return response.status_code == 200

def delete_repo():
    response = requests.delete(
        f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}",
        headers=headers
    )
    return response

def main():
    print("Создание репозитория...")
    create_response = create_repo()
    if create_response.status_code == 201:
        print(f"Репозиторий '{REPO_NAME}' успешно создан.")
    else:
        print(f"Ошибка при создании репозитория: {create_response.json()}")

    print("Проверка существования репозитория...")
    if repo_exists():
        print(f"Репозиторий '{REPO_NAME}' существует.")
    else:
        print(f"Репозиторий '{REPO_NAME}' не найден.")

    print("Удаление репозитория...")
    delete_response = delete_repo()
    if delete_response.status_code == 204:
        print(f"Репозиторий '{REPO_NAME}' успешно удален.")
    else:
        print(f"Ошибка при удалении репозитория: {delete_response.json()}")

if __name__ == "__main__":
    main()
