import os
os.environ['WDM_SSL_VERIFY'] = '0'

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_amazon(query="HP Pavilion laptop", max_items=10):
    print(f"Starting Amazon scrape for: {query}...")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    formatted_query = query.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={formatted_query}"
    
    driver.get(url)
    
    print("\n" + "="*40)
    print(" 🛑 ACTION REQUIRED IN CHROME BROWSER")
    print("="*40)
    print("1. Look at the Chrome window that just opened.")
    print("2. If Amazon asks for a CAPTCHA, solve it.")
    print("3. Wait until you visually see the list of laptops.")
    input("\n👉 Once you see the laptops, click here in the terminal and press ENTER to continue... ")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    scraped_data = []
    
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    if not product_containers:
        product_containers = soup.find_all('div', class_=lambda c: c and 's-result-item' in c)
    
    for container in product_containers:
        if len(scraped_data) >= max_items:
            break

        # NEW LOGIC: Use the product image's hidden accessibility text for the perfect title
        try:
            img_tag = container.find('img', class_='s-image')
            if img_tag and img_tag.get('alt'):
                name = img_tag.get('alt').strip()
            else:
                h2_tag = container.find('h2')
                name = h2_tag.text.strip() if h2_tag else None
        except Exception:
            name = None

        try:
            price_element = container.find('span', class_='a-price-whole')
            price = price_element.text.strip() if price_element else None
        except Exception:
            price = None

        try:
            rating_element = container.find('span', class_='a-icon-alt')
            rating = rating_element.text.strip() if rating_element else None
        except Exception:
            rating = None

        if name and price:
            scraped_data.append({
                'Source': 'Amazon',
                'Name': name,
                'Price': price,
                'Rating': rating or "N/A"
            })

    print(f"\nSuccessfully scraped {len(scraped_data)} items from Amazon.")
    return scraped_data

if __name__ == "__main__":
    test_data = scrape_amazon()
    for item in test_data:
        print(item)