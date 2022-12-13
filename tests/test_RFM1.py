import pandas as pd
from RFM import RFM as RFM


dt = pd.read_csv("BonusCustomersales_New.csv")

RFM.RFMScore(dt, "Day Bought",InvoiceNo = "Unnamed: 0", MonetaryValue= "Totalcost", CustomerID = "Customer Name")