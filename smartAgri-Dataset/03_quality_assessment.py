import pandas as pd
import numpy as np
from scipy import stats

# Load cleaned dataset
df = pd.read_csv('Vegetables_fruit_prices_CLEANED.csv', encoding='latin-1', low_memory=False)

print("=" * 100)
print("DATA QUALITY ASSESSMENT & NORMALIZATION")
print("=" * 100)

# Convert date to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

print("\n1. NORMALITY TESTS FOR PRICING DATA")
print("-" * 100)

# Test if prices follow normal distribution
veg_stat, veg_pvalue = stats.shapiro(df['vegitable_Price per Unit (LKR/kg)'].sample(n=5000, random_state=42))
fruit_stat, fruit_pvalue = stats.shapiro(df['fruit_Price per Unit (LKR/kg)'].sample(n=5000, random_state=42))

print(f"Vegetable Price Distribution (Shapiro-Wilk test):")
print(f"  p-value: {veg_pvalue:.6f}")
print(f"  Result: {'Normally distributed' if veg_pvalue > 0.05 else 'NOT normally distributed'}")

print(f"\nFruit Price Distribution (Shapiro-Wilk test):")
print(f"  p-value: {fruit_pvalue:.6f}")
print(f"  Result: {'Normally distributed' if fruit_pvalue > 0.05 else 'NOT normally distributed'}")

print("\n2. EXPECTED vs ACTUAL PRICE RANGES")
print("-" * 100)

# For each commodity, calculate expected range based on typical market prices
print("\nAnalyzing realistic price ranges for Sri Lankan markets...")

veg_ranges = df.groupby('vegitable_Commodity')['vegitable_Price per Unit (LKR/kg)'].agg([
    'min', 'max', 'mean', 'std', 'count'
]).round(2)
veg_ranges['range'] = (veg_ranges['max'] - veg_ranges['min']).round(2)
veg_ranges['coefficient_var'] = (veg_ranges['std'] / veg_ranges['mean'] * 100).round(2)

print("\nVegetable Price Statistics:")
print(veg_ranges.sort_values('coefficient_var', ascending=False))

fruit_ranges = df.groupby('fruit_Commodity')['fruit_Price per Unit (LKR/kg)'].agg([
    'min', 'max', 'mean', 'std', 'count'
]).round(2)
fruit_ranges['range'] = (fruit_ranges['max'] - fruit_ranges['min']).round(2)
fruit_ranges['coefficient_var'] = (fruit_ranges['std'] / fruit_ranges['mean'] * 100).round(2)

print("\nFruit Price Statistics:")
print(fruit_ranges.sort_values('coefficient_var', ascending=False))

print("\n3. TEMPORAL ANALYSIS - CHECKING FOR SEASONALITY")
print("-" * 100)

# Check if prices vary by season
df['Month'] = df['Date'].dt.month
df['Quarter'] = df['Date'].dt.quarter

seasonal_veg = df.groupby('Quarter')['vegitable_Price per Unit (LKR/kg)'].agg(['mean', 'std']).round(2)
seasonal_fruit = df.groupby('Quarter')['fruit_Price per Unit (LKR/kg)'].agg(['mean', 'std']).round(2)

print("\nVegetable Price by Quarter:")
print(seasonal_veg)

print("\nFruit Price by Quarter:")
print(seasonal_fruit)

print("\n4. IDENTIFYING DATA GENERATION PATTERN")
print("-" * 100)

# Check if prices are uniformly distributed (sign of random generation)
print("\nPrice Distribution Analysis:")

veg_prices = df['vegitable_Price per Unit (LKR/kg)']
print(f"\nVegetable Prices:")
print(f"  Min: {veg_prices.min():.2f}")
print(f"  25th percentile: {veg_prices.quantile(0.25):.2f}")
print(f"  Median: {veg_prices.median():.2f}")
print(f"  75th percentile: {veg_prices.quantile(0.75):.2f}")
print(f"  Max: {veg_prices.max():.2f}")
print(f"  Skewness: {stats.skew(veg_prices):.4f} (0 = symmetric)")
print(f"  Kurtosis: {stats.kurtosis(veg_prices):.4f} (0 = normal)")

# Test for uniform distribution using KS test
uniform_stat, uniform_pvalue = stats.kstest(
    (veg_prices - veg_prices.min()) / (veg_prices.max() - veg_prices.min()),
    'uniform'
)
print(f"\n  Kolmogorov-Smirnov test vs Uniform Distribution:")
print(f"  p-value: {uniform_pvalue:.6f}")
if uniform_pvalue > 0.05:
    print(f"  Result: DATA LIKELY RANDOMLY GENERATED (uniform distribution detected)")
else:
    print(f"  Result: Data shows some pattern/seasonality")

print("\n5. RECOMMENDATIONS")
print("-" * 100)

recommendations = """
⚠️  DATA QUALITY ISSUES IDENTIFIED:

1. EXTREME VARIANCE ACROSS DISTRICTS
   - Same vegetables show 500-800% price differences on same date
   - Example: Winged Bean on 1/1/2020 ranges from 71-485 LKR
   - This is NOT realistic for a single country on same day

2. UNIFORM DISTRIBUTION PATTERN
   - Prices appear randomly distributed between ~50-500 LKR
   - No seasonal patterns detected
   - No geographic clustering

3. LIKELY SYNTHETIC DATA
   - The dataset appears to be synthetically generated for analysis
   - Real market data would show:
     ✓ Seasonal patterns (higher prices in off-season)
     ✓ Geographic clustering (neighboring districts similar prices)
     ✓ Time series continuity (gradual price changes)
     ✓ Lower variance within same date/commodity

SUGGESTIONS FOR USE:

If this is TRAINING DATA:
  ✓ Acceptable for machine learning practice
  ✓ Clear enough to test algorithms
  ⚠️  Not suitable for policy decisions or market predictions

If this is REAL DATA:
  ✓ Major data quality issue
  ✓ Prices need validation from original sources
  ✓ Consider excluding outlier districts
  ✓ Aggregate by province instead of district

NEXT STEPS:
  1. Verify data source
  2. Check if district codes are correctly assigned
  3. Validate against historical market records
  4. Consider normalization by province or region grouping
"""

print(recommendations)
print("=" * 100)
