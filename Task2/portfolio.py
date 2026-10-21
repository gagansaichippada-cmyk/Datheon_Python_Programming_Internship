"""
Stock Portfolio Performance Tracker
Task 2 - Datheon Python Programming Internship

Uses manually entered current prices (or sample prices) and saves a CSV summary.
No live market-price API is used.
"""

import csv
from pathlib import Path

DATASET_FILE = Path("constituents.txt")
OUTPUT_FILE = Path("portfolio_summary.csv")

# Clearly labeled sample prices for demonstration only, not live market prices.
SAMPLE_CURRENT_PRICES = {
    "AAPL": 190.00,
    "MSFT": 420.00,
    "NVDA": 120.00,
    "GOOGL": 175.00,
    "AMZN": 185.00,
}


def load_ticker_symbols(filename=DATASET_FILE):
    """Load ticker symbols from the supplied S&P 500 CSV dataset."""
    symbols = set()
    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = (row.get("Symbol") or "").strip().upper()
                if symbol:
                    symbols.add(symbol)
    except FileNotFoundError:
        print(f"Note: {filename} was not found. Ticker validation will be skipped.")
    except (OSError, csv.Error) as error:
        print(f"Note: Could not read {filename}: {error}")
    return symbols


def ask_positive_number(prompt):
    """Ask until the user enters a number greater than zero."""
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            value = float(raw)
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, such as 25 or 12.50.")


def ask_ticker(valid_symbols):
    while True:
        ticker = input("Stock ticker symbol (or DONE to finish): ").strip().upper()
        if ticker == "DONE":
            return None
        if not ticker:
            print("Ticker cannot be blank.")
            continue
        if valid_symbols and ticker not in valid_symbols:
            print("That symbol was not found in constituents.txt. Try another symbol.")
            continue
        return ticker


def collect_holding(valid_symbols):
    ticker = ask_ticker(valid_symbols)
    if ticker is None:
        return None

    purchase_price = ask_positive_number("Purchase price per share: ")
    quantity = ask_positive_number("Number of shares: ")

    sample_price = SAMPLE_CURRENT_PRICES.get(ticker)
    if sample_price is not None:
        print(f"Sample current price for {ticker}: ${sample_price:.2f} (demo only).")
        use_sample = input("Use this sample price? (y/n): ").strip().lower()
        if use_sample in ("y", "yes"):
            current_price = sample_price
        else:
            current_price = ask_positive_number("Enter current price per share: ")
    else:
        current_price = ask_positive_number("Enter current price per share: ")

    invested = purchase_price * quantity
    market_value = current_price * quantity
    gain_loss = market_value - invested
    gain_loss_pct = (gain_loss / invested) * 100 if invested else 0.0

    return {
        "symbol": ticker,
        "purchase_price": purchase_price,
        "quantity": quantity,
        "current_price": current_price,
        "invested_value": invested,
        "current_market_value": market_value,
        "gain_loss": gain_loss,
        "gain_loss_percent": gain_loss_pct,
    }


def save_summary(holdings, filename=OUTPUT_FILE):
    fieldnames = [
        "symbol", "purchase_price", "quantity", "current_price",
        "invested_value", "current_market_value", "gain_loss",
        "gain_loss_percent",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for holding in holdings:
            writer.writerow({
                "symbol": holding["symbol"],
                "purchase_price": f'{holding["purchase_price"]:.2f}',
                "quantity": f'{holding["quantity"]:g}',
                "current_price": f'{holding["current_price"]:.2f}',
                "invested_value": f'{holding["invested_value"]:.2f}',
                "current_market_value": f'{holding["current_market_value"]:.2f}',
                "gain_loss": f'{holding["gain_loss"]:.2f}',
                "gain_loss_percent": f'{holding["gain_loss_percent"]:.2f}',
            })


def main():
    print("=" * 54)
    print("       STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 54)
    print("Enter your holdings. Type DONE when you have finished.")
    print("Prices are manually entered or clearly labeled demo prices.")
    valid_symbols = load_ticker_symbols()
    holdings = []

    while True:
        holding = collect_holding(valid_symbols)
        if holding is None:
            break
        holdings.append(holding)
        print(f"Added {holding['symbol']}.")

    if not holdings:
        print("No holdings entered. No summary was created.")
        return

    total_invested = sum(item["invested_value"] for item in holdings)
    total_market_value = sum(item["current_market_value"] for item in holdings)
    total_gain_loss = total_market_value - total_invested
    total_gain_loss_pct = (total_gain_loss / total_invested) * 100 if total_invested else 0.0

    print("\nPORTFOLIO SUMMARY")
    print("-" * 76)
    print(f'{"Ticker":<10} {"Invested":>12} {"Market Value":>14} {"Gain/Loss":>14} {"Gain/Loss %":>12}')
    print("-" * 76)
    for item in holdings:
        print(
            f'{item["symbol"]:<10} '
            f'${item["invested_value"]:>11,.2f} '
            f'${item["current_market_value"]:>13,.2f} '
            f'${item["gain_loss"]:>13,.2f} '
            f'{item["gain_loss_percent"]:>11.2f}%'
        )
    print("-" * 76)
    print(f"Total invested:       ${total_invested:,.2f}")
    print(f"Current market value: ${total_market_value:,.2f}")
    print(f"Total gain/loss:      ${total_gain_loss:,.2f} ({total_gain_loss_pct:.2f}%)")

    try:
        save_summary(holdings)
        print(f"\nCSV summary saved to: {OUTPUT_FILE.resolve()}")
    except OSError as error:
        print(f"\nCould not save the CSV summary: {error}")


if __name__ == "__main__":
    main()
