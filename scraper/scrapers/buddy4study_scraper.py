from bs4 import BeautifulSoup
import re
import logging
import sys

# Try importing playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright not found. Please run: pip install playwright && playwright install")

class Buddy4StudyScraper:
    def __init__(self):
        self.base_url = "https://www.buddy4study.com"
        self.url = f"{self.base_url}/scholarships"
        self.logger = logging.getLogger(__name__)

    def scrape(self):
        self.logger.info("Starting Buddy4Study scraping (using Playwright)...")
        scholarships = []
        
        try:
            with sync_playwright() as p:
                # Launch browser (Firefox is more stable on some environments)
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                
                self.logger.info(f"Navigating to {self.url}...")
                page.goto(self.url, timeout=90000) # Increased timeout
                
                # Wait for content to load
                try:
                    page.wait_for_selector("h4[class^='Listing_scholarshipName']", timeout=60000)
                except Exception as e:
                    self.logger.error(f"Timeout waiting for selector: {e}")
                    # Capture screenshot or content for debug if needed, but just returning for now
                    browser.close()
                    return []

                # Get HTML content
                html = page.content()
                browser.close()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            
            titles = soup.select("h4[class^='Listing_scholarshipName']")
            self.logger.info(f"Found {len(titles)} potential scholarships")

            for title in titles:
                try:
                    card = title.find_parent("div")
                    name = title.get_text(strip=True)
                    
                    # Skip junk
                    if any(x in name.lower() for x in ["application status", "one time registration", "otr"]):
                        continue

                    # Extract Deadline
                    deadline = "Not specified"
                    date_block = card.select_one("div[class^='Listing_calendarDate']")
                    if date_block:
                        ps = date_block.find_all("p")
                        if len(ps) >= 2:
                            deadline = ps[1].get_text(strip=True)

                    # Extract Award & Eligibility text
                    award = "Variable Award"
                    eligibility_text = ""
                    
                    award_blocks = card.select("div[class^='Listing_awardCont']")
                    if len(award_blocks) >= 2:
                        award = award_blocks[0].select_one("span").get_text(strip=True)
                        eligibility_text = award_blocks[1].select_one("span").get_text(strip=True)

                    # Extract Link
                    link = self.base_url
                    link_tag = card.find("a", href=True)
                    if link_tag:
                        href = link_tag["href"]
                        if href.startswith("http"):
                            link = href
                        else:
                            link = self.base_url + href

                    # Parse conditions
                    conditions = self._parse_conditions(eligibility_text)

                    scholarship = {
                        "name": name,
                        "provider": "Buddy4Study Partner",
                        "amount": award,
                        "deadline": deadline,
                        "description": f"Eligibility: {eligibility_text}",
                        "application_link": link,
                        "source": "buddy4study_real",
                        "category": "Private/Corporate",
                        "active": True,
                        "eligibility_conditions": conditions,
                        "eligibility_text": eligibility_text
                    }
                    
                    scholarships.append(scholarship)

                except Exception as e:
                    self.logger.warning(f"Error parsing card: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            
        self.logger.info(f"Successfully scraped {len(scholarships)} scholarships from Buddy4Study")
        return scholarships

    def _parse_conditions(self, text):
        """
        Heuristic parser to convert raw eligibility text into structured conditions
        """
        conditions = []
        text_lower = text.lower()

        # 1. Class/Course Parsing
        if "class" in text_lower:
            range_match = re.search(r'class\s*(\d{1,2})\s*(?:-|to)\s*(\d{1,2})', text_lower)
            if range_match:
                start, end = map(int, range_match.groups())
                classes = [f"Class {i}" for i in range(start, end + 1)]
                conditions.append({
                    "field": "course",
                    "operator": "IN",
                    "value": classes
                })
            else:
                single_match = re.search(r'class\s*(\d{1,2})', text_lower)
                if single_match:
                    conditions.append({
                        "field": "course",
                        "operator": "==",
                        "value": f"Class {single_match.group(1)}"
                    })

        if any(w in text_lower for w in ["graduation", "degree", "engineering", "bachelor", "undergraduate"]):
             conditions.append({
                "field": "course", 
                "operator": "IN", 
                "value": ["B.Tech", "B.Sc", "B.Com", "B.A.", "BBA", "BCA", "MBBS", "LLB", "B.Arch", "B.Pharm"]
            })
        
        if "diploma" in text_lower:
            conditions.append({"field": "course", "operator": "==", "value": "Diploma"})

        # 2. Income Parsing
        if "income" in text_lower:
            income_match = re.search(r'(\d+(?:\.\d+)?)\s*lakh', text_lower)
            if income_match:
                amount_lakhs = float(income_match.group(1))
                amount = amount_lakhs * 100000
                conditions.append({
                    "field": "income",
                    "operator": "<=",
                    "value": amount
                })

        # 3. Marks Parsing
        marks_match = re.search(r'(\d+)%', text_lower)
        if marks_match:
            conditions.append({
                "field": "marks",
                "operator": ">=",
                "value": float(marks_match.group(1))
            })

        return conditions
