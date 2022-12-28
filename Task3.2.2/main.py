import os
import csv
from re import sub, compile
import json
from datetime import datetime
from csv import reader as read_csv
from multiprocessing import Process, Pipe

import numpy as np
import base64

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
    columns = []
    salary = 0.0
    count = 0
    salary_prof = 0
    prof_count = 0
    city = dict()
    for row in file_reader:
        if count == 0:
            columns = row
            count = count + 1
            continue
        if "" in row or len(row) != len(columns):
            continue
        current = {}
        for i in range(len(row)):
            current[columns[i]] = row[i]
        vac =Vacancy(current)
        salary += (vac.salary_to + vac.salary_from)*currency_to_rub[vac.salary_currency]/2.0
        count += 1
        if vac.name.__contains__(prof):
            salary_prof += (vac.salary_to + vac.salary_from)*currency_to_rub[vac.salary_currency]/2.0
            prof_count += 1
        if city.__contains__(vac.area_name):
            city[vac.area_name] =

    return [salary/count, count, salary_prof/prof_count, prof_count]


#file_name = '1.csv'
#prof = 'программист'
#vacancies = read_file(file_name, prof.replace('\n', ''))

def multiprocessing_file_read(connection, filename, prof):
    middle_salary= read_file(filename, prof)
    connection.send([filename, middle_salary])
    connection.close()
if __name__ == '__main__':
    path_data = 'data'
    list_connection = list()
    for i in os.listdir(path_data):
        parent_conn, child_conn = Pipe()
        list_connection.append(parent_conn)
        path = path_data + '\\' + i
        p = Process(target=multiprocessing_file_read, args=(child_conn, path, 'Аналитик'))
        p.start()
    for conn in list_connection:
        print(conn.recv())
