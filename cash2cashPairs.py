import requests

# Kraken's public API endpoint for asset pairs
pairs_url = "https://api.kraken.com/0/public/AssetPairs"

# Define the fiat currencies we're interested in
fiat_currencies = {'USD', 'CHF', 'CAD', 'EUR', 'GBP', 'JPY', 'AUD'}

# Get trading pairs
response = requests.get(pairs_url)
pairs = response.json()['result']

# Create list of fiat trading pairs
fiat_pairs = []

# Process each trading pair
for pair_data in pairs.values():
    # Use wsname if available, otherwise fall back to altname
    pair_format = pair_data.get('wsname', pair_data.get('altname', ''))
    if '/' in pair_format:  # Make sure it's a valid pair
        base, quote = pair_format.split('/')
        # Only add if both base and quote are in our fiat list
        if base in fiat_currencies and quote in fiat_currencies:
            fiat_pairs.append(pair_format)

# Sort alphabetically
fiat_pairs.sort()

# Print results
print("\nFiat Currency Pairs on Kraken:")
print("------------------------------")
for pair in fiat_pairs:
    print(pair)

print(f"\nTotal number of fiat pairs: {len(fiat_pairs)}")
