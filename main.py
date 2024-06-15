from requests import Session
from bs4 import BeautifulSoup


def scrape_quotes():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    with Session() as work:
        # Авторизация
        work.get('https://quotes.toscrape.com/', headers=headers)
        response = work.get('https://quotes.toscrape.com/login', headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        token = soup.find('form').find('input').get('value')

        data = {
            'csrf_token': token,
            'username': 'username',
            'password': 'password'
        }

        result = work.post("https://quotes.toscrape.com/login", data=data, headers=headers, allow_redirects=True)

        if result.status_code == 200:  # Проверка успешной авторизации
            quotes_list = []
            authors_list = []

            # Получение цитат с нескольких страниц
            page_num = 1
            while True:
                quotes_page = work.get(f'https://quotes.toscrape.com/page/{page_num}/', headers=headers)
                quotes_soup = BeautifulSoup(quotes_page.text, 'lxml')

                quotes = quotes_soup.find_all('span', class_='text')
                authors = quotes_soup.find_all('small', class_='author')

                if not quotes:
                    break  # Если нет цитат, выходим из цикла

                quotes_list.extend([quote.get_text() for quote in quotes])
                authors_list.extend([author.get_text() for author in authors])

                page_num += 1

            return quotes_list, authors_list
        else:
            print("Ошибка входа")
            return None, None

def write_to_file(quotes, authors):
    with open("data.txt", "w", encoding="utf-8") as file:
        for quote, author in zip(quotes, authors):
            file.write(f"Цитата: {quote}\nАвтор: {author}\n\n")

if __name__ == "__main__":
    quotes, authors = scrape_quotes()

    if quotes and authors:
        for quote, author in zip(quotes, authors):
            print(f"Цитаты: {quote}\nАвтор: {author}\n")
        
        write_to_file(quotes, authors)
        print("Результаты сохранены в файл data.txt")
    else:
        print("Не удалось получить цитаты")