from bs4 import BeautifulSoup
import random
from playwright.sync_api import sync_playwright
import pandas as pd
import time

# Constants
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
]

def GetArticleBodies():
    start = 350 # Article number is actually start+1 because of indexing starting at 0
    end = 400
    nyt_articles = pd.read_csv('../Article_Links/NYT_Article_Links.csv')
    all_article_bodies = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = context.new_page()

        for i, row in nyt_articles.iloc[start:end].iterrows():

            article_url = row['Link']
            link = f"https://accessarticlenow.com/api/c/js?q={article_url}"
            print(f"Processing article {i+1}/{len(nyt_articles)}: {link}")

            try:
                page.goto(link, timeout=15000)
                
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all paragraphs in the article
                article_body = soup.find('section', {'name': 'articleBody'})
                article_paragraphs = article_body.find_all('p')

                # Store the concatenation of all the paragrpahs
                text_concat = ""

                # Loop through every paragraph and add them to text_concat
                for p in article_paragraphs:
                    text = p.get_text(strip=True)
                    text_concat += text
                
                # Add the completed body to the list of article bodies
                all_article_bodies.append(text_concat)
                            
                # Add delay between requests
                page.wait_for_timeout(random.randint(2000, 5000))
                
            except Exception as e:
                print(f"Error processing {link}: {str(e)}")
                all_article_bodies.append("")
            
            time.sleep(random.randint(3,6))

        browser.close()

    pd.DataFrame(all_article_bodies).to_csv(f"NYT_Articles({start+1}-{end}).csv")

# Run the scraper
GetArticleBodies()