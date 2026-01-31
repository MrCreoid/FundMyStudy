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
        # DISABLED: User requested to remove "Buddy4Study Partner" scholarships
        self.logger.info("⚠️  Buddy4Study scraper is DISABLED by configuration")
        return []

        # Original scraping logic commented out effectively by returning above
        scholarships = []
        
        try:
            with sync_playwright() as p:
                # ... (rest of code code be here but we just return early)
                pass
        except Exception:
            pass
            
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
