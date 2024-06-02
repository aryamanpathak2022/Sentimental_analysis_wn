from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_data(url):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome() 
    
    # Navigate to the URL
    driver.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all headline elements
    headlines = soup.find_all('h3', class_='css-1j88qqx e15t083i0')
    
    # Find all date elements
    dates = soup.find_all('div', class_='css-e0xall e15t083i3')
    
    # Extracting headlines and dates
    headlines_list = [headline.text.strip() for headline in headlines]
    dates_list = [date.text.strip() for date in dates]
    
    # Close the driver
    driver.quit()
    
    return headlines_list, dates_list

def save_to_csv(headlines, dates):
    with open('headlines.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        print("Number of headlines:", len(headlines))
        for headline, date in zip(headlines, dates):
            print("Appending headline:", headline)
            writer.writerow(['nytimes', headline, date])

def main():
    # Change the range according to the number of pages you want to scrape
    for page_number in range(1, 4):  # Scraping 3 pages in this example
        url = f'https://www.nytimes.com/spotlight/india?page={page_number}'
        headlines, dates = scrape_data(url)
        save_to_csv(headlines, dates)

if __name__ == "__main__":
    main()
