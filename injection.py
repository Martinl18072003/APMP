"""
File: injection.py
Author: Martin Lemaire
Date created: November 7, 2023
Description: Optimizes injection price.

Modifications:
- [v1.0.0 - 07.11.23 - INITIAL]
"""

# IMPORTS
import subprocess, shutil, ccxt, csv, time, sys, os

# FUNCTION
def min_increment(number):
    """
    Calculates the minimum increment that can be applied to a float number.

    Arguments:
    number (float): The input float number to determine the minimum increment for.

    Returns:
    float: The minimum increment that can be applied to the input number.
    """
    number = str(number)
    tmp = ""
    count = 0
    start_count = False
    for i in range(len(number)):
        tmp = number[i]
        if start_count == True: count += 1
        if tmp==".": start_count = True
    return count

# MAIN
if __name__ == "__main__":

    # ACCOUNT ACCESS
    shutil.copy("/Volumes/APMP/apmp.txt.encrypted", os.path.abspath(os.getcwd()))
    subprocess.run("python3 api_encryption.py apmp.txt 0", shell=True, check=True, text=True)
    subprocess.run("rm apmp.txt.encrypted", shell=True, check=True, text=True)

    with open("apmp.txt", 'r') as file:
        key = file.readline().strip()
        secret = file.readline().strip()

    subprocess.run("rm apmp.txt", shell=True, check=True, text=True)
    account = ccxt.binance({
        'enableRateLimit': True,
        'apiKey': key,
        'secret':secret
    })

    # Reading symbol
    try:
        with open(str(os.path.abspath(os.getcwd())+'/data.csv'), mode='r') as file:
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

    # Define trigger and profit entry
    profit_entry = 0
    value = account.fetchTicker(symbol)
    trigger = value['close']

    # Find the increment
    ohlcv = account.fetch_ohlcv(symbol, '1d', limit=1000)
    tmp = []
    decimals=0
    for i in range(len(ohlcv)):
        tmp.append(10**(-1*min_increment(ohlcv[i][1])))
        if min_increment(ohlcv[i][1])>decimals: decimals = min_increment(ohlcv[i][1])
    increment = format(min(tmp),'.'+str(decimals)+'f')

    # Fetch the quantity to inject
    balance = account.fetch_balance()
    quantity = balance['total']['USDT']

    # Reading injection data
    try:
        with open(str(os.path.abspath(os.getcwd())+'/injection_data.csv'), mode='r') as file:
            reader = csv.reader(file)
            row = next(reader)
            data_csv = [float(value) for value in row]
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

    # Start back at past data if crash
    if data_csv[0] != 0:
        trigger = data_csv[0]

    security_claw = trigger*1.01

    # Variable for the optional display of live data
    life_indicator = 0

    while True:

        value = account.fetchTicker(symbol)
        value = value['close']

        if value <= trigger and profit_entry == 0:
            profit_entry = 1
            
        # Security Claw
        while profit_entry == 1 and value <= (trigger-increment):
            trigger -= increment
            security_claw -= increment

        if profit_entry == 1 and value >= security_claw:
            quantity = int(quantity/value)-1
            account.create_market_buy_order(symbol, quantity)
            print("DONE")
            time.sleep(1000000)
            data = [-1]
            try:
                with open(str(os.path.abspath(os.getcwd())+'/injection_data.csv'), mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)
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
            break

        data = [trigger]

        try:
            with open(str(os.path.abspath(os.getcwd())+'/injection_data.csv'), mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
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

        # Optional display of live data
        if len(sys.argv) > 1:
            if life_indicator==0:
                print(f"  -|-  INJECTION  -  VALUE: {value}  -  TRIGGER: {trigger}  -  SECURITY CLAW: {int(1000*security_claw)/1000}  -  QUANTITY ESTIMATION: {int(quantity/value)-1}  -  QUANTITY: {int(quantity)}  --")
                life_indicator=1
            else:
                print(f"  - -  INJECTION  -  VALUE: {value}  -  TRIGGER: {trigger}  -  SECURITY CLAW: {int(1000*security_claw)/1000}  -  QUANTITY ESTIMATION: {int(quantity/value)-1}  -  QUANTITY: {int(quantity)}  --")
                life_indicator=0
        else: pass