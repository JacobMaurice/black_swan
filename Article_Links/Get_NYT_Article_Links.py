from bs4 import BeautifulSoup
import random
from playwright.sync_api import sync_playwright
import pandas as pd
import time

# Returns a list containing the links on the current page
def GetArticleLinks(page, links_list):
    html = page.content()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all divs with the specific class pattern
    article_divs = soup.find_all('li', class_='css-1l4w6pd')

    # Iterate through the found divs
    for div in article_divs:
        # Extract the title text
        title = div.find('h4', class_='css-nsjm9t').get_text(strip=True)

        # Extract date published
        date = div.find('span', class_='css-17ubb9w').get_text(strip=True)
        
        # Extract the link
        link = "https://www.nytimes.com" + div.find('a')['href']

        links_list.append({
            'Title': title,
            'Date': date,
            'Link': link
        })
        
    return links_list


def ClickShowMoreUntilGone(page):
    while True:
        try:
            # Wait for and click the "Show More" button
            page.wait_for_selector('button[data-testid="search-show-more-button"]', timeout=5000)
            page.click('button[data-testid="search-show-more-button"]')
            
            # Wait for new content to load
            time.sleep(1)  # Adjust this delay as needed
            
            # Optional: Scroll to trigger lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            
        except Exception as e:
            # Button not found - we're done
            print("No more 'Show More' button found")
            break


USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
]

links_list = []
url = "https://www.nytimes.com/search?dropmab=false&endDate=2008-12-31&lang=en&query=Subprime%20Mortgage%20Crisis&sections=Business%7Cnyt%3A%2F%2Fsection%2F0415b2b0-513a-5e78-80da-21ab770cb753&sort=oldest&startDate=2008-11-01&types=article"
file_name = 'Articles_2008_11-12.csv'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(user_agent=random.choice(USER_AGENTS))
    
    # Set longer timeout for initial page load
    page.set_default_timeout(10000)
    
    page.goto(url)
    
    # Click all "Show More" buttons
    ClickShowMoreUntilGone(page)
    
    # Now scrape all loaded articles
    links_list = GetArticleLinks(page, links_list)
    
    # Optional: Save to CSV
    pd.DataFrame(links_list).to_csv(file_name, index=False)
    
    browser.close()

print(f"Found {len(links_list)} articles")