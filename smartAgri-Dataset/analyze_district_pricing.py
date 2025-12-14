import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('Vegetables_fruit_prices_with_climate_130000_2020_to_2025.csv', encoding='latin-1')

print("=" * 100)
print("DISTRICT PRICING ANALYSIS - VEGETABLES & FRUITS (2020-2025)")
print("=" * 100)

print(f"\nDataset shape: {df.shape}")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Number of districts: {df['Region'].nunique()}")
print(f"Districts: {sorted(df['Region'].unique())}")

# 1. Check for data quality issues
print("\n" + "=" * 100)
print("1. DATA QUALITY ISSUES")
print("=" * 100)

# Check for missing values
print("\nMissing values:")
missing = df.isnull().sum()
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("None found")

# Check for invalid values (like 's' in Crop Yield Impact Score)
print("\nInvalid values in Crop Yield Impact Score:")
try:
    invalid_yield = df[pd.to_numeric(df['Crop Yield Impact Score'], errors='coerce').isna()]
    if len(invalid_yield) > 0:
        print(f"Found {len(invalid_yield)} invalid values")
        print(invalid_yield[['Date', 'Region', 'Crop Yield Impact Score']].head(10))
except:
    pass

# 2. Analyze vegetable prices by district
print("\n" + "=" * 100)
print("2. VEGETABLE PRICING ANALYSIS BY DISTRICT")
print("=" * 100)

veg_df = df[['Date', 'Region', 'vegitable_Commodity', 'vegitable_Price per Unit (LKR/kg)']].copy()
veg_df = veg_df.dropna()

print("\nUnique vegetables:", sorted(veg_df['vegitable_Commodity'].unique()))

# Get price ranges for each vegetable by district
print("\nPrice ranges for vegetables by district (Min - Max - Mean):")
veg_stats = veg_df.groupby(['vegitable_Commodity', 'Region'])['vegitable_Price per Unit (LKR/kg)'].agg(['min', 'max', 'mean', 'count']).round(2)
print(veg_stats)

# 3. Check for inconsistencies
print("\n" + "=" * 100)
print("3. PRICING ANOMALIES")
print("=" * 100)

# Find extreme price variations for the same vegetable across districts on same date
print("\nPrice variation for same vegetable across districts (same date):")
for date in sorted(veg_df['Date'].unique())[:5]:  # Check first 5 dates
    date_data = veg_df[veg_df['Date'] == date]
    for commodity in date_data['vegitable_Commodity'].unique():
        commodity_data = date_data[date_data['vegitable_Commodity'] == commodity]
        if len(commodity_data) > 1:
            price_range = commodity_data['vegitable_Price per Unit (LKR/kg)']
            if price_range.max() / price_range.min() > 2:  # More than 2x variation
                print(f"\n{date} - {commodity}:")
                print(f"  Variation: {price_range.min():.2f} LKR to {price_range.max():.2f} LKR ({(price_range.max()/price_range.min() - 1)*100:.1f}% difference)")
                for idx, row in commodity_data.iterrows():
                    print(f"    {row['Region']:15} | {row['vegitable_Price per Unit (LKR/kg)']:7.2f} LKR")

# 4. Fruit pricing analysis
print("\n" + "=" * 100)
print("4. FRUIT PRICING ANALYSIS BY DISTRICT")
print("=" * 100)

fruit_df = df[['Date', 'Region', 'fruit_Commodity', 'fruit_Price per Unit (LKR/kg)']].copy()
fruit_df = fruit_df.dropna()

print("\nUnique fruits:", sorted(fruit_df['fruit_Commodity'].unique()))

fruit_stats = fruit_df.groupby(['fruit_Commodity', 'Region'])['fruit_Price per Unit (LKR/kg)'].agg(['min', 'max', 'mean', 'count']).round(2)
print("\nPrice ranges for fruits by district (Min - Max - Mean):")
print(fruit_stats.head(15))

# 5. Summary of districts with consistently high/low prices
print("\n" + "=" * 100)
print("5. DISTRICT PRICING TRENDS")
print("=" * 100)

veg_by_region = veg_df.groupby('Region')['vegitable_Price per Unit (LKR/kg)'].agg(['mean', 'std', 'min', 'max']).round(2)
veg_by_region = veg_by_region.sort_values('mean', ascending=False)
print("\nVegetable prices - Average by district (sorted highest to lowest):")
print(veg_by_region)

print("\n" + "=" * 100)
