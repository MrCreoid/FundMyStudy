"""
Run with: python main.py --source all
"""
import argparse
import json
import sys
import os
from datetime import datetime
import logging

print("🚀 Starting FundMyStudy Scholarship Scraper...")
print("📡 Using MIXED approach: Real NSP + Mock State scholarships")
print()

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from scrapers.mock_scraper import MockScholarshipScraper
    from scrapers.buddy4study_scraper import Buddy4StudyScraper
    from utils.firestore_helper import FirestoreHelper
    from utils.cleanup import clean_fake_scholarships
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📁 Current directory:", os.getcwd())
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scrape_scholarships(source: str = "all"):
    """
    Main scraping function - MIXED APPROACH
    Returns: {"status": "success/error", "count": X, "scholarships": [...]}
    """
    try:
        logger.info(f"Starting scholarship scraping for source: {source}")
        
        # CLEANUP FIRST
        try:
            clean_fake_scholarships()
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")

        all_scholarships = []
        
        # ==================================================
        # PART 1: Buddy4Study (Real Corporate/Private Scholarships)
        # ==================================================
        if source in ["all", "buddy4study"]:
            print("\n" + "="*60)
            print("🌍 STEP 1: SCRAPING BUDDY4STUDY (Real Private Scholarships)")
            print("="*60)
            
            try:
                b4s_scraper = Buddy4StudyScraper()
                b4s_scholarships = b4s_scraper.scrape()
                
                if b4s_scholarships:
                    all_scholarships.extend(b4s_scholarships)
                    print(f"✅ Added {len(b4s_scholarships)} REAL private scholarships from Buddy4Study")
                    for i, sch in enumerate(b4s_scholarships[:2], 1):
                        print(f"   {i}. {sch['name'][:50]}...")
                else:
                    print("⚠️  No Buddy4Study scholarships found")
            except Exception as e:
                print(f"❌ Error scraping Buddy4Study: {e}")


        # ==================================================
        # PART 3: Add mock data for state scholarships
        # ==================================================
        # Only add mock if we have very raw results (backup)
        if source in ["all", "mock", "state"] and len(all_scholarships) < 5:  
            print("\n" + "="*60)
            print("🏛️  STEP 3: ADDING STATE SCHOLARSHIPS (Mock for Demo)")
            print("="*60)
            
            try:
                mock_scraper = MockScholarshipScraper()
                mock_scholarships = mock_scraper.scrape()
                
                # Filter to keep only state scholarships from mock
                state_scholarships = [s for s in mock_scholarships 
                                     if s.get("state_specific", False)]
                
                if state_scholarships:
                    all_scholarships.extend(state_scholarships)
                    print(f"✅ Added {len(state_scholarships)} STATE scholarships for demo")
                else:
                    print("⚠️  No state scholarships found in mock data")
                    
            except Exception as e:
                print(f"❌ Error getting state scholarships: {e}")
        
        # ==================================================
        # PART 4: Add central scholarships if needed
        # ==================================================
        if source in ["all", "mock", "central"] and len(all_scholarships) < 5:
            print("\n" + "="*60)
            print("⭐ STEP 4: ADDING CENTRAL GOVERNMENT SCHOLARSHIPS")
            print("="*60)
            
            try:
                if 'mock_scraper' not in locals():
                    mock_scraper = MockScholarshipScraper()
                    mock_scholarships = mock_scraper.scrape()
                
                # Filter to keep only central (non-state, non-nsp) scholarships
                central_scholarships = []
                for sch in mock_scholarships:
                    is_state = sch.get("state_specific", False)
                    is_nsp = "nsp" in sch.get("source", "").lower()
                    if not is_state and not is_nsp:
                        central_scholarships.append(sch)
                
                if central_scholarships:
                    all_scholarships.extend(central_scholarships)
                    print(f"✅ Added {len(central_scholarships)} CENTRAL government scholarships")
                else:
                    print("⚠️  No central scholarships found")
                    
            except Exception as e:
                print(f"❌ Error getting central scholarships: {e}")
        
        # ==================================================
        # FINAL STATISTICS
        # ==================================================
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)
        print(f"✅ TOTAL scholarships collected: {len(all_scholarships)}")
        
        if all_scholarships:
            # Analyze sources
            source_counts = {}
            category_counts = {}
            
            for sch in all_scholarships:
                # Count by source
                source_type = sch.get("source", "unknown")
                source_counts[source_type] = source_counts.get(source_type, 0) + 1
                
                # Count by category
                category = sch.get("category", "uncategorized")
                category_counts[category] = category_counts.get(category, 0) + 1
            
            print("\n📈 SOURCE BREAKDOWN:")
            for source_type, count in sorted(source_counts.items()):
                icon = "🌐" if "real" in source_type else "🎭"
                print(f"   {icon} {source_type}: {count} scholarships")
            
            print("\n🏷️  CATEGORY BREAKDOWN:")
            for category, count in sorted(category_counts.items()):
                print(f"   • {category}: {count}")
            
            # Save to Firestore
            print("\n💾 Saving to Firestore database...")
            try:
                firestore_helper = FirestoreHelper()
                save_result = firestore_helper.save_scholarships(all_scholarships)
                
                print(f"✅ Database save complete:")
                print(f"   • New scholarships saved: {save_result.get('saved', 0)}")
                print(f"   • Existing scholarships updated: {save_result.get('updated', 0)}")
                print(f"   • Total in database now: {save_result.get('total', 0)}")
                
                return {
                    "status": "success",
                    "message": f"Successfully processed {len(all_scholarships)} scholarships",
                    "count": len(all_scholarships),
                    "saved": save_result.get("saved", 0),
                    "updated": save_result.get("updated", 0),
                    "total_in_db": save_result.get("total", 0),
                    "sources": source_counts,
                    "categories": category_counts,
                    "timestamp": datetime.utcnow().isoformat(),
                    "scraping_approach": "mixed_real_nsp_mock_state"
                }
                
            except Exception as e:
                print(f"❌ Error saving to Firestore: {e}")
                return {
                    "status": "partial_success",
                    "message": f"Collected {len(all_scholarships)} scholarships but failed to save",
                    "count": len(all_scholarships),
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
        else:
            print("❌ No scholarships were collected")
            return {
                "status": "error",
                "message": "No scholarships found from any source",
                "count": 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR in scraping process: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="FundMyStudy Scholarship Scraper - Mixed Real & Mock Approach")
    parser.add_argument("--source", type=str, default="all",
                       choices=["all", "nsp", "state", "central", "mock"],
                       help="Source to scrape (default: all = Real NSP + Mock State)")
    parser.add_argument("--output", type=str, help="Output JSON file (optional)")
    parser.add_argument("--no-save", action="store_true", help="Don't save to Firestore (debug)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print(f"\n⚙️  Arguments:")
    print(f"   Source: {args.source}")
    print(f"   Output file: {args.output or 'None'}")
    print(f"   Save to DB: {not args.no_save}")
    print(f"   Verbose: {args.verbose}")
    print()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        print("🔍 Verbose mode enabled")
    
    # Run scraper
    print("\n" + "="*60)
    print("🚀 STARTING SCRAPING PROCESS")
    print("="*60)
    
    result = scrape_scholarships(args.source)
    
    # Output result
    print("\n" + "="*60)
    print("🏁 FINAL RESULT")
    print("="*60)
    print(f"Status: {result['status'].upper()}")
    
    if result["status"] == "success":
        print(f"✅ {result['message']}")
        print(f"📊 Total scholarships: {result['count']}")
        
        if "sources" in result:
            print("\nSources:")
            for source, count in result["sources"].items():
                print(f"  {source}: {count}")
                
    elif result["status"] == "partial_success":
        print(f"⚠️  {result['message']}")
        print(f"Error: {result.get('error', 'Unknown')}")
        
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Save to file if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Result saved to: {args.output}")
        except Exception as e:
            print(f"❌ Failed to save output file: {e}")
    
    print(f"\n⏰ Completed at: {result['timestamp']}")
    print("="*60)
    
    # Exit code
    if result["status"] in ["success", "partial_success"]:
        print("\n✅ Scraper completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Scraper failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()