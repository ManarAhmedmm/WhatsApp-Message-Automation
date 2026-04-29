import pandas as pd
import pywhatkit as kit
import time


file_path = "numbers.xlsx"

message = """شكراً ويوم سعيد لحضرتك🌹"""

data = pd.read_excel(file_path)


# data.columns = data.columns.str.strip().str.lower()
data.columns = data.columns.astype(str).str.strip().str.lower()

print(data.columns) 

for i in range(len(data)):
    try:
        phone = str(data.iloc[i, 0])  
        
        print(f"Sending to +{phone} ...")
        
        kit.sendwhatmsg_instantly(f"+{phone}", message, wait_time=10, tab_close=True)
        
        time.sleep(15)
        
    except Exception as e:
        print(f"Error: {e}")

print("Done ✅")