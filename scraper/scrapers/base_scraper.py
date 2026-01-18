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
        """Return mock scholarship data"""
        print("🔄 Generating mock scholarships...")
        
        # Current date for deadlines
        now = datetime.now()
        
        mock_scholarships = [
            {
                "name": "Post Matric Scholarship for Minorities",
                "provider": "Ministry of Minority Affairs, Government of India",
                "description": "Scholarship for students from minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) pursuing post-matriculation or post-secondary courses.",
                "amount": "Up to ₹20,000 per annum",
                "deadline": (now + timedelta(days=60)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "income", "operator": "<=", "value": 250000},
                    {"field": "category", "operator": "==", "value": "Minority"},
                    {"field": "marks", "operator": ">=", "value": 50}
                ],
                "source_url": "https://scholarships.gov.in",
                "application_link": "https://scholarships.gov.in/portal/MinistryScholarships",
                "official_only": True,
                "category": "Post-Matric",
                "state_specific": False,
                "source": self.source,
                "icon": "🎓"
            },
            {
                "name": "National Merit Scholarship Scheme",
                "provider": "Department of Higher Education, Ministry of Education",
                "description": "For meritorious students from low-income families pursuing professional courses like Engineering, Medicine, Architecture, etc.",
                "amount": "₹12,000 per annum for 10 months",
                "deadline": (now + timedelta(days=45)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "income", "operator": "<=", "value": 600000},
                    {"field": "marks", "operator": ">=", "value": 80},
                    {"field": "course", "operator": "IN", "value": ["B.Tech", "MBBS", "B.Arch", "BDS", "B.Pharma"]}
                ],
                "source_url": "https://www.education.gov.in",
                "application_link": "https://www.education.gov.in/scholarships/merit-scholarship",
                "official_only": True,
                "category": "Merit-based",
                "state_specific": False,
                "source": self.source,
                "icon": "⭐"
            },
            {
                "name": "SC Post Matric Scholarship",
                "provider": "Ministry of Social Justice & Empowerment",
                "description": "Scholarship for Scheduled Caste students pursuing post-matriculation courses. Covers maintenance allowance, book bank, and other allowances.",
                "amount": "Full tuition + ₹550-1200 monthly allowance",
                "deadline": (now + timedelta(days=75)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "caste", "operator": "==", "value": "SC"},
                    {"field": "income", "operator": "<=", "value": 250000},
                    {"field": "marks", "operator": ">=", "value": 55}
                ],
                "source_url": "https://socialjustice.gov.in",
                "application_link": "https://socialjustice.gov.in/Scheme/SC-Scholarship",
                "official_only": True,
                "category": "Caste-based",
                "state_specific": False,
                "source": self.source,
                "icon": "📚"
            },
            {
                "name": "Maharashtra Government Scholarship for OBC Students",
                "provider": "Government of Maharashtra",
                "description": "State scholarship for Other Backward Class (OBC) students who are residents of Maharashtra pursuing higher education.",
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
                "source": self.source,
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
                "source": self.source,
                "icon": "🕌"
            },
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
                "source": self.source,
                "icon": "👧"
            },
            {
                "name": "Scholarship for Students with Disabilities",
                "provider": "Department of Empowerment of Persons with Disabilities",
                "description": "Financial assistance for students with 40% or more disability pursuing higher education from recognized institutions.",
                "amount": "Full tuition + ₹2,000 monthly allowance",
                "deadline": (now + timedelta(days=80)).strftime("%Y-%m-%d"),
                "eligibility_conditions": [
                    {"field": "marks", "operator": ">=", "value": 40}
                ],
                "source_url": "https://www.disabilityaffairs.gov.in",
                "application_link": "https://www.disabilityaffairs.gov.in/scholarship-portal",
                "official_only": True,
                "category": "Disability",
                "state_specific": False,
                "source": self.source,
                "icon": "♿"
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
                "source": self.source,
                "icon": "⚙️"
            }
        ]
        
        print(f"✅ Generated {len(mock_scholarships)} mock scholarships")
        return mock_scholarships