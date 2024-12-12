import requests

# Kraken's public API endpoint for asset pairs
pairs_url = "https://api.kraken.com/0/public/AssetPairs"

# Define the quote currencies we want to exclude
excluded_quotes = {'USD', 'GBP', 'EUR', 'CAD', 'JPY', 'CHF', 'AUD'}

# Get trading pairs
response = requests.get(pairs_url)
pairs = response.json()['result']

# Create list of trading pairs
trading_pairs = []

# Process each trading pair
for pair_data in pairs.values():
    # Use wsname if available, otherwise fall back to altname
    pair_format = pair_data.get('wsname', pair_data.get('altname', ''))
    if '/' in pair_format:  # Make sure it's a valid pair
        base, quote = pair_format.split('/')
        if quote not in excluded_quotes:  # Only add if quote currency is not in excluded list
            trading_pairs.append(pair_format)

# Sort alphabetically
trading_pairs.sort()

# Print results
print("\nTrading Pairs on Kraken (excluding pairs with USD, GBP, EUR, JPY, CHF, AUD):")
print("----------------------------------------------------------------------------")
for pair in trading_pairs:
    print(pair)

print(f"\nTotal number of pairs: {len(trading_pairs)}")

