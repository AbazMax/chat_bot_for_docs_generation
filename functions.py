from bs4 import BeautifulSoup
import pdfkit
import os
from datetime import datetime
import locale

def generate_pdf_with_data(html_file, output_pdf,user_data):
    with open(html_file, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Знаходимо елементи, в які потрібно вставити дані
    agreement_num_element = soup.find(id='agreement_num')
    sign_date_d_element = soup.find(id='sign_date_d')
    sign_date_m_element = soup.find(id='sign_date_m')
    sign_date_y_element = soup.find(id='sign_date_y')    
    name_element = soup.find(id='name')
    passport_ser_element = soup.find(id='passport_ser')
    passport_num_element = soup.find(id='passport_num')
    passport_issued_by_element = soup.find(id='passport_issued_by')
    reg_address_element = soup.find(id='reg_address')
    id_code_element = soup.find(id='id_code')
    mobile_phone_element = soup.find(id='mobile_phone')
    
    # Вставляємо дані в елементи
    agreement_num_element.string = user_data['agreement_num']
    sign_date_d_element.string = user_data['sign_date']['day']
    sign_date_m_element.string = user_data['sign_date']['month']
    sign_date_y_element.string = user_data['sign_date']['year']
    name_element.string = user_data['name']
    passport_ser_element.string = user_data['passport_ser']
    passport_num_element.string = user_data['passport_num']
    passport_issued_by_element.string = user_data['passport_issued_by']
    reg_address_element.string = user_data['reg_address']
    id_code_element.string = user_data['id_code']
    mobile_phone_element.string = user_data['mobile_phone']

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

def agr_num_generator(message):
    date = datetime.today().strftime("%y%m%d")
    return f'{date}-{message}'

def get_month():
    date = datetime.today()
    
    # Встановлюємо українську локалізацію
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
    
    # Отримуємо назву місяця українською
    month_name = date.strftime('%B')
    
    # Повертаємо назву місяця
    return month_name

def get_day():
    return f'{datetime.today().day}'

def get_year():
    return f'{datetime.today().year}'



