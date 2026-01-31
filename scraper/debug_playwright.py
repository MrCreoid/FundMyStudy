from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

URL = "https://www.buddy4study.com/scholarships"

def run_debug():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to {URL}...")
        page.goto(URL, timeout=60000)
        
        # Wait a bit for ANY load
        page.wait_for_timeout(5000)
        
        title = page.title()
        print(f"Page Title: {title}")
        
        # Get content
        html = page.content()
        browser.close()
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Check specific selector
        target_selector = "h4[class^='Listing_scholarshipName']"
        targets = soup.select(target_selector)
        print(f"Selector '{target_selector}' found {len(targets)} elements.")
        
        # Inspect all H4s
        print("\n--- All H4 Elements ---")
        h4s = soup.find_all("h4")
        for i, h4 in enumerate(h4s[:10]):
            print(f"{i+1}. Text: '{h4.get_text(strip=True)}' | Classes: {h4.get('class')}")
            
        # Inspect Articles or cards
        print("\n--- Listing Articles? ---")
        articles = soup.find_all("article")
        print(f"Found {len(articles)} <article> tags.")

if __name__ == "__main__":
    run_debug()
