Amazon Website Scraper
Description
This project is an Amazon Website Scraper built in Python. It is designed to scrape product information from Amazon, specifically targeting watch listings on the Canadian Amazon website (amazon.ca). The scraper retrieves data like product titles, prices, and other key product details, and saves this information in an Excel file.

Features
Extracts product information from Amazon.ca.
Focuses on watch listings but can be modified for other products.
Stores data in an Excel file for easy access and manipulation.
Requirements
Python 3
Libraries: requests, bs4 (BeautifulSoup), openpyxl, time, random, urllib3
Installation
Ensure Python 3 is installed on your system.
Install required Python libraries using pip:
bash
Copy code
pip install requests beautifulsoup4 openpyxl
Usage
Run the script using Python.
The script will automatically start scraping data from the specified Amazon page.
After completing the scraping process, the data will be saved in an Excel file named 'productList.xlsx' in your current working directory.
How It Works
The script uses a list of user-agent headers to simulate browser requests.
It sends a request to the Amazon watches listing page and parses the HTML content.
For each product link found, it visits the product page and extracts details like title, price, and other key information.
This data is then written to an Excel sheet.
Limitations
The scraper is set to a fixed URL and focuses only on watch listings.
It is configured to scrape a maximum of 5 product pages per iteration.
User intervention is required to continue scraping after each iteration.
Note
Web scraping can be subject to legal and ethical considerations. Ensure compliance with Amazon's terms of service and relevant laws before using this script.

