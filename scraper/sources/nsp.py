import requests
from bs4 import BeautifulSoup

NSP_URL = "https://scholarships.gov.in"

# def fetch_nsp_scholarships():
#     response = requests.get(NSP_URL, timeout=15)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, "html.parser")

#     scholarships = []

#     for card in soup.select(".card"):
#         name = card.get_text(strip=True)

#         scholarships.append({
#             "name": name,
#             "provider": "Government of India",
#             "source_url": NSP_URL,
#             "official_only": True
#         })

#     return scholarships

def fetch_nsp_scholarships():
    response = requests.get(NSP_URL, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    print("PAGE LENGTH:", len(response.text))

    scholarships = []

    # TEMP: just test page load
    scholarships.append({
        "name": "NSP Test Scholarship",
        "provider": "Government of India",
        "source_url": NSP_URL,
        "official_only": True
    })

    return scholarships
