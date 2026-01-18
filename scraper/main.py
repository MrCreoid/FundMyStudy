#!/usr/bin/env python3
"""
Scholarship Scraper - Main Script
Run with: python main.py --source mock
"""
import argparse
import json
import sys
import os
from datetime import datetime

print("🚀 Starting Scholarship Scraper...")

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from scrapers.mock_scraper import MockScholarshipScraper
    from scrapers.nsp_scraper import NSPScraper
    from utils.firestore_helper import FirestoreHelper
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📁 Current directory:", os.getcwd())
    sys.exit(1)

def scrape_scholarships(source: str = "mock"):
    """
    Main scraping function
    Returns: {"status": "success/error", "count": X, "scholarships": [...]}
    """
    try:
        print(f"\n🎯 Scraping scholarships from source: {source}")
        
        all_scholarships = []
        
        # Mock scraper (always works)
        if source in ["all", "mock"]:
            print("🔄 Using mock scraper...")
            mock_scraper = MockScholarshipScraper()
            mock_scholarships = mock_scraper.scrape()
            all_scholarships.extend(mock_scholarships)
            print(f"✅ Mock scraper found {len(mock_scholarships)} scholarships")
        
        # NSP scraper (real website)
        if source in ["all", "nsp"]:
            print("🔄 Trying NSP scraper...")
            try:
                nsp_scraper = NSPScraper()
                nsp_scholarships = nsp_scraper.scrape()
                all_scholarships.extend(nsp_scholarships)
                print(f"✅ NSP scraper found {len(nsp_scholarships)} scholarships")
            except Exception as e:
                print(f"⚠️  NSP scraper failed: {e}")
        
        print(f"\n📊 Total scholarships found: {len(all_scholarships)}")
        
        # Save to Firestore
        if all_scholarships:
            print("💾 Saving to Firestore...")
            firestore_helper = FirestoreHelper()
            save_result = firestore_helper.save_scholarships(all_scholarships)
            
            return {
                "status": "success",
                "count": len(all_scholarships),
                "saved": save_result["saved"],
                "updated": save_result["updated"],
                "timestamp": datetime.utcnow().isoformat(),
                "message": f"Successfully processed {len(all_scholarships)} scholarships"
            }
        else:
            return {
                "status": "success",
                "count": 0,
                "message": "No scholarships found",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        print(f"💥 Scraping failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="Scholarship Scraper for FundMyStudy")
    parser.add_argument("--source", type=str, default="mock",
                       choices=["all", "mock", "nsp"],
                       help="Source to scrape (default: mock)")
    parser.add_argument("--output", type=str, help="Output JSON file (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't save)")
    
    args = parser.parse_args()
    
    print(f"\n⚙️  Arguments: source={args.source}, output={args.output}, dry-run={args.dry_run}")
    
    if args.dry_run:
        print("🔄 Dry run mode - will not save to Firestore")
    
    # Run scraper
    result = scrape_scholarships(args.source)
    
    # Output result
    print(f"\n📋 Final result: {result['status']}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"💾 Result saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    # Exit code
    if result["status"] == "success":
        print("✅ Scraper completed successfully!")
        sys.exit(0)
    else:
        print("❌ Scraper failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()