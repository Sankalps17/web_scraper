# Import tools needed for web scraping and data handling
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

# Create a dedicated folder to store all product results
output_folder = "product_details"
os.makedirs(output_folder, exist_ok=True)  # Auto-create folder if missing

# Get user's desired product search
product_query = input("Search product (e.g., shirts, jeans): ").strip().lower()
# Convert search term to Myntra URL format (spaces -> hyphens)
search_param = '-'.join(product_query.split())
base_url = f"https://www.myntra.com/{search_param}"

# Configure Chrome browser settings
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Better for server/remote operation
chrome_options.add_argument("--no-sandbox")   # Improves stability on some systems

# Start automated Chrome browser
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

products = []  # Master list to store all found products
total_pages = 7  # Number of product pages to check

try:
    # Process each product results page
    for page in range(1, total_pages + 1):
        # Build page URL (Myntra uses ?p= for page numbers)
        page_url = f"{base_url}?p={page}"
        driver.get(page_url)  # Load the page
        
        print(f"\nProcessing page {page}/{total_pages}...")

        # Scroll down 3 times to load all hidden products
        # (Myntra loads more items as you scroll)
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)  # Wait for new items to appear

        # Find all product cards on the page
        product_cards = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
        )

        # Extract details from each product card
        for card in product_cards:
            try:
                # Get product brand name
                brand = card.find_element(By.CLASS_NAME, "product-brand").text
                # Get product title/name
                name = card.find_element(By.CLASS_NAME, "product-product").text
                # Get link to product page
                url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                # Save product details to master list
                products.append({
                    "brand": brand,
                    "name": name,
                    "url": url
                })
                
            except Exception:
                continue  # Skip products that can't be read properly

        print(f"Page {page} completed - Total products: {len(products)}")

    # Save all collected data to JSON file
    output_file = os.path.join(output_folder, f'myntra_{search_param}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(products)} products to {output_file}")

finally:
    # Always close browser when done (even if errors occur)
    driver.quit()
    print("\nBrowser closed")