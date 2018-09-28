""" CSC 161 Project: Milestone 2

Sahaj Somani
Lab Section MW 3:25-4:40
Spring 2018
"""

import csv
current_stocks = 0
current_cash = 1000

def test_data(filename, col, day):
    row = get_day(filename, day)
    z = get_col(col)
    x = (row[z])  # so it uses the correct colomn
    return float(x)

def get_data(filename, col, day):  # function to extract data from file
    row = get_day(filename, day)
    z = get_col(col)
    x = (row[z])  # so it uses the correct colomn
    return float(x)

def get_sp500(col, day):  # another method just like
    # get_data to get info from the another file concerning the price movements
    # of the S&P 500
    row = get_day_sp500(day)
    z = get_col_sp500(col)
    x = (row[z])
    return float(x)

def read_file(filename):  # function to bring in and read the file
    f = open(filename, "r")
    # csv_f = csv.reader(f)
    row_data = f.readlines()
    return row_data

def get_day(filename, day):  # function to get the correct row
    file = read_file(filename)
    right_day = file[4049 - day]
    row = right_day.split(',')
    return row

def get_day_sp500(day):
    file = read_file("SP500.csv")
    right_day = file[day]
    row = right_day.split(',')
    return row

def get_col(col):  # function to get the correct column
    col = col.lower()  # converting into lower case to avoid case problems
    z = 0
    if col == "open":
        z = 1
    elif col == "high":
        z = 2
    elif col == "low":
        z = 3
    elif col == "close":
        z = 4
    elif col == "volume":
        z = 5
    elif col == "adj_close":
        z = 6
    return z

def get_col_sp500(col):
    col = col.lower()
    z = 0
    if col == "open":
        z = 1 
    elif col == "close":
        z = 4
    return z


def alg_moving_average(filename):

    global current_stocks
    global current_cash
    price_type = "close"
    for i in range(21,4049):  # Loop for going through all days in the file
        # the loop starts at the 21st day because you at least need 20 days of
        # previous data to calculate moving average
        sum_initial = 0
        for j in range(i-20, i):  # loop for calculating average of last 20 days
            sum_initial += float(get_data(filename, price_type, j))
        avg = sum_initial/20

        current_price = (get_data(filename, price_type, i))
        buying_ratio = 1 - 0.05  # if stock is 5% below average (for buying)
        selling_ratio = 1 + 0.03  # if stock is 3% above average (for selling)

        if current_price < avg*buying_ratio:  # buying the stock
            current_stocks += 1  
            current_cash -= current_price
            
        if current_price > avg*selling_ratio:  # selling the stock
            current_stocks -= 1
            current_cash += current_price
            
    # selling all stocks in the end
    final_closing_price = (get_data(filename, price_type, 4048))
    current_cash = current_cash + current_stocks*final_closing_price
    current_stocks = 0
    total_cash = current_cash  # total_cash is a temporary variable to hold the
    # cash balance after trading using moving average
    current_cash = 1000  # current cash has been changed back to initial
    # amount of $1000 for the next algorithm 

    return current_stocks, total_cash

def alg_mine(filename):  # Compares the price of the stock to the S&P 500.
    # Decisions are made based on the magnitude of varience
    global current_stocks
    global current_cash

    for i in range(1, 4049):
        stock_open = get_data(filename, "open", i)  # opening price of the stock
        stock_close = get_data(filename, "close", i)  # closing price of the stock
        stock_diff = stock_open - stock_close
        stock_diff_percentage = (stock_diff/stock_open)  # percentage
        # change in stock price

        sp_open = get_sp500("open", i)  # opening price of S&P 500
        sp_close = get_sp500("close", i)  # closing price of S&P 500
        sp_diff = sp_open - sp_close
        sp_diff_percentage = (sp_diff/sp_open)  # percentage change
        # in the S&P 500

        if stock_diff_percentage < sp_diff_percentage:  # buying decision cycle
            if stock_diff_percentage < (sp_diff_percentage - 0.03):
                # buy only one stock if difference is greater than 3%
                current_stocks += 1
                current_cash -= stock_close
            elif stock_diff_percentage < (sp_diff_percentage - 0.065):
                # buy two stocks if the difference is greater than 6.5%
                current_stocks += 2
                current_cash -= (stock_close*2)
            elif stock_diff_percentage < (sp_diff_percentage - 0.1):
                # buy three stocks if the difference is greater than 10%
                current_stocks += 3
                current_cash -= (stock_close*3)
        elif stock_diff_percentage > sp_diff_percentage:  # selling decision cycle
            if stock_diff_percentage > (sp_diff_percentage - 0.03):
                # sell only one stock if difference is greater than 3%
                current_stocks -= 1
                current_cash += stock_close
            elif stock_diff_percentage > (sp_diff_percentage - 0.065):
                # sell two stocks if the difference is greater than 6.5%
                current_stocks -= 2
                current_cash += (stock_close * 2)
            elif stock_diff_percentage > (sp_diff_percentage - 0.1):
                # sell three stocks if the difference is greater than 10%
                current_stocks -= 3
                current_cash += (stock_close * 3)

    final_closing_price = (get_data(filename, "close", 4048))
    current_cash = current_cash + current_stocks*final_closing_price
    # selling all stocks in the end
    current_stocks = 0

    return current_stocks, current_cash

def main():
    filename = input("Enter a filename for stock data (CSV format): ")
    alg1_stocks, alg1_balance = alg_moving_average(filename)
    print("Your final cash balance using moving average is", alg1_balance)
    alg2_stocks, alg2_balance = alg_mine(filename)
    print("Your final cash balance using matching algorithm is", alg2_balance)

main()

