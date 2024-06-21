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
    articles = []
    links = []

    url = "https://edition.cnn.com/search?q=india&from=0&size=10&page=1&sort=newest&types=article&section="
    
    # Set up the Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load (you can adjust the sleep time)
        
        # Optional navigation for pagination
        # try:
        #     next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-next-button']")
        #     next_page_button.click()
        #     time.sleep(10)
        #     next_page_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='pagination-back-button']")
        #     next_page_button.click()
        #     time.sleep(10)
        # except:
        #     pass  # If pagination buttons are not found, continue without them

        for page in range(pages):
            # Use WebDriverWait to wait until the news items are loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "span"))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract headlines
            for article in soup.find_all('span', class_='container__headline-text'):
                headlines.append(article.text.strip())
                
            for date_element in soup.find_all('div', class_='container__date container_list-images-with-description__date inline-placeholder'):
                dates.append(date_element.text.strip())
                
            for link_element in soup.find_all('span', class_='container__headline-text', href=True):
                link =  link_element['href']
                print(link_element['href'])

                links.append(link)

            # Navigate to the next page if there is one
            try:
                print("hello")
                next_page_button = driver.find_element(By.CLASS_NAME, "pagination-arrow pagination-arrow-right search__pagination-link text-active")
                next_page_button.click()
                time.sleep(15)  # Wait for the new page to load
            except:
                print("error-hello")
                break  # Exit the loop if there are no more pages

    finally:
        driver.quit()
    
    # Scrape full articles
    print(dates)
    for link in range(len(links)):
        print(links[link])
        articles.append(scrape_article(links[link]))
        # save to csv
        with open('headlines.csv', 'a', newline='', encoding='utf-8') as file:
             writer = csv.writer(file)
             writer.writerow(['bbc', headlines[link], dates[link], links[link], articles[link]])

    
    return headlines, dates, links, articles

def scrape_article(url):
    # Set up the Chrome webdriver
    driver = webdriver.Chrome()
    
    try:
        # Navigate to the article URL
        driver.get(url)
        
        # Parse the HTML content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract the article text
        paragraphs = soup.find_all('p', class_='paragraph inline-placeholder vossi-paragraph-primary-core-light')
        article_text = " ".join([para.text.strip() for para in paragraphs])
        print(article_text)
        
    finally:
        driver.quit()
    
    return article_text

def save_to_csv(headlines, dates, links, articles):
    with open('headlines.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for headline, date, link, article in zip(headlines, dates, links, articles):
            writer.writerow(['cnn', headline, date, link, article])

if __name__ == "__main__":
    headlines, dates, links, articles = fetch_bbc_headlines(pages=15)
    save_to_csv(headlines, dates, links, articles)
    
    # Print the results for verification
    # for i in range(len(headlines)):
    #     print(f"Headline: {headlines[i]}, Date: {dates[i]}, Link: {links[i]}, Article: {articles[i][:100]}...")
