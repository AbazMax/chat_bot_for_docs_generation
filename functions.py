from bs4 import BeautifulSoup
import pdfkit
import os
from user_data import UserData
from datetime import datetime
import locale

def generate_pdf_with_data(html_file, output_pdf,user_data):
    # Завантажуємо HTML-файл

    with open(html_file, 'r') as file:
        html_content = file.read()


    # Створюємо об'єкт BeautifulSoup для обробки HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Знаходимо елементи, в які потрібно вставити дані
    agreement_num_element = soup.find(id='agreement_num')
    sign_date_d_element = soup.find(id='sign_date_d')
    sign_date_m_element = soup.find(id='sign_date_m')
    sign_date_y_element = soup.find(id='sign_date_y')    
    name_element = soup.find(id='name')
    surname_element = soup.find(id='surname')
    passport_ser_element = soup.find(id='passport_ser')
    passport_num_element = soup.find(id='passport_num')
    passport_issued_by_element = soup.find(id='passport_issued_by')
    passport_issue_date_element = soup.find(id='passport_issue_date')
    reg_address_element = soup.find(id='reg_address')
    id_code_element = soup.find(id='id_code')
    mobile_phone_element = soup.find(id='mobile_phone')
    
    # Вставляємо дані в елементи
    agreement_num_element.string = user_data.agreement_num
    sign_date_d_element.string = user_data.sign_date['day']
    sign_date_m_element.string = user_data.sign_date['month']
    sign_date_y_element.string = user_data.sign_date['year']
    name_element.string = user_data.name
    surname_element.string = user_data.surname
    passport_ser_element.string = user_data.passport_ser
    passport_num_element.string = user_data.passport_num
    passport_issued_by_element.string = user_data.passport_issued_by
    passport_issue_date_element.string = user_data.passport_issue_date
    reg_address_element.string = user_data.reg_address
    id_code_element.string = user_data.id_code
    mobile_phone_element.string = user_data.mobile_phone

    # Зберігаємо змінений HTML у тимчасовий файл
    temp_html_file = 'temp.html'
    with open(temp_html_file, 'w') as file:
        file.write(str(soup))    

    # Зберігаємо PDF-файл використовуючи wkhtmltopdf
    options = {
    'margin-top': '10mm',
    'margin-right': '15mm',
    'margin-bottom': '15mm',
    'margin-left': '15mm'
    }
    
    pdfkit.from_file(temp_html_file, output_pdf, options=options)

    # Видаляємо тимчасовий HTML-файл
    os.remove(temp_html_file)

# Приклад використання
data = UserData()

html_file = './template/agreement_template.html'
output_pdf = './agreements/output.pdf'
data.agreement_num = '010101'
data.sign_date['day'] = '01'
data.sign_date['month'] = 'квітня'
data.sign_date['year'] = '2023'
data.name = 'Наталія'
data.surname = 'Щербина'
data.passport_ser = 'AB'
data.passport_num = '333555'
data.passport_issued_by = 'якимось РУГУ в якогось району деякого міста'
data.passport_issue_date = '01.01.01'
data.reg_address = 'м. Київ, вул. Хрещатик 1, кв. 1'
data.id_code = '123456789'
data.mobile_phone = '+380993331122'

generate_pdf_with_data(html_file, output_pdf, data)


def agr_num_generator(message):
    date = datetime.today().strftime("%y%m%d")
    return f'{date}-{message}'


def get_month():
    date = datetime.datetime.today()
    
    # Встановлюємо українську локалізацію
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    
    # Отримуємо назву місяця українською
    month_name = date.strftime('%B')
    
    # Повертаємо назву місяця
    return month_name

print(get_month())

def get_day():
    return datetime.today().day

def get_day():
    return datetime.today().year
