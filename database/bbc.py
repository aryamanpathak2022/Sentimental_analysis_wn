from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def fetch_bbc_headlines(pages=5):
    headlines = []
    dates = []
    links = []
    
    url = "https://www.bbc.com/news/world/asia/india"
    
    # Set up the Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (you can adjust the sleep time)
        
        for page in range(pages):
            # Use WebDriverWait to wait until the news items are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h3"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract headlines
            for article in soup.find_all('h3', class_='gs-c-promo-heading__title'):
                headlines.append(article.text.strip())
            
            # Extract dates
            for date_element in soup.find_all('time', class_='qa-status-date'):
                dates.append(date_element.text.strip())
                
            # Extract links and append base URL
            for link_element in soup.find_all('a', class_='gs-c-promo-heading', href=True):
                link = "https://www.bbc.com" + link_element['href']
                links.append(link)
            
            # Click on the next page button
            next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-next-button']")
            next_page_button.click()
            time.sleep(5)  # Wait for the new page to load
        
    finally:
        driver.quit()

    return headlines, dates, links

def append_to_csv(headlines, dates, links):
    with open('headlines.csv', 'a', newline='') as csvfile:
        fieldnames = ['Company_name', 'Headline', 'Date', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write each headline, date, and link as a row in the CSV file
        for i in range(len(headlines)):
            writer.writerow({'Company_name': "BBC", 'Headline': headlines[i], 'Date': dates[i], 'Link': links[i]})

if __name__ == "__main__":
    headlines, dates, links = fetch_bbc_headlines(pages=3)
    
    # Print first headline and corresponding date in loop
    for i in range(len(headlines)):
        print(headlines[i], dates[i])
    
    # Append headlines, dates, and links to CSV file
    append_to_csv(headlines, dates, links)
