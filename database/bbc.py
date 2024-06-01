from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_bbc_headlines(pages=5):
    headline=[]
    date=[]
    articles = []
    url = "https://www.bbc.com/news/world/asia/india"
    
    # Set up the Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (you can adjust the sleep time)
        
        next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-next-button']")
        next_page_button.click()
        time.sleep(10) 
        next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-back-button']")
        next_page_button.click()
        time.sleep(10) 
        for page in range(pages):
            # Use WebDriverWait to wait until the news items are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Extract headlines
            # print(soup.find_all('h2', class_='sc-2c72d884-3 fWWpXO'))
            for article in soup.find_all('h2', class_='sc-2c72d884-3 fWWpXO'):
                headline.append(article.text.strip())
            # print(soup.find_all('span', class_='sc-df20d569-1 fbRULV'))
            for dates in soup.find_all('span', class_='sc-df20d569-1 fbRULV'):
                
                if dates:
                    date.append( dates.get_text(strip=True))
            # for item in soup.find_all('div', class_='sc-da05643e-0 kbaPPZ'):
            #     if item:
            #         headlines.append(item.text.strip())
            
            # Click on the next page button
            next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-next-button']")
            next_page_button.click()
            time.sleep(15)  # Wait for the new page to load # Wait for the new page to load
        
    finally:
        driver.quit()
        

    return (headline,date)

if __name__ == "__main__":
    headline,date = fetch_bbc_headlines(pages=1)
    # print first headline than corresponding date in loop
    for i in range(len(headline)):
        print(headline[i], date[i])
    
    