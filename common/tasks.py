from decimal import Decimal

import requests
from openpyxl import load_workbook

from .celery import app
from .utils import fetch_latest_link
import shutil


@app.task(bind=True)
def update_prices(self):
    # logger.debug(self.request.id)
    url = fetch_latest_link()
    # download the file and save temporarily
    r = requests.get(url, stream=True)
    filename = '/usr/src/app/prices_latest.xlsx'
    with open(filename, 'wb') as f:
        # save the file on disk
        shutil.copyfileobj(r.raw, f)
    book = load_workbook(filename=filename)
    sheet_prices = book['OMCs and LPGMCs Ex-Pump Prices']
    i = 0
    while True:
        # TODO don't hardcode the expected row (i + 10). it tends to change between files
        name = sheet_prices['E' + str(i + 9)].value
        petrol_price = sheet_prices['F' + str(i + 10)].value
        diesel_price = sheet_prices['G' + str(i + 10)].value

        i = i + 1
        print(name)
        print(petrol_price)
        print(diesel_price)
        if not name:
            break
        if not petrol_price or not diesel_price:
            continue
        petrol_price = round(Decimal(petrol_price) / 100, 2)
        diesel_price = round(Decimal(diesel_price) / 100, 2)

        # todo create omc in mongodb
