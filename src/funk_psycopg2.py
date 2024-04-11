import psycopg2


def create_database(database_name: str, params: dict):
    """создаем две таблице с рабоодателем и вакансиямии связываем из по id"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                company_id SERIAL PRIMARY KEY,
                employer VARCHAR(50) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacanciy(
                vacanciy_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES company(company_id),
                name_vacanciy VARCHAR NOT NULL,
                publish_date DATE,
                url TEXT,
                salary_from INTEGER,
                salary_to INTEGER
            )
        """)
    conn.commit()
    conn.close()


def seve_database(company_name: str, data, database_name: str, params: dict):
    """Сохранение данных в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO company (employer)
            VALUES (%s)
            RETURNING  company_id
            """,
            (company_name,)
        )
        company_id = cur.fetchone()[0]
        for vacancy_data in data:
            if vacancy_data['salary'] == None:
                cur.execute(
                    """
                    INSERT INTO vacanciy (company_id, name_vacanciy, publish_date, url, salary_from, salary_to)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """,
                    (company_id, vacancy_data['name'], vacancy_data['published_at'],
                     vacancy_data['alternate_url'], 0, 0),
                )
                continue
            elif vacancy_data['salary'] != None:
                if vacancy_data['salary']['from'] != None:
                    if vacancy_data['salary']['to'] != None:
                        cur.execute(
                            """
                            INSERT INTO vacanciy (company_id, name_vacanciy, publish_date, url, salary_from, salary_to)
                            VALUES (%s,%s,%s,%s,%s,%s)
                        """,
                            (company_id, vacancy_data['name'], vacancy_data['published_at'],
                             vacancy_data['alternate_url'],
                             vacancy_data['salary']['from'], vacancy_data['salary']['to'])
                        )
                        continue
                    elif vacancy_data['salary']['to'] == None:
                        cur.execute(
                            """
                            INSERT INTO vacanciy (company_id, name_vacanciy, publish_date, url, salary_from, salary_to)
                            VALUES (%s,%s,%s,%s,%s,%s)
                        """,
                            (company_id, vacancy_data['name'], vacancy_data['published_at'],
                             vacancy_data['alternate_url'],
                             vacancy_data['salary']['from'], 0)
                        )
                        continue
                elif vacancy_data['salary']['to'] != None:
                    cur.execute(
                        """
                        INSERT INTO vacanciy (company_id, name_vacanciy, publish_date, url, salary_from, salary_to)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """,
                        (company_id, vacancy_data['name'], vacancy_data['published_at'],
                         vacancy_data['alternate_url'],
                         0, vacancy_data['salary']['to'])
                    )
                    continue

    conn.commit()
    conn.close()
