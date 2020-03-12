from bs4 import BeautifulSoup as bs
import lxml
import pandas as pd
import requests
from pprint import pprint
d_vac = dict()
list_vacancy_name = list()
list_salary_min = list()
list_salary_max = list()
list_vacancy_url = list()
vacancy = input('Ключевое слово по поиску вакансии: ')
page_num = int(input('Введите количество страниц с вакансиями: '))
#main_link = 'https://www.superjob.ru/vacancy/search/?keywords=cisco&geo%5Bt%5D%5B0%5D=4'
def vacancy_pars(vacancy, page_num):
    main_link = "https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={}&page={}".format(vacancy, page_num)
    user_agent = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
    html = requests.get(main_link, headers = user_agent).text
    parsed_html = bs(html, 'lxml')

    vacancy_block = parsed_html.find('div', {'class': "vacancy-serp"})
    vacancy_list = vacancy_block.findChildren(recursive = False)
    return(vacancy_list)
#vacancy_descr = vacancy_block.find_all('a', {'class': 'bloko-link HH-LinkModifier'})

for k in range(page_num):
    for i in vacancy_pars(vacancy, k):
        salary = i.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        vacancy_name = i.find('a', {'class': "bloko-link HH-LinkModifier"})
        vacancy_url = i.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
        try:
            vacancy_name = vacancy_name.getText()
            salary = salary.getText()
            vacancy_url_href = vacancy_url.get('href')
            list_vacancy_name.append(vacancy_name)
            if "от" in salary:
                list_salary_min.append(salary)
                list_salary_max.append('Не указана')
            elif "до" in salary:
                list_salary_max.append(salary)
                list_salary_min.append('Не указана')
            else:
                list_salary_max.append(salary.split('-')[1])
                list_salary_min.append(salary.split('-')[0])
            list_vacancy_url.append(vacancy_url_href)
        except:
            pass
d_vac['name'] = list_vacancy_name
d_vac['vacancy_url'] = list_vacancy_url
d_vac['salary_min'] = list_salary_min
d_vac['salary_max'] = list_salary_max

df = pd.DataFrame.from_dict(d_vac)
print(df)
df.to_excel('test.xlsx')


