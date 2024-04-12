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
    while page < 1:
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


def printing(dbm):
    priiv = {1: dbm.get_companies_and_vacancies_count,
             2: dbm.get_all_vacancies,
             3: dbm.get_avg_salary,
             4: dbm.get_vacancies_with_higher_salary,
             5: dbm.get_vacancies_with_keyword
             }
    print()
    print('Доступные режимы выводов и фильтрации  информации из базы даннх')
    print()
    for a, b in priiv.items():
        ab = b.__doc__
        print(a, ab)

    while True:
        user_input = input('Выберите номер фильтрации, который вас интересует: ')
        if user_input in ['1', '2', '3', '4', '5']:
            if user_input in '5':
                user_input_name = input('Введите пораметр поиска: ')
                method = priiv[int(user_input)]
                result = method(user_input_name)
                for c in result:
                    print(*c)
                user_input_select = input('Для остоновки нажмите n : ')
                if user_input_select in 'n':
                    break
                continue
            method = priiv[int(user_input)]
            result = method()
            for c in result:
                print(*c)
            user_input_select = input('Для остоновки нажмите n : ')
            if user_input_select in 'n':
                break
            continue
        else:
            print('Пожалуйста, введите число от 1 до 5.')

