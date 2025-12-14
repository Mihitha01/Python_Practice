import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('vegetable_prices_dataset.csv')

print("=" * 80)
print("PRICING DATASET ANALYSIS")
print("=" * 80)

# 1. Check for duplicates
print("\n1. DUPLICATE ENTRIES (Same Date, Product, Market):")
duplicates = df[df.duplicated(subset=['Date', 'Product Name', 'Market'], keep=False)].sort_values(['Date', 'Product Name', 'Market'])
if len(duplicates) > 0:
    print(f"   Found {len(duplicates)} duplicate rows:")
    for idx, row in duplicates.iterrows():
        print(f"   {row['Date']} | {row['Product Name']:10} | {row['Market']:12} | {row['Price Today']:7.1f} | {row['Source File']}")
else:
    print("   No duplicates found")

# 2. Check for inconsistent pricing in same market on same date
print("\n2. PRICE VARIATIONS FOR SAME PRODUCT IN SAME MARKET (Multiple entries on same date):")
grouped = df.groupby(['Date', 'Product Name', 'Market'])['Price Today'].agg(['count', 'min', 'max', 'mean', 'std'])
inconsistent = grouped[grouped['count'] > 1]
if len(inconsistent) > 0:
    print(f"   Found {len(inconsistent)} products with multiple prices on same date/market:")
    for idx, row in inconsistent.iterrows():
        date, product, market = idx
        count, min_p, max_p, mean_p, std = row.values
        variance = ((max_p - min_p) / mean_p * 100) if mean_p > 0 else 0
        print(f"   {date} | {product:10} | {market:12} | Count: {int(count)}, Min: {min_p:.1f}, Max: {max_p:.1f}, Variance: {variance:.1f}%")

# 3. Check for missing markets for same product on same date
print("\n3. MARKET COVERAGE GAPS (Products with different markets on same date):")
product_market_coverage = df.groupby(['Date', 'Product Name'])['Market'].apply(lambda x: set(x)).reset_index()
for idx, row in product_market_coverage.iterrows():
    date, product, markets = row.values
    print(f"   {date} | {product:10} | Markets: {', '.join(sorted(markets))}")

# 4. Summary statistics by market
print("\n4. MARKET STATISTICS:")
market_stats = df.groupby('Market').agg({
    'Price Today': ['count', 'mean', 'min', 'max', 'std']
}).round(2)
print(market_stats)

# 5. Identify potential data quality issues
print("\n5. OUTLIERS (Prices that are unusually high or low for a product):")
for product in df['Product Name'].unique():
    product_data = df[df['Product Name'] == product]
    Q1 = product_data['Price Today'].quantile(0.25)
    Q3 = product_data['Price Today'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = product_data[(product_data['Price Today'] < lower_bound) | (product_data['Price Today'] > upper_bound)]
    if len(outliers) > 0:
        print(f"\n   {product}:")
        print(f"   Normal range: {lower_bound:.1f} - {upper_bound:.1f}")
        for idx, row in outliers.iterrows():
            print(f"      {row['Date']} | {row['Market']:12} | {row['Price Today']:7.1f} LKR")

print("\n" + "=" * 80)
