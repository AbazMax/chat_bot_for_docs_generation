from bs4 import BeautifulSoup
import pdfkit
import os
from datetime import datetime
import locale
from sys import platform

def generate_pdf_with_data(html_file, output_pdf,user_data):
    """
    Scrapping html template with BeautifulSoup.
    Fill received user data and generate PDF file.

    Args:
        html_file: html template for scraping
        output_pdf: path to generated PDF file
        user_data: dictionary with keys:
                        {'agreement_num': '',
                        'sign_date_d: '',
                        'sign_date_m': '',
                        'sign_date_y': '',
                        'name': '',
                        'passport_ser': '',
                        'passport_num': '',
                        'passport_issued_by': '',
                        'reg_address':, '',
                        'id_code':, '',
                        'mobile_phone': ''}
    """
    with open(html_file, 'r', encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

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

    temp_html_file = 'temp.html'
    with open(temp_html_file, 'w', encoding="utf-8") as file:
        file.write(str(soup))    

    # save PDF file using wkhtmltopdf
    options = {
    'margin-top': '10mm',
    'margin-right': '15mm',
    'margin-bottom': '15mm',
    'margin-left': '15mm'
    }
    
    try:
        pdfkit.from_file(temp_html_file, output_pdf, options=options)
    except OSError:
        path_wkhtmltopdf = os.getenv('PATH_WKHTMLTOPDF')
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)    
        pdfkit.from_file(temp_html_file, output_pdf, options=options, configuration=config)
    os.remove(temp_html_file)

def agr_num_generator(message):
    """
    Generating agreement number. 
    Concists of date in format "ymd" and user id in telegram
    """
    date = datetime.today().strftime("%y%m%d")
    return f'{date}-{message}'

def get_month():
    """Get the month in the Ukrainian language in the genitive case"""
    date = datetime.today()
    if platform == 'win32':
        locale.setlocale(locale.LC_TIME, 'Ukrainian_Ukraine')
        if date.month != 2 and date.month != 11:
            month_name = date.strftime('%B')[:3] + "ня"
        elif date.month == 2:
            month_name = 'лютого'
        elif date.month == 11:
            month_name = 'листопада'
    else:        
        locale.setlocale(locale.LC_TIME, 'uk_UA.utf-8')
        month_name = date.strftime('%B')
    return month_name

def get_day():
    return f'{datetime.today().day}'

def get_year():
    return f'{datetime.today().year}'



