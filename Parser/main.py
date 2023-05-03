from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def get_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    site = url
    driver.get(site)
    time.sleep(5)

    page_source = driver.page_source

    with open('index.html', 'w', encoding = 'utf-8-sig') as file:
            file.write(page_source)

    with open('index.html', encoding = 'utf-8-sig') as file:
            src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('article', {'data-name': 'CardComponent'})
    count = 0

    result_list = []
   
    for card in cards:
        card_geo = card.find(class_ = '_93444fe79c--labels--L8WyJ').text
        card_rent = card.find('span', {'data-mark': 'MainPrice'}).find('span').text.replace(' ', '').replace('₽/мес.', '')
        card_links = card.find('a', {'target': '_blank'}).get('href')
        card_description = card.find(attrs={'data-name': 'Description'}).find('p')
        descr = card_description.text.replace('\n', '')
        card_title = card.find('span', {'data-mark': 'OfferTitle'}).text
        count += 1  
        result_list.append(
        {
            'Id': count,
            "Price": int(card_rent),
            "Title": card_title,
            "Descripion": descr,
            "Location": card_geo,
            "Link": card_links
        }
        )


    with open('Not_filtered_result.json', 'w', encoding = 'utf-8-sig') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    with open('Not_filtered_result.json', encoding = 'utf-8-sig') as file:
        not_full = json.load(file)
    
    price_down = sorted(not_full, key=lambda price: price['Price'])
    
    with open('Down_filtered_result.json', 'w', encoding = 'utf-8-sig') as file:
        json.dump(price_down, file, indent=4, ensure_ascii=False)


    return "Wake up, Neo..."





if __name__ == '__main__':
    get_data('https://www.cian.ru/snyat-kvartiru-bez-posrednikov/')
