import requests

# Kraken's public API endpoint for asset pairs
pairs_url = "https://api.kraken.com/0/public/AssetPairs"

# Define the quote currencies we want
wanted_quotes = {'EUR', 'GBP', 'CAD', 'AUD', 'CHF', 'JPY'}

# Get trading pairs
response = requests.get(pairs_url)
pairs = response.json()['result']

# Create list of formatted pairs
trading_pairs = []
for pair_data in pairs.values():
    # Use wsname if available, otherwise fall back to altname
    pair_format = pair_data.get('wsname', pair_data.get('altname', ''))
    if '/' in pair_format:  # Make sure it's a valid pair
        base, quote = pair_format.split('/')
        if quote in wanted_quotes:  # Only add if quote currency is in our wanted list
            trading_pairs.append(pair_format)

# Sort alphabetically
trading_pairs.sort()

# Print all pairs
print("Trading Pairs on Kraken:")
print("------------------------")
for pair in trading_pairs:
    print(pair)

# Optionally, save to a file
with open('kraken_pairs_list.txt', 'w') as f:
    for pair in trading_pairs:
        f.write(f"{pair}\n")

print(f"\nTotal number of pairs: {len(trading_pairs)}")
print("List has been saved to 'kraken_pairs_list.txt'")
