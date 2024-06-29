import requests
import json
import time


def get_vacancies():

    # Получаем список компаний, вакансии которых будем парсить
    with open("data/companies.json", "r", encoding="utf-8") as file:
        companies = json.load(file)

    # Записываем вакансии компаний в отдельные json файлы
    for company_name, company_id in companies.items():
        print(f"Парсим вакансии по компании: {company_name}")

        with open(f"data/{company_name}_vacancies.json", "w", encoding="utf-8") as file:

            company_vacancies = []
            for page in range(20):
                data = (requests.get(
                    f"https://api.hh.ru/vacancies?employer_id={company_id}&area=113&per_page=100&page={page}")).json()

                # print(f"https://api.hh.ru/vacancies?employer_id={company_id}&area=113&per_page=100&page={page}")

                try:
                    company_vacancies.extend(data['items'])
                except KeyError as error:
                    print(error)
                    continue

                print(f"Страница = {page}")

            json.dump(company_vacancies, file, sort_keys=False, indent=4,
                      ensure_ascii=False)

            # Таймаут чтобы не превырашать лимит запросов (просит каптчу, если превысить)
            time.sleep(5)
