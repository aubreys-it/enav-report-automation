import os
from playwright.sync_api import Playwright, sync_playwright

def download_report(download_dir: str) -> str:
    hr_url      = os.environ["HR_SITE_URL"]
    hr_username = os.environ["HR_USERNAME"]
    hr_password = os.environ["HR_PASSWORD"]

    # Initialize this so it's accessible outside the 'run' scope
    final_path = ""

    def run(playwright: Playwright) -> None:
        nonlocal final_path
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(hr_url)
        page.get_by_role("textbox", name="Username").fill(hr_username)
        page.get_by_role("textbox", name="Password").fill(hr_password)
        page.get_by_role("button", name="Login").click()
        
        page.get_by_role("link", name="SAGE Import").click()
        page.get_by_role("link", name="View").click()
        
        with page.expect_download() as download_info:
            page.get_by_role("button", name=" Download").click()
        
        download = download_info.value
        final_path = os.path.join(download_dir, download.suggested_filename)
        
        # KEY CHANGE: Save it while the browser is still open
        download.save_as(final_path)

        # Optional: Clean logout
        page.get_by_role("button", name="GRANT HOUSER ").click()
        page.get_by_role("link", name="Logout").click()

        context.close()
        browser.close()

    with sync_playwright() as playwright:
        run(playwright)

    print(f"[scraper] Downloaded: {final_path}")
    return final_path

if __name__ == "__main__":
    import tempfile
    # Create a dummy temp dir for the Docker test
    with tempfile.TemporaryDirectory() as tmp:
        print(f"Starting download to {tmp}...")
        download_report(tmp)
        print("Done.")
    
