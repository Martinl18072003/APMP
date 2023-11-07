import ccxt, csv, time, sys

# ACCOUNT ACCESS
account = ccxt.binance()#TODO FILL

"""
OPERATIONAL PROCEDURE:
 LAUNCH VIA THE PROTECTION LAYER ONLY, NEVER THIS SCRIPT ALONE
"""

symbol = "LDO/USDT" #TODO Make it read data.csv
profit_entry = 0
value = account.fetchTicker(symbol)
trigger = value['close']
increment = 0.001
balance = account.fetch_balance()
quantity = balance['total']['USDT']
CSV_path = '/Users/martin/Library/CloudStorage/OneDrive-Personal/MJL_Sol/Research/Main_Trading_Program/MARK_III/injection_data.csv'

with open(CSV_path, mode='r') as file:
    reader = csv.reader(file)
    row = next(reader)
    data_csv = [float(value) for value in row]

if data_csv[0] != 0:
    trigger = data_csv[0]

security_claw = trigger/0.95*0.96
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
        with open(CSV_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        break

    data = [trigger]
    with open(CSV_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    if life_indicator==0:
        print(f"  -|-  INJECTION  -  VALUE: {value}  -  TRIGGER: {trigger}  -  SECURITY CLAW: {int(1000*security_claw)/1000}  -  QUANTITY ESTIMATION: {int(quantity/value)-1}  -  QUANTITY: {int(quantity)}  --")
        life_indicator=1
    else:
        print(f"  - -  INJECTION  -  VALUE: {value}  -  TRIGGER: {trigger}  -  SECURITY CLAW: {int(1000*security_claw)/1000}  -  QUANTITY ESTIMATION: {int(quantity/value)-1}  -  QUANTITY: {int(quantity)}  --")
        life_indicator=0