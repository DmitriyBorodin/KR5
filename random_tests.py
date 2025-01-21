import json
import os
from tqdm import tqdm
from src.dbmanager import DBManager
from src.utils import *
from config import config

params = config()

# with open("data/companies.json", "r", encoding="utf-8") as file:
#     companies = json.load(file)
#
# for company_name, company_id in companies.items():
#     print(f"Парсим вакансии по компании: {company_name}")
#
#     print(f"data/{company_name}_vacancies.json")

db_name = 'testfirst'
create_vacancies_table(db_name, params)

# get_vacancies()
# create_vacancies_table()
# fill_vacancies_table()

# DBmng = DBManager('localhost', 'HHVac', 'postgres','121212')
# #
# total, total_high = DBmng.get_some_stats()
#
# print(total, total_high)

# zzz = DBmng.get_vacancies_with_keyword('Python', True)
# print(zzz)
#
# for vac in zzz:
#     print(vac)

# for cn, cc in comp_count.items():
#     print(f'Компания: {cn}\nКоличество вакансий:{cc}\n')


# for i in tqdm(range(10), desc='Парсим вакансии', unit='вакансии', ncols=60, bar_format= "{l_bar}{bar}{n_fmt}/{total_fmt}", colour="green"):
#     time.sleep(3)


# def get_loading_bar():
#
#     with open("data/companies.json", "r", encoding="utf-8") as file:
#         companies = json.load(file)
#
#     for company_name, company_id in companies.items():
#         print(f"Парсим вакансии по компании: {company_name}")
#
#         with open(f"data/{company_name}_vacancies.json", "w", encoding="utf-8") as file:
#
#             company_vacancies = []
#             for page in range(20):
#
#                 with requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}&area=113&per_page=100&page={page}", stream=True) as r:
#
#                     print(f"https://api.hh.ru/vacancies?employer_id={company_id}&area=113&per_page=100&page={page}")
#
#
#
#                     try:
#                         company_vacancies.extend(data['items'])
#                     except KeyError as error:
#                         print(error)
#                         continue
#
#                     print(f"Страница = {page}")
#
#                 json.dump(company_vacancies, file, sort_keys=False, indent=4,
#                           ensure_ascii=False)
#
#                 # Таймаут чтобы не превырашать лимит запросов (просит каптчу, если превысить)
#                 time.sleep(4)

# get_vacancies()

# directory = os.fsencode("data")
#
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     if filename != "companies.json":
#         print(filename[:-15])
#         continue




# print(f"Парсим вакансии по компании: Газпромбанк")
#
# with open(f"data/Газпромбанк_vacancies.json", "w",
#           encoding="utf-8") as file:
#
#     company_vacancies = []
#     for page in range(21):
#         data = (requests.get(
#             f"https://api.hh.ru/vacancies?employer_id=3388&area=113&per_page=100&page={page}")).json()
#
#         print(
#             f"https://api.hh.ru/vacancies?employer_id=3388&area=113&per_page=100&page={page}")
#
#         try:
#             company_vacancies.extend(data['items'])
#         except KeyError as error:
#             print(error)
#             continue
#
#         print(f"Страница = {page}")
#
#     json.dump(company_vacancies, file, sort_keys=False, indent=4,
#               ensure_ascii=False)