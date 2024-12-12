import requests
import csv

# Kraken's public API endpoint for assets
assets_url = "https://api.kraken.com/0/public/Assets"

# Get assets
response = requests.get(assets_url)
assets = response.json()['result']

# Create list of tickers
tickers = []
for asset in assets:
    # Some assets have 'X' or 'Z' prefix, remove those
    clean_ticker = assets[asset].get('altname', asset)
    tickers.append(clean_ticker)

# Sort alphabetically
tickers.sort()

# Export to CSV
with open('kraken_tickers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Ticker'])  # Header
    for ticker in tickers:
        writer.writerow([ticker])

print(f"Exported {len(tickers)} tickers to kraken_tickers.csv")
print("\nFirst few tickers:")
for ticker in tickers[:10]:  # Show first 10 tickers as preview
    print(ticker)
