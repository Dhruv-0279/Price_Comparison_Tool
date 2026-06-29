import pandas as pd
import re
import os
from scraper.flipkart_scraper import scrape_flipkart
from scraper.amazon_scraper import scrape_amazon

os.makedirs("data", exist_ok=True)

def clean_price(price_str):
    if not price_str or price_str == "N/A":
        return None
    match = re.search(r'[\d,]+', str(price_str))
    if match:
        clean_str = match.group().replace(',', '')
        try:
            return float(clean_str)
        except ValueError:
            return None
    return None

def clean_rating(rating_str):
    if not rating_str or rating_str == "N/A":
        return None
    match = re.search(r'\d+(\.\d+)?', str(rating_str))
    if match:
        rating_val = float(match.group())
        # NEW LOGIC: Sanity check. Ratings must be 5.0 or lower.
        if rating_val <= 5.0:
            return rating_val
    return None

def main():
    query = "HP Pavilion laptop"
    
    print("\n==================================")
    print(" 1. STARTING DATA EXTRACTION")
    print("==================================")
    
    flipkart_data = scrape_flipkart(query, max_items=10)
    amazon_data = scrape_amazon(query, max_items=10)
    
    all_data = flipkart_data + amazon_data
    
    if not all_data:
        print("Error: No data was scraped at all. Pipeline stopped.")
        return

    print("\n==================================")
    print(" 2. RAW DATA SAVED")
    print("==================================")
    df_raw = pd.DataFrame(all_data)
    df_raw.to_csv("data/raw_data.csv", index=False)
    print(f"Saved {len(df_raw)} raw items to data/raw_data.csv")

    print("\n==================================")
    print(" 3. STARTING DATA CLEANING & FORMATTING")
    print("==================================")
    df_clean = df_raw.copy()
    
    df_clean['Clean_Price'] = df_clean['Price'].apply(clean_price)
    df_clean['Clean_Rating'] = df_clean['Rating'].apply(clean_rating)
    
    initial_count = len(df_clean)
    df_clean.dropna(subset=['Clean_Price'], inplace=True)
    dropped_count = initial_count - len(df_clean)
    if dropped_count > 0:
        print(f"Filtered out {dropped_count} item(s) missing a valid price.")

    df_clean['Clean_Rating'] = df_clean['Clean_Rating'].round(1)
    
    df_clean['Price'] = df_clean['Clean_Price'].apply(lambda x: f"₹{int(x):,}")
    df_clean['Rating'] = df_clean['Clean_Rating'].apply(lambda x: str(x) if pd.notnull(x) else "N/A")

    df_clean.to_csv("data/clean_data.csv", index=False)
    print(f"Successfully saved {len(df_clean)} cleaned items to data/clean_data.csv")
    print("\nPIPELINE COMPLETE! Ready for the Streamlit Dashboard.")

if __name__ == "__main__":
    main()