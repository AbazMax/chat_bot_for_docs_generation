# Telegram chat bot for generating documents 
Generate a PDF document based on  html template.
Bot based on Aiogram, it let to be absolutely asynchronous in working 
with many users at a time.
All user data save in the user state and deletes after generating the file. It makes you sure that data will not be saved anywhere except the document.

For filling HTML templace used BeautifulSoup4.
For converting HTML file to PDF used Wkhtmltopdf.

## Running

1. Clone repository
```
https://github.com/AbazMax/chat_bot_for_docs_generation.git
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Create .env file and use your telegram Token
4. Run main file
```
python main.py
```

