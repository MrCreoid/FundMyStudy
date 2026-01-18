import subprocess
import json
import os
from datetime import datetime
import sys

class ScraperService:
    def __init__(self):
        # Get the scraper folder path (one level up from backend)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(current_dir)
        self.scraper_path = os.path.join(backend_dir, "../scraper")
        print(f"📁 Scraper path: {self.scraper_path}")

    def run_scraper(self, source: str = "mock"):
        """
        Run the scraper as a subprocess
        Returns: {"status": "success/error", "data": ...}
        """
        try:
            print(f"🚀 Starting scraper for source: {source}")
            
            # Check if scraper folder exists
            if not os.path.exists(self.scraper_path):
                return {
                    "status": "error",
                    "error": f"Scraper folder not found at: {self.scraper_path}",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Path to the scraper main.py
            scraper_main = os.path.join(self.scraper_path, "main.py")
            
            if not os.path.exists(scraper_main):
                return {
                    "status": "error",
                    "error": f"Scraper main.py not found at: {scraper_main}",
                    "timestamp": datetime.utcnow().isoformat()
                }

            print(f"📄 Running: python {scraper_main} --source {source}")
            
            # Run the scraper
            result = subprocess.run(
                [sys.executable, scraper_main, "--source", source],
                capture_output=True,
                text=True,
                cwd=self.scraper_path,
                timeout=120  # 2 minute timeout
            )
            
            print(f"📤 Scraper stdout: {result.stdout[:200]}...")
            if result.stderr:
                print(f"📤 Scraper stderr: {result.stderr[:200]}...")

            if result.returncode == 0:
                try:
                    # Try to parse JSON output
                    output = json.loads(result.stdout)
                    return {
                        "status": "success",
                        "data": output,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                except json.JSONDecodeError:
                    # Return raw output
                    return {
                        "status": "success",
                        "data": {"output": result.stdout},
                        "timestamp": datetime.utcnow().isoformat()
                    }
            else:
                return {
                    "status": "error",
                    "error": result.stderr or "Unknown error",
                    "stdout": result.stdout,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Scraper timed out after 2 minutes",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_scraping_status(self):
        """Get status of scraping"""
        return {
            "status": "ready",
            "service": "scraper_service",
            "scraper_path": self.scraper_path,
            "timestamp": datetime.utcnow().isoformat()
        }

# Create singleton
scraper_service = ScraperService()