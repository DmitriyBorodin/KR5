import json
from src.utils import *




# with open("data/companies.json", "r", encoding="utf-8") as file:
#     companies = json.load(file)
#
# for company_name, company_id in companies.items():
#     print(f"Парсим вакансии по компании: {company_name}")
#
#     print(f"data/{company_name}_vacancies.json")





get_vacancies()





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