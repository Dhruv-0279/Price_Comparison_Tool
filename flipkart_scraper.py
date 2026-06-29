import os
# Bypass SSL Certificate verification for webdriver download
os.environ['WDM_SSL_VERIFY'] = '0'

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_flipkart(query="HP Pavilion laptop", max_items=10):
    """
    Scrapes product Name, Price, and Rating from Flipkart using Selenium and BeautifulSoup.
    Caps at max_items to respect usage policies.
    """
    print(f"Starting Flipkart scrape for: {query}...")
    
    # 1. Setup Headless Chrome (Mimics a real browser but runs in the background)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening a visible window
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Automatically manage the ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 2. Format the URL and Load the Page
    formatted_query = query.replace(" ", "%20")
    url = f"https://www.flipkart.com/search?q={formatted_query}"
    
    driver.get(url)
    
    # Wait for dynamic content to load
    time.sleep(3) 
    
    # 3. Pass the fully loaded HTML to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit() # Close the browser immediately to save memory

    # 4. Extract Data with Robust Error Handling
    scraped_data = []
    
    # Find all main div blocks that look like product containers
    # Using 'data-id' is a highly reliable way to catch all product cards on Flipkart
    product_containers = soup.find_all('div', {'data-id': True}) 
    
    for container in product_containers:
        # Stop if we hit our maximum limit (Project Guideline: Scrape top 10)
        if len(scraped_data) >= max_items:
            break

        # ROBUST ERROR HANDLING: Extracting Name
        try:
            name_element = container.find('div', class_='RG5Slk') 
            name = name_element.text.strip() if name_element else None
        except Exception:
            name = None

        # ROBUST ERROR HANDLING: Extracting Price
        try:
            price_element = container.find('div', class_='mao5dl') 
            price = price_element.text.strip() if price_element else None
        except Exception:
            price = None

        # ROBUST ERROR HANDLING: Extracting Rating
        try:
            rating_element = container.find('div', class_='a7saXW')
            rating = rating_element.text.strip() if rating_element else None
        except Exception:
            rating = None

        # Only append if we at least found a name and a price
        if name and price:
            scraped_data.append({
                'Source': 'Flipkart',
                'Name': name,
                'Price': price,
                'Rating': rating or "N/A"
            })

    print(f"Successfully scraped {len(scraped_data)} items from Flipkart.")
    return scraped_data

# Quick test to ensure it works when run directly
if __name__ == "__main__":
    test_data = scrape_flipkart()
    for item in test_data:
        print(item)