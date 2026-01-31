from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.buddy4study.com"
URL = BASE_URL + "/scholarships"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)

    
    page.wait_for_selector("h4[class^='Listing_scholarshipName']", timeout=60000)

    html = page.content()
    browser.close()

soup = BeautifulSoup(html, "html.parser")

titles = soup.select("h4[class^='Listing_scholarshipName']")
print("Scholarships found:", len(titles))

data = []

for title in titles:
    try:
        card = title.find_parent("div")

        name = title.get_text(strip=True)

        
        deadline = None
        date_block = card.select_one("div[class^='Listing_calendarDate']")
        if date_block:
            ps = date_block.find_all("p")
            if len(ps) >= 2:
                deadline = ps[1].get_text(strip=True)

        
        award = None
        eligibility = None

        award_blocks = card.select("div[class^='Listing_awardCont']")
        if len(award_blocks) >= 2:
            award = award_blocks[0].select_one("span").get_text(strip=True)
            eligibility = award_blocks[1].select_one("span").get_text(strip=True)

        
        link_tag = card.find("a", href=True)
        link = BASE_URL + link_tag["href"] if link_tag else None

        data.append({
            "scholarship_name": name,
            "deadline": deadline,
            "award": award,
            "eligibility": eligibility,
            "link": link,
            "source": "buddy4study.com"
        })

    except Exception:
        continue

df = pd.DataFrame(data)
df.to_csv("buddy4study_scholarships.csv", index=False)

print(f"Saved {len(df)} scholarships")