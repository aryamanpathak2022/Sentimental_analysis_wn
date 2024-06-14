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
    
    # Find all headline elements and their links
    headlines = soup.find_all('h3', class_='css-1j88qqx e15t083i0')
    links = [link['href'] for link in soup.select('a.css-8hzhxf')]
    
    # Append base URL to the links
    base_url = "https://www.nytimes.com"
    full_links = [base_url + link for link in links]
    
    # Find all date elements
    dates = soup.find_all('div', class_='css-e0xall e15t083i3')
    
    # Extracting headlines, dates, and links
    headlines_list = [headline.text.strip() for headline in headlines]
    dates_list = [date.text.strip() for date in dates]
    
    # Close the driver for now
    driver.quit()
    
    # Scrape articles
    articles = []
    for link in full_links:
        articles.append(scrape_article(link))
    
    return headlines_list, dates_list, full_links, articles

def scrape_article(url):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()
    
    # Navigate to the article URL
    driver.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract the article text
    paragraphs = soup.find_all('p', class_='css-at9mc1 evys1bk0')
    article_text = " ".join([para.text.strip() for para in paragraphs])

    print(article_text)
    
    # Close the driver
    driver.quit()
    
    return article_text

def save_to_csv(headlines, dates, links, articles):
    with open('headlines.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        print("Number of headlines:", len(headlines))
        for headline, date, link, article in zip(headlines, dates, links, articles):
            print("Appending headline:", headline)
            writer.writerow(['nytimes', headline, date, link, article])

def main():
    # Change the range according to the number of pages you want to scrape
    for page_number in range(1, 4):  # Scraping 3 pages in this example
        url = f'https://www.nytimes.com/spotlight/india?page={page_number}'
        headlines, dates, links, articles = scrape_data(url)
        save_to_csv(headlines, dates, links, articles)

if __name__ == "__main__":
    main()
