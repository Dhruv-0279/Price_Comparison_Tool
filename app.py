import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Laptop Price Comparison", page_icon="💻", layout="wide")

# --- ERROR HANDLING & DATA LOADING ---
@st.cache_data
def load_data():
    file_path = "data/clean_data.csv"
    if not os.path.exists(file_path):
        return None
    return pd.read_csv(file_path)

# --- HEADER & MONITORING ---
st.title("💻 HP Pavilion Price Comparison Dashboard")
st.markdown("This dashboard compares real-time scraped prices between Amazon and Flipkart.")

df = load_data()

if df is None or df.empty:
    st.error("⚠️ No clean data found! Please run `python run_pipeline.py` in your terminal first.")
    st.stop()

# Monitoring Metrics
st.subheader("📊 Scraping Monitor & Metrics")
col1, col2, col3 = st.columns(3)

flipkart_count = len(df[df['Source'] == 'Flipkart'])
amazon_count = len(df[df['Source'] == 'Amazon'])
avg_price = df['Clean_Price'].mean()

col1.metric("Total Items Scraped", len(df))
col2.metric("Flipkart vs Amazon", f"{flipkart_count} / {amazon_count}")
col3.metric("Average Price", f"₹ {avg_price:,.2f}")

st.divider()

# --- VISUALIZATION ---
st.subheader("📉 Price Comparison Visualization")
st.markdown("Comparing the top 10 cheapest laptops found across both platforms.")

df_sorted = df.sort_values(by="Clean_Price", ascending=True).head(10).copy()

# Shorten long product names so the Y-axis looks clean
df_sorted['Short_Name'] = df_sorted['Name'].apply(lambda x: (str(x)[:45] + '...') if len(str(x)) > 45 else str(x))

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=df_sorted, 
    y="Short_Name", 
    x="Clean_Price", 
    hue="Source", 
    palette={"Amazon": "#FF9900", "Flipkart": "#2874F0"}, 
    ax=ax,
    dodge=False
)

ax.set_title("Top 10 Cheapest 'HP Pavilion' Models", fontsize=14, pad=15)
ax.set_xlabel("Price (₹)", fontsize=12)
ax.set_ylabel("Product Name", fontsize=12)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.tight_layout()

st.pyplot(fig)

# Save chart for project deliverables
os.makedirs("output", exist_ok=True)
fig.savefig("output/price_comparison_chart.png", bbox_inches='tight')

st.divider()

# --- DATA TABLES ---
st.subheader("📁 Processed Dataset")
st.markdown("Explore the cleaned data below.")

st.dataframe(
    df[['Source', 'Name', 'Clean_Price', 'Clean_Rating', 'Price', 'Rating']], 
    use_container_width=True,
    hide_index=True
)

st.success("✅ Output chart successfully saved to `output/price_comparison_chart.png` for final submission.")