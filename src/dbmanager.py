import psycopg2
from tabulate import tabulate


class DBManager:
    headers = ['Companym_name', 'Vacancy_name', 'pay', 'currency', 'vac_link']

    def __init__(self, db_name, params):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получаем список компаний и количество размещенных ими вакансий
        """

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT DISTINCT company_name
                        FROM vacancies
                        """)

                    companies_list = cur.fetchall()

                    # print(companies_list)

                    companies_count = {}
                    for company in companies_list:
                        company_name = company[0]
                        cur.execute(
                            f"""
                            SELECT COUNT(*) FROM vacancies
                            WHERE company_name in ('{company_name}')
                            """)
                        company_count = cur.fetchone()
                        companies_count[company_name] = company_count[0]
                        # print(companies_count)

        finally:
            conn.close()

        # for cn, cc in companies_count.items():
        #     print(f'Компания: {cn}\nКоличество вакансий:{cc}\n')

        return companies_count

    def get_all_vacancies(self):
        """
        названия компании, названия вакансии и зарплаты и ссылки на ваканси
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT company_name, vac_name, pay, pay_currency, vac_link
                        FROM vacancies
                        ORDER BY pay DESC
                        """)
                    all_vac_list_tuples = cur.fetchall()

        finally:
            conn.close()
        result = tabulate(all_vac_list_tuples,
                          headers=DBManager.headers,
                          tablefmt='psql')
        return result

    def get_avg_salary(self):
        """
        Возвращает среднюю зарплату среди вакансий с ненулевой зп в рублях
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT AVG(pay)
                        FROM vacancies
                        WHERE pay <> 0 AND pay_currency = 'RUR'
                        """)
                    avg_pay = cur.fetchone()

        finally:
            conn.close()

        return round(avg_pay[0])

    def get_vacancies_with_higher_salary(self, num_of_vacs):
        """
        Возвращает вакансии с зарплатой больше средней по всем вакансиям
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        try:
            with conn:
                with conn.cursor() as cur:
                    avg_pay = self.get_avg_salary()

                    cur.execute(
                        f"""
                        SELECT company_name, vac_name, pay, pay_currency, vac_link
                        FROM vacancies WHERE pay > {avg_pay}
                        """)
                    higher_pay_vac_list_tuples = cur.fetchall()
                    sorted_list = sorted(higher_pay_vac_list_tuples,
                                         key=lambda x: x[2], reverse=True)
        finally:
            conn.close()

        result = tabulate(sorted_list[:num_of_vacs],
                          headers=DBManager.headers,
                          tablefmt='psql')
        return result

    def get_vacancies_with_keyword(self, keyword, is_fuzzy=False):
        """
        Возвращает список вакансий, в названии которых есть ключевое слово
        Опионально можно подключить поиск и по требованиям+обязанностям (параметр is_fuzzy)
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        try:
            with conn:
                with conn.cursor() as cur:
                    if is_fuzzy:
                        cur.execute(
                            f"""
                        SELECT *
                        FROM vacancies
                        WHERE LOWER(vac_name) LIKE '%{keyword.lower()}%' 
                        OR LOWER(requirement) LIKE '%{keyword.lower()}%' 
                        OR LOWER(responsibility) LIKE '%{keyword.lower()}%'
                        """)
                    else:
                        cur.execute(
                            f"""
                        SELECT *
                        FROM vacancies
                        WHERE LOWER(vac_name) LIKE '%{keyword.lower()}%'
                        """)

                    vac_list = cur.fetchall()
                    # print(vac_list)
        finally:
            conn.close()

        result = tabulate(vac_list,
                          headers=DBManager.headers,
                          tablefmt='psql')

        return result

    def get_some_stats(self, avg_pay):
        conn = psycopg2.connect(dbname=self.db_name, **self.params)

        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"""
                        SELECT COUNT(*)
                        FROM vacancies
                        WHERE pay <> 0
                        """)
                    total_vac_w_pay = cur.fetchone()

                    cur.execute(
                        f"""
                        SELECT COUNT(*)
                        FROM vacancies
                        WHERE pay > {avg_pay}
                        """)
                    total_vac_with_higher_pay = cur.fetchone()
        finally:
            conn.close()

        return total_vac_w_pay[0], total_vac_with_higher_pay[0]
