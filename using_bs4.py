import json
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def format_search_url(query, page):
    """Create Myntra search URL for given query and page number"""
    base_url = "https://www.myntra.com/{}/?p={}"
    formatted_query = '-'.join(query.strip().lower().split())
    return base_url.format(formatted_query, page)

# Set up browser and output folder
driver = webdriver.Chrome()
output_folder = "product_details"
os.makedirs(output_folder, exist_ok=True)

# Get user input
search_term = input("Enter product to search (e.g., shirts, shoes): ")

# Data storage lists
products = []

try:
    for page in range(1, 11):  # Scrape 10 pages
        url = format_search_url(search_term, page)
        driver.get(url)
        time.sleep(2)  # Allow page load
        
        # Scroll to load dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract product cards
        product_cards = soup.find_all('li', class_='product-base')
        
        for card in product_cards:
            product_data = {
                'brand_name': None,
                'product_name': None,
                'product_url': None
            }
            
            try:
                # Extract brand name
                brand = card.find('h3', class_='product-brand')
                if brand:
                    product_data['brand_name'] = brand.get_text(strip=True)
                
                # Extract product name
                product = card.find('h4', class_='product-product')
                if product:
                    product_data['product_name'] = product.get_text(strip=True)
                
                # Extract product URL
                link = card.find('a', href=True)
                if link:
                    product_data['product_url'] = f"https://www.myntra.com/{link['href']}"
                
                products.append(product_data)
                
            except Exception as e:
                continue

    # Save results to JSON
    output_file = os.path.join(output_folder, f'myntra_{search_term.replace(" ", "_")}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully saved {len(products)} products to {output_file}")

finally:
    driver.quit()