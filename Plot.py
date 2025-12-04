import json
import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import os

# --- Configuration ---
JSON_FILE_NAME = "globe.json"
OUTPUT_FILE_NAME = 'price_analysis_globe.jpeg'


# --- Data Cleaning Functions ---

def clean_and_convert_to_float(value):
    """
    Cleans a string value by prioritizing fraction handling (e.g., "1/2"),
    then removing non-numeric characters for conversion to float.
    Returns None if conversion fails.
    """
    if value is None:
        return None

    s = str(value).strip()

    # Priority 1: Handle fractions (e.g., "1/2", "3/4")
    if '/' in s:
        parts = s.split('/')
        if len(parts) == 2:
            try:
                numerator = float(parts[0].strip())
                denominator = float(parts[1].strip())
                if denominator != 0:
                    return numerator / denominator
            except ValueError:
                # If conversion fails (e.g., "N/A"), fall through to next logic
                pass

    # Priority 2: Handle standard numbers (e.g., "$1,200,000", "4.5", "5")
    try:
        # Remove characters that are not digits or a decimal point
        cleaned_value = re.sub(r'[^\d.]', '', s)
        if cleaned_value:
            return float(cleaned_value)
    except ValueError:
        pass

    return None


def calculate_stats(df):
    """
    Calculates the required statistics from the DataFrame.
    """
    # Use the cleaned columns for calculation
    prices = df['price'].dropna().tolist()
    beds = df['beds'].dropna().tolist()
    baths = df['baths'].dropna().tolist()
    sq_fts = df['sq_ft'].dropna().tolist()
    # Use the original agency column (not cleaned)
    agencies = df['agency'].dropna().tolist()

    # Calculate Averages
    avg_price = sum(prices) / len(prices) if prices else 0

    # Average Beds (MODIFIED: Rounded and cast to integer as requested)
    avg_beds_float = sum(beds) / len(beds) if beds else 0
    avg_beds_int = int(round(avg_beds_float))

    # Average Baths (Remains a float to show half-bath precision as requested)
    avg_baths = sum(baths) / len(baths) if baths else 0

    # Average Sq. Ft.
    avg_sqft = sum(sq_fts) / len(sq_fts) if sq_fts else 0

    # Find Real Estate Agency with Most Listings
    most_common_agency = "N/A"
    if agencies:
        agency_counts = Counter(agencies)
        # most_common(1) returns a list of the single most common item and its count: [('Agency Name', count)]
        most_common_agency, count = agency_counts.most_common(1)[0]

    return {
        "avg_price": f"${avg_price:,.2f}",
        "avg_beds": avg_beds_int,
        "avg_baths": f"{avg_baths:.2f}",
        "avg_sqft": f"{avg_sqft:,.2f}",
        "most_common_agency": most_common_agency
    }


def generate_analysis_plot(json_file_name, output_file_name):
    """
    Main function to load data, analyze it, and generate the plot.
    """
    if not os.path.exists(json_file_name):
        print(f"Error: JSON file '{json_file_name}' not found. Please ensure it is in the current directory.")
        return

    try:
        with open(json_file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_name}'. Check if the file is valid.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    if not data:
        print(f"Error: The JSON file '{json_file_name}' is empty.")
        return

    # Convert the list of dicts to a pandas DataFrame
    df = pd.DataFrame(data)

    # 1. Data Cleaning
    print("Applying data cleaning and conversion...")
    df['price'] = df['price'].apply(clean_and_convert_to_float)
    df['beds'] = df['beds'].apply(clean_and_convert_to_float)
    df['baths'] = df['baths'].apply(clean_and_convert_to_float)
    df['sq_ft'] = df['sq_ft'].apply(clean_and_convert_to_float)

    # Filter out rows where price could not be determined for sorting/plotting
    df_plot = df.dropna(subset=['price']).copy()

    if df_plot.empty:
        print("Error: No valid price data found after cleaning. Cannot generate plot.")
        return

    # 2. Sort Data (Lowest to Highest Price)
    print("Sorting listings by price...")
    df_plot = df_plot.sort_values(by='price', ascending=True).reset_index(drop=True)

    # 3. Calculate Statistics (using the full cleaned dataset)
    stats = calculate_stats(df)
    avg_price_float = float(stats['avg_price'].replace('$', '').replace(',', ''))

    # Print the calculated stats to the console
    print("\n" + "=" * 50)
    print("Real Estate Analysis Summary:")
    print("=" * 50)
    stat_text_console = (
        f"Average Price: {stats['avg_price']}\n"
        f"Average Bedrooms: {stats['avg_beds']} (Integer)\n"
        f"Average Bathrooms: {stats['avg_baths']} (Float)\n"
        f"Average Sq. Ft.: {stats['avg_sqft']} sq ft\n"
        f"Most Common Agency: {stats['most_common_agency']}"
    )
    print(stat_text_console)
    print("=" * 50 + "\n")

    # 4. Generate the Line Graph
    print(f"Generating plot and saving to '{output_file_name}'...")
    plt.figure(figsize=(12, 7))

    # Plot the sorted prices
    plt.plot(df_plot.index, df_plot['price'], marker='o', linestyle='-',
             color='#1f77b4', linewidth=1.5, markersize=5, label='Individual Listing Price')

    # Add a line for the overall average price for context
    plt.axhline(avg_price_float, color='#d62728', linestyle='--', linewidth=2,
                label=f'Average Price ({stats["avg_price"]})')

    # Formatting the plot
    plt.title(f'Real Estate Listing Prices in {json_file_name.replace(".json", "").capitalize()}',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel(f'Listing Index (Sorted by Price from Lowest to Highest, N={len(df_plot)})', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.grid(True, which='major', linestyle=':', linewidth=0.7, alpha=0.6)

    # Adjust Y-axis format to show $ and commas for prices
    y_formatter = plt.FuncFormatter(lambda x, p: f'${x:,.0f}')
    plt.gca().yaxis.set_major_formatter(y_formatter)

    # Add Legend
    plt.legend(loc='upper left', fontsize=10)

    # 5. Add Statistics Output to the JPEG (Text Box)
    stat_text_plot = (
        f"--- Summary Statistics ---\n"
        f"Avg. Price: {stats['avg_price']}\n"
        f"Avg. Beds: {stats['avg_beds']}\n"
        f"Avg. Baths: {stats['avg_baths']}\n"
        f"Avg. Sq. Ft.: {stats['avg_sqft']} sq ft\n"
        f"Top Agency: {stats['most_common_agency']}"
    )

    # Position the text box in the upper right corner of the plot
    plt.text(0.98, 0.98, stat_text_plot,
             transform=plt.gca().transAxes,
             fontsize=10,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle="round,pad=0.6", fc="white", alpha=0.9, ec="gray", linewidth=0.5),
             fontfamily='monospace')

    # Ensure layout is tight to prevent truncation
    plt.tight_layout()

    # 6. Save as JPEG
    plt.savefig(output_file_name, format='jpeg', dpi=300)
    print(f"Success! Plot and analysis exported to '{output_file_name}'")


# Execute the script
if __name__ == "__main__":
    generate_analysis_plot(JSON_FILE_NAME, OUTPUT_FILE_NAME)