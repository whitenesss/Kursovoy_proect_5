from src.class_abstract_bdmanager import AbstractBDmanager
import psycopg2


class DBManager(AbstractBDmanager):

    def __init__(self, database_name, param):
        self.param = param
        self.database_name = database_name

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""

        conn = psycopg2.connect(dbname=self.database_name, **self.param)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT company.employer, COUNT(vacanciy.vacanciy_id) as vacancies_count
            FROM company 
            JOIN vacanciy  ON company.company_id = vacanciy.company_id
            GROUP BY company.employer
            ORDER BY vacancies_count DESC
            """)

        # Получение результатов
        companies_vacancies_count = cur.fetchall()
        cur.close()
        conn.close()

        return companies_vacancies_count

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию."""

        conn = psycopg2.connect(dbname=self.database_name, **self.param)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT employer, name_vacanciy, salary_from, salary_to,url 
            FROM vacanciy
            JOIN company  ON company.company_id = vacanciy.company_id
            ORDER BY salary_from DESC
            """)
        all_vacancies = cur.fetchall()
        cur.close()
        conn.close()
        return all_vacancies

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.param)
        cur = conn.cursor()

        cur.execute(
            """
            select AVG(salary_from) from vacanciy
            """)
        avg_salary = cur.fetchall()
        cur.close()
        conn.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.param)
        cur = conn.cursor()

        cur.execute("SELECT name_vacanciy, salary_from, salary_to,"
                    "url FROM vacanciy WHERE salary_from > %s", (self.get_avg_salary()), )
        vacancies = cur.fetchall()

        cur.close()
        conn.close()

        return vacancies

    def get_vacancies_with_keyword(self, name_vacansy):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        conn = psycopg2.connect(dbname=self.database_name, **self.param)
        cur = conn.cursor()

        cur.execute("select name_vacanciy, salary_from, "
                    "salary_to,url  from vacanciy where name_vacanciy LIKE %s", ('%' + name_vacansy + '%',))
        vacancies = cur.fetchall()
        cur.close()
        conn.close()
        return vacancies
