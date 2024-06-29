import psycopg2


class DBManager:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.__password = password
        self.conn = 'host=self.host, database=self.database,user=self.user, password=self.__password'

    # def __enter__(self):
    #     conn = psycopg2.connect(host='localhost', database='HHVac',
    #                             user='postgres',
    #                             password='121212')
    #     curr = conn.cursor()
    #
    # def __exit__(self):
    #     conn.commit()
    #
    #     cur.close()
    #     conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получаем список компаний и количество размещенных ими вакансий
        """

        conn = psycopg2.connect(host=self.host, database=self.database,
                                user=self.user, password=self.__password)
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
        conn = psycopg2.connect(host=self.host, database=self.database,
                                user=self.user, password=self.__password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT company_name, vac_name, pay, pay_currency, vac_link
                        FROM vacancies
                        """)
                    all_vac_list_tuples = cur.fetchall()

                    # for vac in all_vac_list_tuples:
                    #     print(vac)

        finally:
            conn.close()

        return all_vac_list_tuples


    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
