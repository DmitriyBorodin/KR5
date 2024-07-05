from src.utils import *
from src.dbmanager import DBManager
from config import config


def main():

    params = config()

    while True:
        user_input = input('Здравствуйте, вы уже сегодня парсили вакансии в бд?\n'
                           'Что угодно - Да!\n'
                           '2 - Нет(\n')
        if user_input == '2':
            # Парсим вакансии с HH.ru и записываем их в json файлы

            db_name = input('Введите название базы данных для создания\n')
            create_database(db_name, params)


            print('Cейчас мы будем парсить вакансии с hh.ru по 10ти топовым IT компаниям:')

            get_vacancies()

            # Создаём таблицу (если ещё не сущесвует)
            create_vacancies_table(db_name, params)

            # Наполняем таблицу вакансиями из json файлов
            fill_vacancies_table(db_name, params)
            break
        else:
            print('Понятно, тогда больше не будем парсить\n')
            db_name = input('Введите название бд, куда уже парсили вакансии\n')
            break

    dbmng = DBManager(db_name, params)

    # Получаем выводим список компаний и кол-во их вакансий
    companies_count = dbmng.get_companies_and_vacancies_count()

    print('Список компаний и количество их вакансий:')
    for cn, cc in companies_count.items():
        print(f'{cn} - {cc}')

    # Получаем среднюю зарплату по всем вакансиям с указанной зп и немного статистики
    avg_pay = dbmng.get_avg_salary()
    total_vac_w_pay, total_vac_w_higher_pay = dbmng.get_some_stats(avg_pay)
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
            if user_input in ('stop', 'стоп'):
                print('Завершаю работу')
                exit()
            elif int(user_input) == 1:
                user_input = input('Введите количество вакансий для отображения\n')
                try:
                    num_of_vacs = int(user_input)
                    higher_salary_vacancies = dbmng.get_vacancies_with_higher_salary(num_of_vacs)
                    print(higher_salary_vacancies)
                    # for vac in range(num_of_vacs):
                    #     print(higher_salary_vacancies[vac])
                    print('')
                    break
                except ValueError:
                    print('Не похоже на цифру..')
            elif int(user_input) == 2:
                print('')
                break
        except ValueError:
            print('Это было не "1 или 2"...\nДавай попробуем ещё раз')

    # Вывод вакансий по keyword
    while True:
        user_input = input('Введите ключевое слово для поиска в названии вакансии среди всех вакансий:\n')
        try:
            if user_input in ('stop', 'стоп'):
                print('Завершаю работу')
                exit()
            if not user_input.strip():
                print('Пожалуйста, введите ключевое слово')
                continue
            if not user_input.isalpha():
                print('В качестве ключевого слова принимаются только слова')
            else:
                keyword_vacs = dbmng.get_vacancies_with_keyword(user_input)
                if not keyword_vacs:
                    print('По этому запросу нет вакансий')
                else:
                    print(keyword_vacs)
                    print(f'Это конец списка вакансий по запросу "{user_input}"')
                break
        except ValueError as e:
            print(e)

    # Выводим все вакансии подряд в терминал (опционально)
    while True:
        user_input = input(
            '\nА хотите вывести на экран вообще все вакансии подряд? Введите 1 или 2\n'
            '1 - Да, давай всё на экран\n'
            '2 - Не надо, пожалуйста\n')
        try:
            if user_input in ('stop', 'стоп'):
                print('Завершаю работу')
                exit()
            elif not isinstance(int(user_input), int):
                print('В качестве ответа принимается только 1 или 2, давай попробуем ещё раз')
            elif int(user_input) == 1:
                print('Лавина неотсортированных вакансий через 3..')
                time.sleep(1)
                print('2..')
                time.sleep(1)
                print('1!')
                time.sleep(0.7)
                all_vac = dbmng.get_all_vacancies()
                print(all_vac)
                break
            elif int(user_input) == 2:
                print('Тогда завершаю работу без засорения терминала кучей вакансий')
                break
        except ValueError as e:
            print(e)


if __name__ == '__main__':
    main()
