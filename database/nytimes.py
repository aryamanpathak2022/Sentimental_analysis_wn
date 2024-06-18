from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv


def scrape_data(url):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    # Parse the HTML content (consider using WebDriverWait for dynamic content)
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

    # Close the driver
    driver.quit()

    # Scrape articles and write to CSV
    for link, headline, date in zip(full_links, headlines_list, dates_list):
        article_text = scrape_article(link)

        # Open CSV in append mode for each article
        with open('headlines.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['nytimes', headline, date, link, article_text])


def scrape_article(url):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()

    # Navigate to the article URL
    driver.get(url)

    # Scroll down to load all content (replace with your scroll strategy)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust wait time as needed

            # Check if scrolling reached the end (replace with a better condition)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        except TimeoutException:
            # Handle timeout exceptions if scrolling takes too long
            print(f"Timeout waiting for element on {url}")
            break

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the article text
    paragraphs = soup.find_all('p', class_='css-at9mc1 evys1bk0')
    article_text = " ".join([para.text.strip() for para in paragraphs])

    # Close the driver
    driver.quit()

    return article_text


def main():
    # Change the range according to the number of pages you want to scrape
    for page_number in range(1, 15):  # Scraping 3 pages in this example
        url = f'https://www.nytimes.com/spotlight/india?page={page_number}'
        scrape_data(url)


if __name__ == "__main__":
    main()
