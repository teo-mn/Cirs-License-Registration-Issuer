import json

import requests
import random

licenses = ['Барилга угсралт', 'Зураг төсөл', '16 ДАВХАР ХҮРТЭЛ БАРИЛГА']
requirements = ['БА-3.1', 'БА-3.3', 'БА-3.4', 'БА-6.1', 'БА-6.2', 'БА-6.3', 'БА-6.4', 'БА-7.1']
owners = [['123', 'Блокчэйн Сольюшн'], ['1234', 'Эй Ай Лаб'], ['12345', 'Корэкс']]
employees = [
    {
        "regnum": "АА11223344",
        "last_name": "Батболд",
        "first_name": "Доржсүрэн",
        "profession": "Барилгын инженэр",
        "degree": "Бакалавр"
    },
    {"regnum": "УУ99887766",
     "last_name": "Дондог",
     "first_name": "Алимаа",
     "profession": "Мэдээллийн техологийн инженэр",
     "degree": "магистр"},
    {"regnum": "ФФ55667788",
     "last_name": "Цэцэг",
     "first_name": "Төмөр",
     "profession": "Хүний их эмч",
     "degree": "Доктор"}
]


def fill_data():
    # requests.post('http://localhost:8000/api/register', data)
    cnt_license = 30
    cnt_req = 10
    cnt_employee = 3

    for i in range(cnt_license):
        start_date = random.randint(1698656171, 1702198571)
        owner = owners[random.randint(0, len(owners) - 1)]
        print(owner)
        data = {
            "request_id": "9",
            "callback_url": "http://localhost:8000/test",
            "payload": {
                "license_system_id": str(i),
                "license_type": licenses[random.randint(0, len(licenses) - 1)],
                "license_id": str(i),
                "start_date": start_date,
                "end_date": random.randint(start_date, 1733820971),
                "owner_id": str(owner[0]),
                "owner_name": str(owner[1]),
                "requirements": []
            }
        }
        for j in range(cnt_req):
            req = {
                "requirement_system_id": str(i * 100 + j),
                "requirement_id": str(i * 100 + j),
                "state": 0,
                "employees": []
            }
            for k in range(cnt_employee):
                e = employees[random.randint(0, len(employees) - 1)]
                req["employees"].append(e)
            data["payload"]["requirements"].append(req)
        headers = {"Content-Type": "application/json"}
        res = requests.post('http://localhost:8000/api/register', headers=headers, data=json.dumps(data))
        print(res)


if __name__ == '__main__':
    fill_data()
