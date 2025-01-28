# Import core functionality
from selenium import webdriver                # Browser automation
from selenium.webdriver.common.by import By   # HTML element location strategies
from selenium.webdriver.chrome.service import Service  # Chrome service management
from selenium.webdriver.chrome.options import Options  # Browser customization
from selenium.webdriver.support.ui import WebDriverWait  # Smart waiting
from selenium.webdriver.support import expected_conditions as EC  # Wait conditions
from webdriver_manager.chrome import ChromeDriverManager  # Automatic driver handling
import time     # Timing operations
import json     # JSON data handling
import os       # File system operations

# OUTPUT CONFIGURATION
output_folder = "product_details"  # Central location for all results
os.makedirs(output_folder, exist_ok=True)  # Auto-create folder if missing

# USER CONFIGURATION

product_query = input("Search product (e.g., shirts, jeans): ").strip().lower() # Get user search input and format for URL
search_param = '-'.join(product_query.split())  # Convert "blue shirts" to "blue-shirts"
base_url = f"https://www.myntra.com/{search_param}"  # Base search URL


# BROWSER CONFIGURATION

chrome_options = Options() # Set up Chrome options for headless/remote operation
#chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for stability
#chrome_options.add_argument("--no-sandbox")   # Bypass OS security model for Docker/CI

# Initialize browser instance
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options ) # Auto-download driver


# DATA STORAGE
products = []       # Master list for product objects
total_pages = 7     # Number of pagination pages to scrape

try:
    
    # PAGINATION HANDLING
    for page in range(1, total_pages + 1):    # Build page-specific URL
        
        page_url = f"{base_url}?p={page}"
        driver.get(page_url)  # Navigate to target page
        
        print(f"\n📃 Processing page {page}/{total_pages}...")
        
        
        # Simulate user scrolling to trigger lazy-loading
        for _ in range(3):  # Triple scroll to load all items
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)  # Allow content to load between scrolls

        # PRODUCT CARD PROCESSING
        # Wait for product cards to become available
        product_cards = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
        )

        # Extract data from each product card
        for card in product_cards:
            try:
                # Structured data extraction
                brand = card.find_element(By.CLASS_NAME, "product-brand").text
                name = card.find_element(By.CLASS_NAME, "product-product").text
                url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                products.append({
                    "brand": brand,
                    "name": name,
                    "url": url
                })
                
            except Exception:
                continue  # Skip malformed cards

        print(f"Page {page} completed - Total: {len(products)} products")
   
    # DATA EXPORT
    output_file = os.path.join(output_folder, f'myntra_{search_param}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)  # Human-readable format

    print(f"\n Saved {len(products)} products to {output_file}")

finally:
    
    # RESOURCE CLEANUP-
    driver.quit()  # Ensure browser closure even on errors
    print("\n Browser session terminated")