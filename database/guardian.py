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
    url = "https://www.theguardian.com/world/india"
    
    # Set up the Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(10)  # Wait for the page to load (you can adjust the sleep time)
        svg_button_xpath = "//svg[contains(@aria-hidden, 'true')]/path"
        button_xpath = '//*[@id="notice"]/div[3]/div/div/button[1]'
        
        

        no_thank_you_button = driver.find_element(By.XPATH, button_xpath)
        no_thank_you_button.click()
        for page in range(pages):
            # Use WebDriverWait to wait until the news items are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "h2"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Extract headlines
            # print(soup.find_all('h2', class_='sc-2c72d884-3 fWWpXO'))
            for article in soup.find_all('a', class_='dcr-lv2v9o'):
                headline.append(article.get_text(strip=True))
            # print(soup.find_all('span', class_='sc-df20d569-1 fbRULV'))
            for dates in soup.find_all('h2', class_='dcr-r2qp9x'):
                
                if dates:
                    date.append( dates.text.strip())
            # for item in soup.find_all('div', class_='sc-da05643e-0 kbaPPZ'):
            #     if item:
            #         headlines.append(item.text.strip())
            
            # Click on the next page button
            svg_button = driver.find_element(By.XPATH, svg_button_xpath)
            svg_button.click()
            time.sleep(5)  # Wait for the new page to load # Wait for the new page to load
        
    finally:
        driver.quit()
        

    return (headline,date)

if __name__ == "__main__":
    headline,date = fetch_bbc_headlines(pages=1)
    # print first headline than corresponding date in loop
    for i in range(len(headline)):
        print(headline[i], date[i])
    
    