import logging
# Fix imports for running as module vs script
try:
    from backend.services.firestore import db
except ImportError:
    # Fallback for when running from scraper directory
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from backend.services.firestore import db

logger = logging.getLogger(__name__)

def clean_fake_scholarships():
    """
    Deletes scholarships that match 'fake' patterns from the database.
    Patterns: 'Application Status', 'One Time Registration', 'Dark Contrast', 'Light Contrast'
    """
    logger.info("🧹 Starting cleanup of fake/junk scholarships...")
    
    junk_keywords = [
        "application status",
        "one time registration",
        "otr",
        "dark contrast",
        "light contrast",
        "screen reader",
        "skip to main content"
    ]
    
    # We also want to remove OLD NSP scholarships (source='nsp_real')
    # Since we can't query by source efficiently without composite index,
    # and we are iterating anyway, we'll check the source if available in data.
    
    count = 0
    try:
        # We have to stream all and filter because firestore doesn't support "contains" query
        # Given the collection isn't huge (100-200), this is acceptable
        docs = db.collection("scholarships").stream()
        
        batch = db.batch()
        batch_count = 0
        
        for doc in docs:
            data = doc.to_dict()
            name = data.get("name", "").lower()
            
            # Check if name contains any junk keywords
            is_junk = any(keyword in name for keyword in junk_keywords)
            
            # Check if it was an NSP scholarship we want to remove
            source = data.get("source", "unknown")
            is_nsp = "nsp" in source.lower()
            
            if is_junk or is_nsp:
                batch.delete(doc.reference)
                batch_count += 1
                count += 1
                logger.debug(f"🗑️  Marked for deletion: {data.get('name')}")
                
            # Commit batch every 400 items (Firestore limit is 500)
            if batch_count >= 400:
                batch.commit()
                batch = db.batch()
                batch_count = 0
                
        # Commit remaining
        if batch_count > 0:
            batch.commit()
            
        logger.info(f"✅ Cleanup complete. Removed {count} junk scholarships.")
        
    except Exception as e:
        logger.error(f"❌ Error during cleanup: {e}")
