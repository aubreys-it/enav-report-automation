import os
import tempfile
from scraper import download_report
from uploader import upload_to_sharepoint

def start_automation():
    # Use a temporary directory that disappears after the block ends
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"[main] Starting scraper in {temp_dir}...")
        
        try:
            # 1. Scrape the HR site
            local_file_path = download_report(temp_dir)
            
            # 2. Upload to SharePoint
            upload_to_sharepoint(local_file_path)
            
            print("[main] Automation completed successfully.")
            
        except Exception as e:
            print(f"[main] Automation failed: {e}")
            raise

if __name__ == "__main__":
    x=1/0
    start_automation()