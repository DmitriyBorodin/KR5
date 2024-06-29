import requests
import json
import time
import psycopg2


def get_vacancies():
    """
    Получаем список компаний, парсим вакансий каждой компании в отдельный файл
    """

    # Получаем список компаний
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


def create_vacancies_table():
    """
    Пересоздаёт таблицу vacancies
    """
    conn = psycopg2.connect(host='localhost', database='HHVac', user='postgres',
                            password='121212')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('DROP TABLE IF EXISTS vacancies')
                cur.execute("""
                            CREATE TABLE vacancies
                            (
                                vac_id serial,
                                company_name varchar(50) NOT NULL,
                                vac_name varchar(255) NOT NULL,
                                pay varchar(255),
                                pay_currency varchar(10),
                                city varchar(50) NOT NULL,
                                vac_link varchar(255) NOT NULL,
                                hh_vac_id varchar(9) NOT NULL,
                                description varchar(255) NOT NULL,
                                
                                CONSTRAINT pk_vacancies_vac_id PRIMARY KEY(vac_id)
                            );
                            """)
                # cur.execute('INSERT INTO user_account VALUES (%s, %s)', (6, 'Bruh'))
                # cur.execute('SELECT * FROM user_account')
    finally:
        conn.close()
