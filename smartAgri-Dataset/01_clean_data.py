import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
df = pd.read_csv('Vegetables_fruit_prices_with_climate_130000_2020_to_2025.csv', encoding='latin-1', low_memory=False)

print("=" * 100)
print("DATA CLEANING & VALIDATION REPORT")
print("=" * 100)

# 1. Fix invalid Crop Yield Impact Score values
print("\n1. FIXING INVALID VALUES")
print("-" * 100)

invalid_mask = pd.to_numeric(df['Crop Yield Impact Score'], errors='coerce').isna()
invalid_count = invalid_mask.sum()

if invalid_count > 0:
    print(f"Found {invalid_count} invalid values in 'Crop Yield Impact Score':")
    invalid_rows = df[invalid_mask][['Date', 'Region', 'Crop Yield Impact Score']].copy()
    print(invalid_rows)
    
    # Replace with mean value grouped by region
    for idx in df[invalid_mask].index:
        region = df.loc[idx, 'Region']
        mean_score = pd.to_numeric(df[df['Region'] == region]['Crop Yield Impact Score'], errors='coerce').mean()
        df.loc[idx, 'Crop Yield Impact Score'] = mean_score
        print(f"  Fixed: {region} -> {mean_score:.2f}")
else:
    print("No invalid values found")

# Convert to numeric
df['Crop Yield Impact Score'] = pd.to_numeric(df['Crop Yield Impact Score'], errors='coerce')

# 2. Handle missing values in price columns
print("\n2. CHECKING FOR MISSING PRICE VALUES")
print("-" * 100)

missing_veg = df['vegitable_Price per Unit (LKR/kg)'].isna().sum()
missing_fruit = df['fruit_Price per Unit (LKR/kg)'].isna().sum()

print(f"Missing vegetable prices: {missing_veg}")
print(f"Missing fruit prices: {missing_fruit}")

# 3. Remove outliers using IQR method
print("\n3. DETECTING OUTLIERS")
print("-" * 100)

def detect_outliers_by_commodity(df, commodity_col, price_col):
    """Detect outliers using IQR method per commodity"""
    outliers = []
    for commodity in df[commodity_col].unique():
        commodity_data = df[df[commodity_col] == commodity][price_col]
        Q1 = commodity_data.quantile(0.25)
        Q3 = commodity_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        commodity_outliers = df[(df[commodity_col] == commodity) & 
                                ((df[price_col] < lower_bound) | (df[price_col] > upper_bound))]
        outliers.append(commodity_outliers)
    
    return pd.concat(outliers, ignore_index=True) if outliers else pd.DataFrame()

veg_outliers = detect_outliers_by_commodity(df, 'vegitable_Commodity', 'vegitable_Price per Unit (LKR/kg)')
fruit_outliers = detect_outliers_by_commodity(df, 'fruit_Commodity', 'fruit_Price per Unit (LKR/kg)')

print(f"Vegetable outliers detected: {len(veg_outliers)}")
print(f"Fruit outliers detected: {len(fruit_outliers)}")

# 4. Analyze price variance by commodity and district
print("\n4. PRICE STABILITY ANALYSIS (Coefficient of Variation)")
print("-" * 100)

# For vegetables
veg_cv = df.groupby(['vegitable_Commodity', 'Region']).agg({
    'vegitable_Price per Unit (LKR/kg)': ['mean', 'std', 'count']
}).round(2)
veg_cv.columns = ['Mean', 'Std', 'Count']
veg_cv['CV'] = (veg_cv['Std'] / veg_cv['Mean'] * 100).round(2)
veg_cv_sorted = veg_cv.sort_values('CV', ascending=False).head(20)

print("Top 20 Vegetable commodity-district pairs with highest price variance (CV%):")
print(veg_cv_sorted[['Mean', 'Std', 'CV', 'Count']])

# 5. Create cleaned dataset
print("\n5. SAVING CLEANED DATASET")
print("-" * 100)

df_clean = df.copy()
output_file = 'Vegetables_fruit_prices_CLEANED.csv'
df_clean.to_csv(output_file, index=False)
print(f"✓ Saved cleaned dataset to: {output_file}")

# 6. Summary statistics
print("\n6. SUMMARY STATISTICS - CLEANED DATA")
print("-" * 100)

print(f"\nVegetable Price Range: {df_clean['vegitable_Price per Unit (LKR/kg)'].min():.2f} - {df_clean['vegitable_Price per Unit (LKR/kg)'].max():.2f} LKR")
print(f"Vegetable Price Mean: {df_clean['vegitable_Price per Unit (LKR/kg)'].mean():.2f} LKR")
print(f"Vegetable Price Std: {df_clean['vegitable_Price per Unit (LKR/kg)'].std():.2f} LKR")

print(f"\nFruit Price Range: {df_clean['fruit_Price per Unit (LKR/kg)'].min():.2f} - {df_clean['fruit_Price per Unit (LKR/kg)'].max():.2f} LKR")
print(f"Fruit Price Mean: {df_clean['fruit_Price per Unit (LKR/kg)'].mean():.2f} LKR")
print(f"Fruit Price Std: {df_clean['fruit_Price per Unit (LKR/kg)'].std():.2f} LKR")

print("\n" + "=" * 100)
