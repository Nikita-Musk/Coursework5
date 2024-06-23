import requests
from src.constants import EMPLOYER_IDS, HH_URL


def employer_parser() -> list[dict]:
    """
    Парсит информацию о работадателях и вакансиях с HeadHunter API.

    Returns:
        list: Список словарей, содержащих информацию о работодателях и вакансиях.
    """
    employers_info: list[dict] = []
    for employer_id in EMPLOYER_IDS:
        # Формируем URL для запроса к API работодателя
        url: str = f"{HH_URL}{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            # Парсим JSON-ответ от API работодателя
            company_response = response.json()
            vacancies_url: str = company_response["vacancies_url"]
            vacancies: list[dict] = []
            # Итерируем по 2 страницам (можно изменить количество)
            for page in range(2):
                params = {"per_page": 100, "page": page}
                vacancies_response: dict = requests.get(vacancies_url, params=params).json()
                vacancies.extend(vacancies_response["items"])
            # Создаем словарь для хранения информации о работадателе и вакансиях
            employers_info.append({
                "company": {
                    "company_id": company_response["id"],
                    "name": company_response["name"],
                    "company_url": company_response["alternate_url"]
                },
                "vacancies": vacancies
            })
        else:
            print(f"Ошибка {response.status_code} при запросе к API компании")
    return employers_info


if __name__ == '__main__':
    emp = employer_parser()
    print(emp)