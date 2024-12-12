import requests
import csv

# Kraken's public API endpoint for asset pairs and assets
pairs_url = "https://api.kraken.com/0/public/AssetPairs"
assets_url = "https://api.kraken.com/0/public/Assets"

# Get trading pairs and assets
pairs_response = requests.get(pairs_url)
assets_response = requests.get(assets_url)

pairs = pairs_response.json()['result']
assets = assets_response.json()['result']

# Let's print some example data to see what we're working with
print("Example of assets data:")
for asset_key in list(assets.keys())[:5]:
    print(f"{asset_key}: {assets[asset_key]}")

print("\nExample of pairs data:")
for pair_key in list(pairs.keys())[:5]:
    print(f"{pair_key}: {pairs[pair_key]}")

# Create sets to store unique base and quote currencies with their info
base_currencies = {}
quote_currencies = set()

# Process each trading pair
for pair_name, pair_data in pairs.items():
    pair_format = pair_data.get('wsname', pair_data.get('altname', ''))
    
    if '/' in pair_format:
        base, quote = pair_format.split('/')
        base_ticker = pair_data.get('base')
        
        print(f"\nProcessing pair: {pair_format}")
        print(f"Base ticker: {base_ticker}")
        if base_ticker in assets:
            print(f"Asset info for {base_ticker}: {assets[base_ticker]}")
        
        # Store base currency with its ticker and name
        if base not in base_currencies and base_ticker in assets:
            full_name = assets[base_ticker].get('name', '')
            print(f"Full name found: {full_name}")
            base_currencies[base] = {'name': full_name if full_name else base, 'ticker': base}

        quote_currencies.add(quote)

# Convert to sorted lists
quote_currencies = sorted(list(quote_currencies))
base_items = sorted(base_currencies.items(), key=lambda x: x[1]['name'])

# Create CSV file
with open('kraken_pairs_matrix.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header row
    header = ['Currency Name', 'Ticker'] + quote_currencies
    writer.writerow(header)
    
    # Write each base currency row
    for base_ticker, base_info in base_items:
        row = [base_info['name'], base_info['ticker']] + [''] * len(quote_currencies)
        writer.writerow(row)
        print(f"Writing row: {row}")  # Debug print

print("CSV debug file has been created!")
