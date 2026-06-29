# Price_Comparison_Tool
A tool to compare prices across different platforms
💻 Price Comparison Tool/ This project is a production-ready data engineering pipeline designed to scrape, clean, and visualize e-commerce pricing data for "HP Pavilion" laptops. It provides an automated way to compare real-time pricing between Amazon and Flipkart using an interactive Streamlit dashboard.
🛠️ Engineering Challenges & Solutions:
During development, I focused on building a modular pipeline with intentional design choices to overcome real-world anti-bot security:
Bypassing Amazon's Anti-Bot & CAPTCHAs: I intentionally disabled "headless" mode for the Amazon scraper and implemented a manual terminal pause. This allows for human verification during CAPTCHA challenges, ensuring the script can resume extraction seamlessly.
Solving the Amazon Title Truncation Bug: Amazon often truncates product titles in the text layer. I bypassed this by targeting the product image's hidden accessibility alt attribute, which reliably contains the full, unabbreviated laptop title.
Data Integrity (Pricing & Ratings):Price Cleaning: Used custom Regular Expressions (r'[\d,]+') to isolate the true price from heavily concatenated promotional strings (e.g., "₹75,990₹99,90023% off"). 
Rating Validation: Implemented a sanity-check validator to ensure all ratings are ≤ 5.0, preventing raw review counts (like "450") from corrupting the dataset.
Clean Visualizations: To keep the Seaborn bar plots readable, I implemented a string-truncation function that dynamically caps laptop titles at 45 characters on the y-axis.  
📁 Project ArchitecturePlaintextprice_comparison_project/
├── scraper/                 
│   ├── __init__.py          
│   ├── amazon_scraper.py    # Pulls data using image alt attributes + terminal pause
│   └── flipkart_scraper.py  # Pulls data using resilient container targeting
├── data/                    # (Generated locally)
├── output/                  # (Generated locally)
├── app.py                   # Streamlit interactive dashboard script
├── run_pipeline.py          # Master orchestrator script (Extraction -> Cleaning)
└── requirements.txt         # Project dependencies
🚀 Setup and Execution Instructions
1. Environment SetupIt is recommended to use a virtual environment to manage dependencies.  Bashpip install -r requirements.txt
2. Running the Data PipelineTo trigger the end-to-end process (scraping, cleaning, and exporting data), run:
Bashpython run_pipeline.py
Note: When the Chrome window opens for Amazon, let the page load (solve the CAPTCHA if prompted), then press ENTER in your terminal to resume the extraction process.
3. Launching the Interactive UITo launch the dashboard to monitor live metrics, explore the cleaned dataset, and view the price comparison chart:
Bashstreamlit run app.py  
