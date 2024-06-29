from src.utils import *
from src.dbmanager import DBManager


def main():
    while True:
        user_input = input('Здравствуйте, вы уже сегодня парсили вакансии в бд?\n'
                           'Что угодно - Да!\n'
                           '2 - Нет(\n')
        if user_input == '2':
            # Парсим вакансии с HH.ru и записываем их в json файлы
            print('Тогда сейчас мы будем парсить вакансии с hh.ru по 10ти топовым IT компаниям:')

            get_vacancies()

            # Создаём таблицу (если ещё не сущесвует)
            create_vacancies_table()

            # Наполняем таблицу вакансиями из json файлов
            fill_vacancies_table()
            break
        else:
            print('Понятно, тогда больше не будем парсить\n')
            break

    dbmng = DBManager('localhost', 'HHVac', 'postgres', '121212')

    # Получаем выводим список компаний и кол-во их вакансий
    companies_count = dbmng.get_companies_and_vacancies_count()

    print('Список компаний и количество их вакансий:')
    for cn, cc in companies_count.items():
        print(f'{cn} - {cc}')

    # Получаем среднюю зарплату по всем вакансиям с указанной зп и немного статистики
    avg_pay = dbmng.get_avg_salary()
    total_vac_w_pay, total_vac_w_higher_pay = dbmng.get_some_stats()
    print(f'\nСредняя зарплата по вакансиям(включая только вакансии с указанным уровнем дохода) - {avg_pay} рублей\n'
          f'Всего таких вакансий - {total_vac_w_pay}\n'
          f'Из них зарплату выше среднего имеют {total_vac_w_higher_pay} вакансий\n'
          f'Т.е. зп выше средней могут предложить {round(((total_vac_w_higher_pay/total_vac_w_pay)*100))}% вакансий\n')

    # Выводим список вакансий с зп выше средней (опционально)
    while True:
        user_input = input('Вывести N количество вакансий с ЗП выше средней?\n'
                           'Введите 1 или 2\n'
                           '1 - Да, выводим\n'
                           '2 - Нет, спасибо\n')
        try:
            if int(user_input) not in (1, 2):
                if user_input in ('stop', 'стоп'):
                    print('Завершаю работу')
                    exit()
                else:
                    print('В качестве ответа принимается только 1 или 2')
            elif int(user_input) == 1:
                user_input = input('Введите количество вакансий для отображения\n'
                                   'Если оставить пустым - покажу все вакансии\n')
                try:
                    num_of_vacs = str(user_input)
                    higher_salary_vacancies = dbmng.get_vacancies_with_higher_salary(num_of_vacs)
                    for vac in higher_salary_vacancies:
                        print(vac)
                    print('')
                    break
                except ValueError as e:
                    print(e)
                break
            elif int(user_input) == 2:
                print('')
                break
        except ValueError as e:
            print(e)

    # Вывод вакансий по keyword
    while True:
        user_input = input('Введите ключевое слово для поиска в названии вакансии среди всех вакансий:\n')
        try:
            if user_input in ('stop', 'стоп'):
                print('Завершаю работу')
                exit()
            elif not user_input.isalpha():
                print('В качестве ответа принимается только слова')
            else:
                keyword_vacs = dbmng.get_vacancies_with_keyword(user_input)
                if not keyword_vacs:
                    print('По этому запросу нет вакансий')
                for vac in keyword_vacs:
                    print(vac)
                print(f'Это конец списка вакансий по запросу "{user_input}"')
                break
        except ValueError as e:
            print(e)

    # Выводим все вакансии подряд в терминал (опционально)
    while True:
        user_input = input(
            'А хотите вывести на экран вообще все вакансии подряд? Введите 1 или 2\n'
            '1 - Да, давай всё на экран\n'
            '2 - Не надо, пожалуйста\n')
        try:
            if int(user_input) not in (1, 2):
                if user_input in ('stop', 'стоп'):
                    print('Завершаю работу')
                    exit()
                else:
                    print('В качестве ответа принимается только 1 или 2, давай попробуем ещё раз')
            elif int(user_input) == 1:
                print('Лавина неотсортированных вакансий через 3..')
                time.sleep(1)
                print('2..')
                time.sleep(1)
                print('1!')
                time.sleep(0.7)
                all_vac = dbmng.get_all_vacancies()
                for vac in all_vac:
                    print(vac)
                break
            elif int(user_input) == 2:
                print('Тогда завершаю работу без засорения терминала кучей вакансий')
                break
        except ValueError as e:
            print(e)


if __name__ == '__main__':
    main()
