import requests


def get_employer_id(company_name):
    """получаем id компании на hh.ru"""
    url = 'https://api.hh.ru/employers'
    params = {'text': company_name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        emploers_data = response.json()
        if 'items' in emploers_data and len(emploers_data['items']) > 0:
            for emploer in emploers_data['items']:
                if emploer['name'] == company_name:
                    return emploer['id']
        else:
            print("Компания не найдена.")
            return None
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None


def get_all_vacancies_by_employer_id(employer_id):
    """получаем вакансии конкретной компании по id не больше 1500 вакансий"""
    all_vacancies = []
    url = 'https://api.hh.ru/vacancies'
    page = 0
    per_page = 100  # Максимальное количество вакансий на одной странице
    while page < 4:
        params = {'employer_id': employer_id, 'per_page': per_page, 'page': page}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            vacancies_data = response.json()
            if vacancies_data['items']:
                all_vacancies.extend(vacancies_data['items'])
                page += 1
                # for vacancies in vacancies_data['items']:
                #     print(vacancies['name'])
            else:
                break  # Если больше нет вакансий, прерываем цикл
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
            return None
    return all_vacancies


