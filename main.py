import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import random
import urllib3

# URL of the Amazon product page you want to scrape
headersList = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.1; rv:109.0) Gecko/20100101 Firefox/120.0', 	
'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/120.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36','Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.50 Mobile/15E148 Safari/604.1']

url = 'https://www.amazon.ca/s?k=watches&dc&crid=1I9UCV2J7SYGG&sprefix=watces%2Caps%2C242&ref=a9_sc_1'
headers = {
    'User-Agent': random.choice(headersList),
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip', 
    'DNT' : '1', # Do Not Track Request Header 
    'Connection' : 'close'
}
def Scrape():
    global wb
    wb = openpyxl.Workbook()
    global sheet
    sheet = wb.active

    empty = True
    print("Starting to scrape")
    while empty:
        time.sleep(5)
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        webpageLinks = soup.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        print("Scraping...")
        if webpageLinks:
            empty = False
    iterations = 0
    max_iterations = 5
    header_written = False

    for link in webpageLinks:
        var = True
        href = link.get('href')
        amazonLink = "https://www.amazon.ca" + href
        time.sleep(5)
        newWebpage = requests.get(amazonLink, headers=headers)
        soup2 = BeautifulSoup(newWebpage.content, 'html.parser')
        soup2Prettified = BeautifulSoup(soup2.prettify(), "html.parser")

        try:
            title = soup2Prettified.find(id="productTitle").get_text().strip()
            price = soup2Prettified.find(class_="a-price-whole")
            priceFraction = soup2Prettified.find(class_="a-price-fraction")
            table = soup2Prettified.find('table', class_='a-keyvalue a-spacing-mini')

            price_text = ""

            if price is not None:
                price_text += price.get_text().strip()

            if priceFraction is not None:
                price_text += priceFraction.get_text().strip()

            priceList = price_text.split()
            price_text = ""
            for i in priceList:
                price_text += i
            global product_info
            product_info = {}
            for row in table.find_all('tr'):
                header = row.find('th').get_text().strip()
                data = row.find('td').get_text().strip()        
                product_info[header] = data

            for key, value in product_info.items():
                print(f"{key}: {value}")

            print(title, end="\n")
            print(price_text)

            if not header_written:
                header = ['Product', 'Price'] + list(product_info.keys())
                sheet.append(header)
                header_written = True
                
            row_data = [title, price_text] + list(product_info.values())
            sheet.append(row_data)

            

            iterations += 1

            if iterations == max_iterations:
                iterations = 0
                print("Continuing to the next set of iterations.")
                user_input = input("Press '1' to stop scraping or press Enter to continue: ")
                if user_input == '1':
                    print('Scraping stopped \nResult Has Been Successfully Saved in Your Current Working Directory.')
                    break
                else: 
                    continue

        except Exception as e:
            print(f"Error! Could not retrieve information for {amazonLink}: {e}")




Scrape()
wb.save('productList.xlsx')

