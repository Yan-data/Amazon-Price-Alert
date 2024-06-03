import csv
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os
ALERT_PRICE = 90
URL = os.environ.get('URL')
print(URL)
USER_AGENT = os.environ.get('USER_AGENT')
ACCEPT_LANGUAGE = os.environ.get('ACCEPT_LANGUAGE')
SMTP_ADDRESS = os.environ.get('SMTP_ADDRESS')
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
headers = {
    'Accept-Language': ACCEPT_LANGUAGE,
    'User-Agent': USER_AGENT,
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"'
}


def check_price():
    # get price data
    response = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    price_tag = soup.find(class_="aok-offscreen")
    price = float(price_tag.getText().split('$')[1])
    title = soup.find(id="productTitle").get_text().strip()
    today = datetime.now().date()
    data = [title, price, today]
    # save data to csv
    with open(f'amazon_price_list', 'a+', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    def send_email():
        message = f"{title} is now {price}"
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            result = connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
            )
    # send email when price is below alert limit
    if price <= ALERT_PRICE:
        send_email()


# run the program every 24 hours
while True:
    check_price()
    time.sleep(86400)