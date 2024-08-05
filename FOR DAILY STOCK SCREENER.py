import yfinance as yf
import pandas as pd
from datetime import datetime

def calculate_fibonacci_pivots(high, low, close):
    pivot = (high + low + close) / 3
    range_ = high - low
    s1 = pivot - (range_ * 0.382)
    s2 = pivot - (range_ * 0.618)
    s3 = pivot - (range_ * 1.000)
    r1 = pivot + (range_ * 0.382)
    r2 = pivot + (range_ * 0.618)
    r3 = pivot + (range_ * 1.000)
    return s1, s2, s3, r1, r2, r3

def check_stocks_touching_s3(stock_list, year):
    previous_year = year - 1
    start_date = datetime(previous_year, 1, 1)
    end_date = datetime(year, 1, 1)

    stocks_touching_s3 = []
    stocks_with_no_data = []

    for stock in stock_list:
        try:
            # Fetch historical data for the previous year
            data = yf.download(stock, start=start_date, end=end_date, progress=False)

            if data.empty:
                stocks_with_no_data.append(stock)
                continue

            yearly_high = data['High'].max()
            yearly_low = data['Low'].min()
            yearly_close = data['Close'][-1]

            # Calculate S3 level using previous year's data
            s1, s2, s3, r1, r2, r3 = calculate_fibonacci_pivots(yearly_high, yearly_low, yearly_close)

            # Fetch data for the current year to check if S3 level was touched
            current_year_start_date = datetime(year, 1, 1)
            current_year_end_date = datetime(year + 1, 1, 1)
            latest_data = yf.download(stock, start=current_year_start_date, end=current_year_end_date, progress=False)

            if latest_data.empty:
                stocks_with_no_data.append(stock)
                continue

            # Check if the stock touches S3 level in the current year
            touched_s3 = latest_data['Low'].min() <= s3

            if touched_s3:
                stocks_touching_s3.append(stock)

        except Exception as e:
            print(f"Error processing {stock}: {e}")
            stocks_with_no_data.append(stock)

    return stocks_touching_s3, stocks_with_no_data

def get_in_stock_list():
    return [
        # Add your stock list here
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS" # Example stocks
        # More stocks...
    ]

def main():
    year = int(input("Enter the year to check stocks (e.g., 2023): "))
    stock_list = get_in_stock_list()
    stocks_touching_s3, stocks_with_no_data = check_stocks_touching_s3(stock_list, year)

    print(f"Stocks touching S3 level in {year}:")
    print(stocks_touching_s3)

    if stocks_with_no_data:
        print(f"Stocks with no data for {year - 1} or {year}:")
        print(stocks_with_no_data)

if __name__ == "__main__":
    main()
