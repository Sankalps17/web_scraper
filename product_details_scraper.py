"""
Myntra Product Scraper
This script searches for products on Myntra.com and saves the results to a JSON file.
"""

from selenium import webdriver               # For browser automation
from selenium.webdriver.common.by import By  # For locating HTML elements
from selenium.webdriver.chrome.service import Service  # Chrome browser management
from selenium.webdriver.chrome.options import Options  # Chrome configuration
from selenium.webdriver.support.ui import WebDriverWait  # For waiting until elements load
from selenium.webdriver.support import expected_conditions as EC  # Conditions for waiting
from webdriver_manager.chrome import ChromeDriverManager  # Automatic Chrome driver setup
import time   # For adding delays
import json   # For saving data in JSON format


# Ask user what product they want to search for
product_search = input( "What product are you looking for?: " ).strip().lower()

# Format the search query for URL (replace spaces with hyphens)
formatted_query = '-'.join(product_search.split())
myntra_url = f"https://www.myntra.com/{formatted_query}"


# BROWSER SETUP
# Configure Chrome browser options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")     # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")      # Improve compatibility with some systems

# Set up Chrome browser with automatic driver management
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)


driver.get(myntra_url) # Open Myntra in the browser


# DATA COLLECTION SETUP
# List to store all product information
product_list = []
output_filename = f'myntra_{formatted_query}_products.json'

try:
 
    # PAGE INTERACTION
    
    print("\n🔄 Loading products... (This might take a moment)")
    
    # Scroll down multiple times to load all products
    for scroll_attempt in range(5):
        
        driver.execute_script("window.scrollBy(0, 1000);") # Scroll down by 1000 pixels each time
        
        time.sleep(2)  # Wait 2 seconds between scrolls for content to load

 
    # PRODUCT EXTRACTION

    print("\n🔍 Finding products on the page...")
    all_products = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
    )

    print(f"\n✅ Found {len(all_products)} products! Here's what we found:\n")

    for product_card in all_products:
        try:
            # Extract brand name
            brand = product_card.find_element(By.CLASS_NAME, "product-brand").text
            
            # Extract product name
            product_name = product_card.find_element(By.CLASS_NAME, "product-product").text
            
            # Extract product page URL
            product_url = product_card.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Show results in terminal
            print(f"• {brand}: {product_name}")
            print(f"  🔗 {product_url}\n")

            # Add to product list
            product_list.append({
                "brand": brand,
                "product_name": product_name,
                "product_url": product_url
            })

        except Exception as error:
            # Skip products that can't be read properly
            continue

    
    # SAVE RESULTS TO FILE
    # Create JSON file with product data
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(product_list, json_file, ensure_ascii=False, indent=4)

    # Final success message
    print(f"\n🎉 Success! Saved {len(product_list)} products to '{output_filename}'")
    print("💡 You can find this file in the same folder as this script!")

finally:
    # Close the browser when done
    driver.quit()
    print("\n🧹 All done! Browser closed successfully.")
