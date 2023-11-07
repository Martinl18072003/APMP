"""
File: log_data_to_history.py
Author: Martin Lemaire
Date created: November 7, 2023
Description: Adds the current data of the program to "data_history.csv".

Modifications:
- [v1.0.0 - 07.11.23 - INITIAL]
"""

# IMPORTS
import csv
import datetime

# MAIN
if __name__ == "__main__":

    # Reading
    try:
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            data = next(reader)
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

    # Fetching date and time to add to the history
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_with_datetime = [current_datetime] + data

    # Writing
    try:
        with open('data_history.csv', 'a', newline='') as history_file:
            writer = csv.writer(history_file)
            writer.writerow(data_with_datetime)
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