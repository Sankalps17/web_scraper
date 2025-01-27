from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Get user input for product search
product_query = input("Enter product to search (e.g., shirts, jeans, dresses): ").strip().lower()
sanitized_query = '-'.join(product_query.split())  # Convert spaces to hyphens
base_url = f"https://www.myntra.com/{sanitized_query}"

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(base_url)

products_data = []  # List to store product information
json_filename = f'myntra_{sanitized_query}_products.json'

try:
    # Scroll to load all products
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Allow products to load

    # Wait for product cards to load
    product_cards = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
    )

    print(f"\nScraped Product Details for '{product_query}':\n")
    for product in product_cards:
        try:
            # Extract product details
            brand = product.find_element(By.CLASS_NAME, "product-brand").text
            name = product.find_element(By.CLASS_NAME, "product-product").text
            # price = product.find_element(By.CLASS_NAME, "product-discountedPrice").text
            url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            # Print to terminal
            print(f"Brand: {brand} | Product: {name} | URL: {url}")
            
            # Add to products data list
            products_data.append({
                "brand": brand,
                "product": name,
                # "price": price,
                "url": url
            })
        except Exception as e:
            pass  # Skip any errors

    # Save data to JSON file
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(products_data, f, ensure_ascii=False, indent=4)
        
    print(f"\nData successfully saved to {json_filename}")

finally:
    driver.quit()
