"""
File: parameter_computer.py
Author: Martin Lemaire
Date created: November 7, 2023
Description: Computes the specific program's parameters according to the selected symbol in its current state.

Modifications:
- [v1.0.0 - 07.11.23 - INITIAL]
"""

# IMPORTS
import csv, ccxt, os
import numpy as np
import pandas as pd

# MAIN
if __name__ == "__main__":

    CSV_path = "data.csv"

    # Reading
    try:
        with open(CSV_path, mode='r') as file:
            reader = csv.reader(file)
            row = next(reader)
            data_csv = [value for value in row]
    except FileNotFoundError:
        print("The file does not exist. Please check the file path or create the file.")
    except PermissionError:
        print("Permission denied to open the file. Make sure you have the necessary permissions.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        # This block executes if no exceptions occur
        pass

    symbol = data_csv[14]
    exchange = ccxt.binance()
    input_file = "initial_data.csv"

    # Writing
    try:
        with open(input_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Open", "High", "Low", "Close"])  # Write header row
            ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=1000)
            for i in range(len(ohlcv)): writer.writerow([ohlcv[i][1], ohlcv[i][2], ohlcv[i][3], ohlcv[i][4]])
    except FileNotFoundError:
        print("The file does not exist. Please check the file path or create the file.")
    except PermissionError:
        print("Permission denied to open the file. Make sure you have the necessary permissions.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        # This block executes if no exceptions occur
        pass

    # Load the CSV file with 4 columns
    output_file = 'returns.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Create a new list to store the calculated values
    new_column_values = []

    # Iterate through the DataFrame rows
    for index, row in df.iterrows(): new_column_values.extend([abs(row.iloc[3]/row.iloc[0]-1)*100])

    # Create a new DataFrame with the calculated values as a single column
    new_df = pd.DataFrame({'New_Column': new_column_values})

    # Save the new DataFrame to a CSV file
    new_df.to_csv(output_file, index=False)

    # Load the CSV file with 4 columns
    input_file = output_file

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Create a new list to store the calculated values
    new_column_values = []
    sum = 0
    count = 0

    # Iterate through the DataFrame rows
    for index, row in df.iterrows(): new_column_values.append(row.iloc[0])

    claw_dist = int(100*(np.mean(new_column_values)))/100

    if claw_dist < 2: min_claw_dist = 2
    else: min_claw_dist = claw_dist

    max_claw_dist = int(min_claw_dist*1.75)/100
    min_claw_dist = int(min_claw_dist)/100

    data_csv[12] = min_claw_dist
    data_csv[13] = max_claw_dist

    # Writing
    try:
        with open(CSV_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_csv)
    except FileNotFoundError:
        print("The file does not exist. Please check the file path or create the file.")
    except PermissionError:
        print("Permission denied to open the file. Make sure you have the necessary permissions.")
    except IOError as e:
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        # This block executes if no exceptions occur
        pass

    os.remove("initial_data.csv")
    os.remove("returns.csv")
