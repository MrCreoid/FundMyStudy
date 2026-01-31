import requests
from bs4 import BeautifulSoup
import json

url = "https://www.buddy4study.com/scholarships"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Check for Next.js data
    next_data = soup.select_one("#__NEXT_DATA__")
    
    # Search for any JSON blob containing "scholarship"
    import re
    scripts = soup.find_all("script")
    found_json = False
    
    for script in scripts:
        if script.string and "Listing_scholarshipName" in script.string:
            print("Found script processing styles/classes.")
            
        if script.string and '"scholarshipName"' in script.string:
            print("✅ Found JSON with 'scholarshipName' in a script tag!")
            print(f"Script preview: {script.string[:200]}...")
            found_json = True
            
    if not found_json:
        print("❌ Could not find scholarship data in any script tag.")
        
    titles = soup.select("h4[class^='Listing_scholarshipName']")
    print(f"Direct HTML check found {len(titles)} titles.")
    
except Exception as e:
    print(f"Error: {e}")
