import psycopg2
import requests
import random

conn = psycopg2.connect(
    host="localhost",
    database="country",
    user="postgres",
    password="12345678"
)
cursor = conn.cursor()

url = "https://restcountries.com/v3.1/all?fields=name,capital,flags,subregion,population"
response = requests.get(url, timeout=1)

if response.status_code == 200:
    countries = response.json()
    if isinstance(countries, list) and len(countries) >= 10:
        random_countries = random.sample(countries, 10)

        for country in random_countries:
            name = country.get("name", {}).get("common", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            flag = country.get("flags", {}).get("png", "")
            subregion = country.get("subregion", "N/A")
            population = country.get("population", 0)

            cursor.execute(
                "INSERT INTO countries (name, capital, flag, subregion, population) VALUES (%s, %s, %s, %s, %s)",
                (name, capital, flag, subregion, population)
            )

        conn.commit()
        print("Countries inserted successfully.")
    else:
        print("Error: Invalid data or less than 10 countries.")
else:
    print("Failed to fetch countries:", response.status_code)

cursor.close()
conn.close()