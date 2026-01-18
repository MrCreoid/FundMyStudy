"""
Mock scraper for demo/testing
Returns realistic scholarship data
"""
from datetime import datetime, timedelta
import random

class MockScholarshipScraper:
    def __init__(self):
        self.source = "mock"
        print(f"🎭 Initialized MockScraper (source: {self.source})")
    
    def scrape(self):
        """Return mock scholarship data focusing on STATE scholarships"""
        print("🏛️  Generating STATE scholarship mock data...")
        
        # Current date for deadlines
        now = datetime.now()
        
        mock_scholarships = [
            # STATE SCHOLARSHIPS (These are the focus)
            {
                "name": "Maharashtra Government Scholarship for OBC Students",
                "provider": "Government of Maharashtra",
                "description": "State scholarship for OBC students who are residents of Maharashtra pursuing higher education.",
                "amount": "Full tuition fee waiver + exam fees",
                "deadline": (now + timedelta(days=30)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "state", "operator": "==", "value": "Maharashtra"},
                    {"field": "caste", "operator": "==", "value": "OBC"},
                    {"field": "income", "operator": "<=", "value": 80000}
                ],
                "source_url": "https://mahadbt.maharashtra.gov.in",
                "application_link": "https://mahadbt.maharashtra.gov.in/SchemeData/SchemeData?str=EBC",
                "official_only": True,
                "category": "State-specific",
                "state_specific": True,
                "state": "Maharashtra",
                "source": "state_mock",
                "icon": "🏛️"
            },
            {
                "name": "UP Government Minority Scholarship",
                "provider": "Government of Uttar Pradesh",
                "description": "Pre-Matric and Post-Matric scholarship for minority students studying in Uttar Pradesh.",
                "amount": "₹5,000 per annum + admission fee",
                "deadline": (now + timedelta(days=50)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "state", "operator": "==", "value": "Uttar Pradesh"},
                    {"field": "category", "operator": "==", "value": "Minority"},
                    {"field": "income", "operator": "<=", "value": 200000}
                ],
                "source_url": "https://scholarship.up.gov.in",
                "application_link": "https://scholarship.up.gov.in/ApplicationForm.aspx",
                "official_only": True,
                "category": "Minority",
                "state_specific": True,
                "state": "Uttar Pradesh",
                "source": "state_mock",
                "icon": "🕌"
            },
            {
                "name": "Delhi SC/ST/OBC/Minority Scholarship",
                "provider": "Government of Delhi",
                "description": "Scholarship for SC/ST/OBC/Minority students residing in Delhi.",
                "amount": "₹15,000-30,000 per annum",
                "deadline": (now + timedelta(days=40)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "state", "operator": "==", "value": "Delhi"},
                    {"field": "income", "operator": "<=", "value": 300000}
                ],
                "source_url": "https://delhi.gov.in/scholarship",
                "application_link": "https://delhi.gov.in/scholarship/apply",
                "official_only": True,
                "category": "State-specific",
                "state_specific": True,
                "state": "Delhi",
                "source": "state_mock",
                "icon": "🏙️"
            },
            
            # CENTRAL GOVERNMENT SCHOLARSHIPS (Other ministries)
            {
                "name": "Girl Child Scholarship for Higher Education",
                "provider": "Ministry of Women & Child Development",
                "description": "Encourages education of girl children from BPL families. For girls pursuing graduate/post-graduate courses.",
                "amount": "₹10,000 per annum for maximum 2 years",
                "deadline": (now + timedelta(days=40)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "income", "operator": "<=", "value": 150000},
                    {"field": "marks", "operator": ">=", "value": 75}
                ],
                "source_url": "https://wcd.nic.in",
                "application_link": "https://wcd.nic.in/schemes/girl-child-scholarship",
                "official_only": True,
                "category": "Gender-based",
                "state_specific": False,
                "source": "central_mock",
                "icon": "👧"
            },
            {
                "name": "AICTE Scholarship for Technical Education",
                "provider": "All India Council for Technical Education (AICTE)",
                "description": "For students pursuing diploma/degree courses in AICTE approved institutions. Includes PRAGATI scheme for girls.",
                "amount": "₹30,000 per annum + contingency grant",
                "deadline": (now + timedelta(days=35)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "course", "operator": "IN", "value": ["B.Tech", "B.E.", "M.Tech", "Diploma", "Polytechnic"]},
                    {"field": "income", "operator": "<=", "value": 800000},
                    {"field": "marks", "operator": ">=", "value": 65}
                ],
                "source_url": "https://www.aicte-india.org",
                "application_link": "https://www.aicte-india.org/schemes/students/scholarship",
                "official_only": True,
                "category": "Technical",
                "state_specific": False,
                "source": "central_mock",
                "icon": "⚙️"
            }
        ]
        
        print(f"✅ Generated {len(mock_scholarships)} mock scholarships (focus on state)")
        return mock_scholarships