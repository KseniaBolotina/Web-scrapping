import requests
from bs4 import BeautifulSoup
import json
from fake_headers import Headers

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser="firefox", os="win").generate()
main_response = requests.get(url, headers=headers)

main_html = main_response.text
main_soup = BeautifulSoup(main_html, 'lxml')

def clean_text(text):
    return text.translate({ord('\xa0'): ' ', ord('\u202f'): ' '})
vacancies = []
vacancies_find = main_soup.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y')
for vac in vacancies_find:
    title = clean_text((vac.find('a', class_='bloko-link')).text.strip())
    link = vac.find('a', class_='bloko-link').get('href')
    company = clean_text((vac.find('a', class_='bloko-link bloko-link_kind-secondary')).text.strip())
    city = clean_text((vac.find('span', {'data-qa': 'vacancy-serp__vacancy-address_narrow'})).text.strip())
    salary_tag = vac.find('span',
                           class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh')
    salary = clean_text(salary_tag.text.strip()) if salary_tag else 'Не указана'

    vacancy_response = requests.get(link, headers=headers)
    vacancy_soup = BeautifulSoup(vacancy_response.text, 'lxml')

    description = (vacancy_soup.find('div', {'data-qa': 'vacancy-description'})).text
    if 'Django' in description or 'Flask' in description:
        vacancies.append({
            'Вакансия': title,
            'Ссылка на вакансию': link,
            'Название компании': company,
            'Город': city,
            'Зарлата': salary
        })


with open('vacancies.json', 'w', encoding='utf-8', newline='') as file:
    json.dump(vacancies, file, ensure_ascii=False, indent=4)
