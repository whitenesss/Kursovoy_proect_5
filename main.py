from src.class_DBManager import DBManager
from data.config import config
from src.utils import get_employer_id, get_all_vacancies_by_employer_id
from src.funk_psycopg2 import create_database, seve_database

config = config()
companys = ["Тинькофф", "Яндекс", "VK", "Лаборатория Касперского",
            "МТС", "СБЕР", "Райффайзен Банк", "Спортмастер", "Аэрофлот", "Альфа-Банк"]
# companys = ["Тинькофф", "Яндекс"]
name_data_1 = 'hh_vacahncy'
create_database(name_data_1, config)
for company_name in companys:
    employers_id = get_employer_id(company_name)

    if employers_id:
        print(f"Идентификатор компании '{company_name}': {employers_id}")
        all_vacancie = get_all_vacancies_by_employer_id(employers_id)
        if all_vacancie:
            print(f"Общее количество вакансий компании '{company_name}': {len(all_vacancie)}")

            seve_database(company_name, all_vacancie, name_data_1, config)
            print("Вакансии успешно записаны в файл 'hh.json'")
        else:
            print(f"Не удалось получить вакансии компании '{company_name}'.")
    else:
        print(f"Не удалось найти компанию '{company_name}'.")

dbm = DBManager(name_data_1, config)

print(dbm.get_vacancies_with_higher_salary())
