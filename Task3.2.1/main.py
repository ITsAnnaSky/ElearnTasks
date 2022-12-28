import os
import csv
from re import sub, compile
import json
from datetime import datetime
from csv import reader as read_csv

import numpy as np
import base64

#
currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}




class Stat:
    salary_by_year = {}
    vacancy_by_year = {}
    salary_prof = {}
    prof_by_year = {}
    salary_by_city = {}
    precent_by_city = {}

    def __init__(self, sby, vby, sp, pby, sbc, pbc):
        self.salary_by_year = sby
        self.vacancy_by_year = vby
        self.salary_prof = sp
        self.prof_by_year = pby
        self.salary_by_city = sbc
        self.precent_by_city = pbc


class Vacancy:
    name = ''
    salary_from = 0.0
    salary_to = 0.0
    salary_currency = ''
    area_name = ''
    published_at = '1'

    def __init__(self, vac):
        self.name = vac['name']
        # print(salary_from)
        self.salary_from = float(vac['salary_from'])
        self.salary_to = float(vac['salary_to'])
        self.salary_currency = vac['salary_currency']
        self.area_name = vac['area_name']
        self.published_at = vac['published_at']


def read_file(file_name, prof):
    rows = list()
    vacancies = list()
    prof = prof.lower()
    file = open(file_name, 'r', encoding='utf-8-sig')
    file_reader = csv.reader(file, delimiter=",")
    count = 0
    columns = ''
    files = {}
    for row in file_reader:
        if columns == '':
            columns = row
            continue
        time = row[5]
        year = time.split('-')[0]
        if files.__contains__(year):
            line = ','.join(str(i) for i in row) + '\n'
            files[year].write(line)
        else:
            files[year] = open(year, 'w', encoding='utf-8')
            line = ','.join(str(i) for i in columns) + '\n'
            line2 = ','.join(str(i) for i in row) + '\n'
            files[year].write(line)
            files[year].write(line2)
    for i in files:
        files[i].close()
    return vacancies


file_name = '1.csv'
prof = 'программист'
vacancies = read_file(file_name, prof.replace('\n', ''))

