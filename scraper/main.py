#!/usr/bin/env python3
"""
Scholarship Scraper - Main Script
"""
import argparse
import json
import sys
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.nsp_scraper import NSPScraper
from scrapers.aicte_scraper import AICTEScraper
from utils.firestore_helper import FirestoreHelper

def scrape_scholarships(source: str = "all"):
    """
    Main scraping function
    Returns: {"status": "success/error", "count": X, "scholarships": [...]}
    """
    try:
        logger.info(f"Starting scholarship scraping for source: {source}")
        
        all_scholarships = []
        scrapers = []
        
        # Initialize scrapers based on source
        if source in ["all", "nsp"]:
            scrapers.append(NSPScraper())
        
        if source in ["all", "aicte"]:
            scrapers.append(AICTEScraper())
        
        # Run all scrapers
        for scraper in scrapers:
            try:
                logger.info(f"Running {scraper.source_name} scraper...")
                scholarships = scraper.scrape()
                all_scholarships.extend(scholarships)
                logger.info(f"{scraper.source_name} found {len(scholarships)} scholarships")
            except Exception as e:
                logger.error(f"{scraper.source_name} scraper failed: {e}")
        
        logger.info(f"Total scholarships found: {len(all_scholarships)}")
        
        # Save to Firestore
        if all_scholarships:
            logger.info("Saving to Firestore...")
            firestore_helper = FirestoreHelper()
            save_result = firestore_helper.save_scholarships(all_scholarships)
            
            return {
                "status": "success",
                "count": len(all_scholarships),
                "saved": save_result["saved"],
                "updated": save_result["updated"],
                "timestamp": datetime.utcnow().isoformat(),
                "sources": [s.source_name for s in scrapers]
            }
        else:
            return {
                "status": "success",
                "count": 0,
                "message": "No scholarships found",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="Scholarship Scraper for FundMyStudy")
    parser.add_argument("--source", type=str, default="all",
                       choices=["all", "nsp", "aicte", "state"],
                       help="Source to scrape (default: all)")
    parser.add_argument("--output", type=str, help="Output JSON file (optional)")
    
    args = parser.parse_args()
    
    # Run scraper
    result = scrape_scholarships(args.source)
    
    # Output result
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Result saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    # Exit code
    sys.exit(0 if result["status"] == "success" else 1)

if __name__ == "__main__":
    main()