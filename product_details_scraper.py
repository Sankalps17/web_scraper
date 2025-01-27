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

# Create folder for storing results
output_folder = "product_details"
os.makedirs(output_folder, exist_ok=True)

# User input
product_query = input("Search product (e.g., shirts, jeans): ").strip().lower()
search_param = '-'.join(product_query.split())
base_url = f"https://www.myntra.com/{search_param}"

# Browser setup
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

products = []
total_pages = 7  # Number of pages to scrape

try:
    for page in range(1, total_pages + 1):
        # Navigate to current page
        page_url = f"{base_url}?p={page}"
        driver.get(page_url)
        
        print(f"\nProcessing page {page}/{total_pages}...")

        # Scroll logic explanation: 
        # Myntra uses lazy loading - scrolling triggers loading of more products
        # We scroll multiple times to ensure all products load
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)  # Allow time for new products to load

        # Product extraction
        product_cards = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
        )

        for card in product_cards:
            try:
                brand = card.find_element(By.CLASS_NAME, "product-brand").text
                name = card.find_element(By.CLASS_NAME, "product-product").text
                url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                products.append({
                    "brand": brand,
                    "name": name,
                    "url": url
                })
                
            except Exception:
                continue

        print(f"Page {page} completed - Total products: {len(products)}")

    # Save results
    output_file = os.path.join(output_folder, f'myntra_{search_param}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(products)} products to {output_file}")

finally:
    driver.quit()
    print("\nBrowser closed")