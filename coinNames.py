import requests
import csv

# Kraken's public API endpoints
pairs_url = "https://api.kraken.com/0/public/AssetPairs"
assets_url = "https://api.kraken.com/0/public/Assets"
ticker_info_url = "https://api.kraken.com/0/public/Ticker"

# Get trading pairs and assets
pairs_response = requests.get(pairs_url)
assets_response = requests.get(assets_url)

pairs = pairs_response.json()['result']
assets = assets_response.json()['result']

# Create sets to store unique base and quote currencies with their info
base_currencies = {}
quote_currencies = set()

# Process each trading pair
for pair_name, pair_data in pairs.items():
    pair_format = pair_data.get('wsname', pair_data.get('altname', ''))
    
    if '/' in pair_format:
        base, quote = pair_format.split('/')
        base_ticker = pair_data.get('base')
        
        # Store base currency with its ticker
        if base not in base_currencies:
            # Try to get the proper name from the assets data
            if base_ticker in assets:
                # Some assets have an 'X' or 'Z' prefix in their base ticker
                clean_base_ticker = base_ticker[1:] if base_ticker.startswith(('X', 'Z')) else base_ticker
                base_currencies[base] = {
                    'name': assets[base_ticker].get('altname', base),
                    'ticker': base
                }

        quote_currencies.add(quote)

# Let's try to get additional info from CoinGecko's API for better names
try:
    coingecko_url = "https://api.coingecko.com/api/v3/coins/list"
    coingecko_response = requests.get(coingecko_url)
    coingecko_data = coingecko_response.json()
    
    # Create a mapping of symbols to names
    symbol_to_name = {coin['symbol'].upper(): coin['name'] for coin in coingecko_data}
    
    # Update our base_currencies with better names where available
    for base_ticker in base_currencies:
        if base_ticker in symbol_to_name:
            base_currencies[base_ticker]['name'] = symbol_to_name[base_ticker]
except:
    print("Couldn't fetch CoinGecko data, continuing with original names...")

# Convert to sorted lists
quote_currencies = sorted(list(quote_currencies))
# Sort base_currencies by name
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

print("CSV file has been created!")
saved