import pandas as pd
import numpy as np
from scipy import stats

# Load cleaned dataset
df = pd.read_csv('Vegetables_fruit_prices_CLEANED.csv', encoding='latin-1', low_memory=False)

print("=" * 100)
print("GEOGRAPHIC PATTERN ANALYSIS")
print("=" * 100)

# Define districts by geographic region
regions_dict = {
    'Western Province': ['Colombo', 'Gampaha', 'Kalutara'],
    'Central Province': ['Kandy', 'Matale', 'Nuwara Eliya'],
    'Southern Province': ['Galle', 'Matara', 'Hambantota'],
    'Northern Province': ['Jaffna', 'Mullaitivu', 'Vavuniya'],
    'Eastern Province': ['Ampara', 'Batticaloa', 'Trincomalee'],
    'North Western Province': ['Kurunegala', 'Puttalam'],
    'North Central Province': ['Polonnaruwa', 'Anuradhapura'],
    'Uva Province': ['Badulla', 'Monaragala'],
    'Sabaragamuwa Province': ['Ratnapura', 'Kegalle'],
    'Other': ['Kilinochchi', 'Mannar']
}

# Create reverse mapping
district_to_province = {}
for province, districts in regions_dict.items():
    for district in districts:
        district_to_province[district] = province

df['Province'] = df['Region'].map(district_to_province)

print("\n1. PRICE ANALYSIS BY PROVINCE")
print("-" * 100)

# Vegetable prices by province
veg_by_province = df.groupby('Province')['vegitable_Price per Unit (LKR/kg)'].agg(['mean', 'std', 'min', 'max', 'count']).round(2)
veg_by_province = veg_by_province.sort_values('mean', ascending=False)
print("\nVegetable Prices by Province:")
print(veg_by_province)

# Fruit prices by province
fruit_by_province = df.groupby('Province')['fruit_Price per Unit (LKR/kg)'].agg(['mean', 'std', 'min', 'max', 'count']).round(2)
fruit_by_province = fruit_by_province.sort_values('mean', ascending=False)
print("\nFruit Prices by Province:")
print(fruit_by_province)

print("\n2. PRICE VARIANCE ANALYSIS BY PROVINCE")
print("-" * 100)

# Coefficient of Variation by province
veg_cv_by_province = (veg_by_province['std'] / veg_by_province['mean'] * 100).round(2)
fruit_cv_by_province = (fruit_by_province['std'] / fruit_by_province['mean'] * 100).round(2)

print("\nVegetable Price Coefficient of Variation by Province (%):")
print(veg_cv_by_province.sort_values(ascending=False))

print("\nFruit Price Coefficient of Variation by Province (%):")
print(fruit_cv_by_province.sort_values(ascending=False))

print("\n3. CLIMATE IMPACT ANALYSIS")
print("-" * 100)

# Analyze correlation between climate and prices
climate_cols = ['Temperature (°C)', 'Rainfall (mm)', 'Humidity (%)']

# Try to fix the degree symbol
try:
    if 'Temperature (°C)' not in df.columns:
        temp_col = [col for col in df.columns if 'Temperature' in col][0]
        df['Temperature (°C)'] = df[temp_col]
except:
    pass

print("\nTemperature vs Vegetable Price Correlation:")
if 'Temperature (°C)' in df.columns:
    temp_veg_corr = df[['Temperature (°C)', 'vegitable_Price per Unit (LKR/kg)']].corr().iloc[0, 1]
    print(f"  Correlation: {temp_veg_corr:.4f}")
    temp_fruit_corr = df[['Temperature (°C)', 'fruit_Price per Unit (LKR/kg)']].corr().iloc[0, 1]
    print(f"  Fruit Correlation: {temp_fruit_corr:.4f}")

print("\nRainfall vs Vegetable Price Correlation:")
if 'Rainfall (mm)' in df.columns:
    rain_veg_corr = df[['Rainfall (mm)', 'vegitable_Price per Unit (LKR/kg)']].corr().iloc[0, 1]
    print(f"  Correlation: {rain_veg_corr:.4f}")
    rain_fruit_corr = df[['Rainfall (mm)', 'fruit_Price per Unit (LKR/kg)']].corr().iloc[0, 1]
    print(f"  Fruit Correlation: {rain_fruit_corr:.4f}")

print("\nHumidity vs Vegetable Price Correlation:")
if 'Humidity (%)' in df.columns:
    humid_veg_corr = df[['Humidity (%)', 'vegitable_Price per Unit (LKR/kg)']].corr().iloc[0, 1]
    print(f"  Correlation: {humid_veg_corr:.4f}")
    humid_fruit_corr = df[['Humidity (%)', 'fruit_Price per Unit (LKR/kg)']].corr().iloc[0, 1]
    print(f"  Fruit Correlation: {humid_fruit_corr:.4f}")

print("\n4. CONSISTENCY SCORES BY DISTRICT")
print("-" * 100)

# Create consistency score (inverse of CV)
district_stats = df.groupby('Region').agg({
    'vegitable_Price per Unit (LKR/kg)': ['mean', 'std'],
    'fruit_Price per Unit (LKR/kg)': ['mean', 'std']
}).round(2)

district_stats.columns = ['Veg_Mean', 'Veg_Std', 'Fruit_Mean', 'Fruit_Std']
district_stats['Veg_CV'] = (district_stats['Veg_Std'] / district_stats['Veg_Mean'] * 100).round(2)
district_stats['Fruit_CV'] = (district_stats['Fruit_Std'] / district_stats['Fruit_Mean'] * 100).round(2)
district_stats['Consistency_Score'] = (100 - (district_stats['Veg_CV'] + district_stats['Fruit_CV']) / 2).round(2)
district_stats = district_stats.sort_values('Consistency_Score', ascending=False)

print("\nDistrict Consistency Scores (Higher = More Reliable):")
print(district_stats[['Veg_CV', 'Fruit_CV', 'Consistency_Score']])

print("\n5. SUSPICIOUS DISTRICTS (High Price Variance)")
print("-" * 100)

suspicious = district_stats[district_stats['Consistency_Score'] < 50].sort_values('Consistency_Score')
print(f"\nDistricts with Consistency Score < 50 (Potentially Unreliable Data):")
print(suspicious[['Veg_CV', 'Fruit_CV', 'Consistency_Score']])

if len(suspicious) == 0:
    print("All districts appear to have high variance - data quality issue!")
    print("\nNote: The extremely high price variance across all districts suggests")
    print("the prices may be randomly generated rather than based on real data.")

print("\n" + "=" * 100)
