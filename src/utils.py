import requests
import json
import time
import psycopg2
import os


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
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS vacancies
                            (
                                vac_id serial,
                                company_name varchar(50) NOT NULL,
                                vac_name varchar(255) NOT NULL,
                                pay int,
                                pay_currency varchar(10),
                                city varchar(50) NOT NULL,
                                vac_link varchar(255) NOT NULL,
                                hh_vac_id varchar(9) NOT NULL,
                                requirement varchar(255) NOT NULL,
                                responsibility varchar(255) NOT NULL,
                                schedule varchar(255),
                                
                                CONSTRAINT pk_vacancies_vac_id PRIMARY KEY(vac_id)
                            );
                            """)
                conn.commit()
    finally:
        conn.close()


def fill_vacancies_table():
    """
    Наполняет таблицу вакансиями
    """

    conn = psycopg2.connect(host='localhost', database='HHVac', user='postgres',
                            password='121212')
    try:
        with (conn):
            with conn.cursor() as cur:

                directory = os.fsencode("data")

                for vac_comp_file in os.listdir(directory):

                    filename = os.fsdecode(vac_comp_file)

                    if filename != "companies.json":
                        company_name = filename[:-15]
                        with open(f"data/{filename}", encoding='utf-8') as file:
                            data = file.read()
                            vac_list = json.loads(data)
                            # print(data)
                            # print(filename)
                            # time.sleep(3)
                            for vacancy in vac_list:
                                vac_params = [company_name]
                                vac_params.extend(get_vac_params(vacancy))
                                # vac_params = [str(param) for param in vac_params]
                                print(vac_params)
                                # for p in vac_params:
                                #     print(p)
                                company_name, vac_name, pay, pay_currency, city, vac_link, hh_vac_id, requirement, responsibility, schedule = [*vac_params]
                                cur.execute('INSERT INTO vacancies (company_name, vac_name, pay, pay_currency, city, vac_link, hh_vac_id, requirement, responsibility, schedule)'
                                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [*vac_params])
                                conn.commit()
    finally:
        conn.close()


def get_vac_params(vacancy):
    """
    Принимает вакансию и возвращает набор её параметров
    """

    vac_name = vacancy['name']

    pay = 0
    if not vacancy.get('salary'):
        pay = 0
    elif vacancy['salary']['to']:
        pay = int(vacancy['salary']['to'])

    pay_currency = 'Не указана'
    if vacancy.get('salary'):
        pay_currency = vacancy['salary']['currency']

    city = vacancy['area']['name']

    vac_link = vacancy['alternate_url']

    hh_vac_id = vacancy['id']

    try:
        if vacancy['snippet']['requirement'] is None:
            requirement = 'Нет списка требований'
        else:
            requirement = vacancy['snippet']['requirement']
    except KeyError:
        requirement = 'Нет списка требований'

    try:
        if vacancy['snippet']['responsibility'] is None:
            responsibility = 'Нет описания'
        else:
            responsibility = vacancy['snippet']['responsibility']
    except KeyError:
        responsibility = 'Нет описания'

    schedule = vacancy['schedule']['name']

    return vac_name, pay, pay_currency, city, vac_link, hh_vac_id, requirement, responsibility, schedule



