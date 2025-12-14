import pandas as pd
import numpy as np

# Load cleaned dataset
df = pd.read_csv('Vegetables_fruit_prices_CLEANED.csv', encoding='latin-1', low_memory=False)

print("=" * 100)
print("GENERATING CORRECTED/NORMALIZED PRICING DATA")
print("=" * 100)

# Define Sri Lankan districts by geographic region
regions_dict = {
    'Western': ['Colombo', 'Gampaha', 'Kalutara'],
    'Central': ['Kandy', 'Matale', 'Nuwara Eliya'],
    'Southern': ['Galle', 'Matara', 'Hambantota'],
    'Northern': ['Jaffna', 'Mullaitivu', 'Vavuniya'],
    'Eastern': ['Ampara', 'Batticaloa', 'Trincomalee'],
    'North Western': ['Kurunegala', 'Puttalam'],
    'North Central': ['Polonnaruwa', 'Anuradhapura'],
    'Uva': ['Badulla', 'Monaragala'],
    'Sabaragamuwa': ['Ratnapura', 'Kegalle'],
    'Other': ['Kilinochchi', 'Mannar']
}

# Create reverse mapping
district_to_region = {}
for region, districts in regions_dict.items():
    for district in districts:
        district_to_region[district] = region

df['Geographic_Region'] = df['Region'].map(district_to_region)

print("\n1. CREATING NORMALIZED DATASET (By Geographic Region)")
print("-" * 100)

# Create normalized prices by region
df_normalized = df.copy()

# Group prices by region and commodity, then normalize
for commodity in df['vegitable_Commodity'].unique():
    for region in df['Geographic_Region'].unique():
        mask = (df_normalized['vegitable_Commodity'] == commodity) & (df_normalized['Geographic_Region'] == region)
        
        if mask.sum() > 0:
            # Calculate regional mean and std
            region_prices = df_normalized[mask]['vegitable_Price per Unit (LKR/kg)']
            region_mean = region_prices.mean()
            region_std = region_prices.std()
            
            # Replace outliers with regional mean
            outliers_mask = (np.abs(region_prices - region_mean) > 2 * region_std)
            df_normalized.loc[mask & (np.abs(df_normalized['vegitable_Price per Unit (LKR/kg)'] - region_mean) > 2 * region_std), 
                             'vegitable_Price per Unit (LKR/kg)'] = region_mean

print("✓ Applied outlier correction using 2-sigma rule")

print("\n2. SUMMARY OF NORMALIZED DATA")
print("-" * 100)

# Calculate statistics for normalized data
veg_before = df['vegitable_Price per Unit (LKR/kg)']
veg_after = df_normalized['vegitable_Price per Unit (LKR/kg)']

print(f"\nVegetable Prices:")
print(f"  BEFORE Normalization:")
print(f"    Range: {veg_before.min():.2f} - {veg_before.max():.2f} LKR")
print(f"    Mean: {veg_before.mean():.2f} LKR")
print(f"    Std Dev: {veg_before.std():.2f} LKR")
print(f"    Coefficient of Variation: {(veg_before.std()/veg_before.mean()*100):.2f}%")

print(f"\n  AFTER Normalization:")
print(f"    Range: {veg_after.min():.2f} - {veg_after.max():.2f} LKR")
print(f"    Mean: {veg_after.mean():.2f} LKR")
print(f"    Std Dev: {veg_after.std():.2f} LKR")
print(f"    Coefficient of Variation: {(veg_after.std()/veg_after.mean()*100):.2f}%")

# Same for fruits
fruit_before = df['fruit_Price per Unit (LKR/kg)']
fruit_after = df_normalized['fruit_Price per Unit (LKR/kg)']

print(f"\nFruit Prices:")
print(f"  BEFORE Normalization:")
print(f"    Range: {fruit_before.min():.2f} - {fruit_before.max():.2f} LKR")
print(f"    Mean: {fruit_before.mean():.2f} LKR")
print(f"    Std Dev: {fruit_before.std():.2f} LKR")

print(f"\n  AFTER Normalization:")
print(f"    Range: {fruit_after.min():.2f} - {fruit_after.max():.2f} LKR")
print(f"    Mean: {fruit_after.mean():.2f} LKR")
print(f"    Std Dev: {fruit_after.std():.2f} LKR")

print("\n3. REGIONAL PRICE COMPARISON (Normalized)")
print("-" * 100)

veg_by_region = df_normalized.groupby('Geographic_Region')['vegitable_Price per Unit (LKR/kg)'].agg([
    'mean', 'std', 'min', 'max'
]).round(2)
veg_by_region = veg_by_region.sort_values('mean', ascending=False)

print("\nVegetable Prices by Region (After Normalization):")
print(veg_by_region)

fruit_by_region = df_normalized.groupby('Geographic_Region')['fruit_Price per Unit (LKR/kg)'].agg([
    'mean', 'std', 'min', 'max'
]).round(2)
fruit_by_region = fruit_by_region.sort_values('mean', ascending=False)

print("\nFruit Prices by Region (After Normalization):")
print(fruit_by_region)

print("\n4. DISTRICT-LEVEL QUALITY ASSESSMENT")
print("-" * 100)

district_quality = df_normalized.groupby('Region').agg({
    'vegitable_Price per Unit (LKR/kg)': ['mean', 'std'],
    'fruit_Price per Unit (LKR/kg)': ['mean', 'std']
}).round(2)

district_quality.columns = ['Veg_Mean', 'Veg_Std', 'Fruit_Mean', 'Fruit_Std']
district_quality['Data_Points'] = df_normalized.groupby('Region').size()
district_quality['Quality_Flag'] = 'OK'  # We'll mark any problematic ones

# Mark districts with unusually high or low average prices
veg_mean_overall = df_normalized['vegitable_Price per Unit (LKR/kg)'].mean()
veg_std_overall = df_normalized['vegitable_Price per Unit (LKR/kg)'].std()

for district in district_quality.index:
    district_mean = district_quality.loc[district, 'Veg_Mean']
    if abs(district_mean - veg_mean_overall) > 1.5 * veg_std_overall:
        district_quality.loc[district, 'Quality_Flag'] = 'OUTLIER'

print("\nDistrict Quality Summary:")
print(district_quality.sort_values('Veg_Mean', ascending=False))

outlier_districts = district_quality[district_quality['Quality_Flag'] == 'OUTLIER'].index.tolist()
if outlier_districts:
    print(f"\n⚠️  Districts with unusual pricing patterns: {', '.join(outlier_districts)}")

print("\n5. SAVING NORMALIZED DATASETS")
print("-" * 100)

# Save multiple versions
df_normalized.to_csv('Vegetables_fruit_prices_NORMALIZED.csv', index=False)
print("✓ Saved: Vegetables_fruit_prices_NORMALIZED.csv")

# Create regional aggregated version (more reliable)
regional_data = []
for commodity in df['vegitable_Commodity'].unique():
    for region in df['Geographic_Region'].unique():
        mask = (df['vegitable_Commodity'] == commodity) & (df['Geographic_Region'] == region)
        if mask.sum() > 0:
            row = {
                'Commodity': commodity,
                'Type': 'Vegetable',
                'Region': region,
                'Price_LKR': df_normalized[mask]['vegitable_Price per Unit (LKR/kg)'].mean(),
                'Price_Std': df_normalized[mask]['vegitable_Price per Unit (LKR/kg)'].std(),
                'Data_Points': mask.sum()
            }
            regional_data.append(row)

for commodity in df['fruit_Commodity'].unique():
    for region in df['Geographic_Region'].unique():
        mask = (df['fruit_Commodity'] == commodity) & (df['Geographic_Region'] == region)
        if mask.sum() > 0:
            row = {
                'Commodity': commodity,
                'Type': 'Fruit',
                'Region': region,
                'Price_LKR': df_normalized[mask]['fruit_Price per Unit (LKR/kg)'].mean(),
                'Price_Std': df_normalized[mask]['fruit_Price per Unit (LKR/kg)'].std(),
                'Data_Points': mask.sum()
            }
            regional_data.append(row)

df_regional = pd.DataFrame(regional_data)
df_regional = df_regional.sort_values(['Type', 'Commodity', 'Region'])
df_regional.to_csv('Vegetables_fruit_prices_REGIONAL_AGGREGATED.csv', index=False)
print("✓ Saved: Vegetables_fruit_prices_REGIONAL_AGGREGATED.csv")
print(f"  Contains {len(df_regional)} regional price points")

print("\n6. USAGE RECOMMENDATIONS")
print("-" * 100)

recommendations = """
WHICH FILE TO USE:

1. NORMALIZED.csv (for district-level analysis)
   ✓ Outliers corrected using 2-sigma rule
   ✓ Maintains original structure
   ✓ Use for: predictive modeling, trend analysis

2. REGIONAL_AGGREGATED.csv (for more reliable results)
   ✓ Prices aggregated by geographic region
   ✓ More stable and realistic
   ✓ Use for: policy analysis, market reports, comparisons

3. Original (if needed)
   ✓ Keep for audit trail
   ⚠️  Use with caution due to data quality issues

NEXT STEPS:
  1. Verify the data source - appears synthetically generated
  2. Use REGIONAL_AGGREGATED for reports
  3. For district-level work, use NORMALIZED with data quality flags
  4. Consider collecting real market data to validate
"""

print(recommendations)
print("=" * 100)
