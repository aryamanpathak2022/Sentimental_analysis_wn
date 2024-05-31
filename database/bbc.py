from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_bbc_headlines(pages=5):
    headlines = []
    dates = []
    url = "https://www.bbc.com/news/world/asia/india"
    
    # Set up the Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (you can adjust the sleep time)
        
        for page in range(pages):
            # Use WebDriverWait to wait until the news items are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract headlines
            for article in soup.find_all('h2', class_='sc-2c72d884-3 fWWpXO'):
                if article:
                    headlines.append(article.get_text(strip=True))
            
            # Extract dates
            for date in soup.find_all('span', {'data-testid': 'card-metadata-lastupdated'}):
                if date:
                    dates.append(date.get_text(strip=True))
            
            # Click on the next page button
            next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-next-button']")
            next_page_button.click()
            time.sleep(3)  # Wait for the new page to load
        
    finally:
        driver.quit()

    return headlines, dates

if __name__ == "__main__":
    headlines, dates = fetch_bbc_headlines(pages=1)
    # Print first headline then corresponding date in loop
    for i in range(len(headlines)):
        print(headlines[i], dates[i])
