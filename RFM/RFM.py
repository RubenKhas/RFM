"""Main module."""

# %%
import pandas as pd
import numpy as np
import datetime as dt
import warnings
warnings.filterwarnings('ignore')

# %%
def RFMScore(df, InvoiceDate, InvoiceNo, MonetaryValue, CustomerID, Quantity = '', UnitPrice='' ):
    
    #convert date column to datetime format to be able to do calculations
    df[InvoiceDate] = pd.to_datetime(df[InvoiceDate])
    
    
    #if the monetary value is not provided in the beginning we can use Quantity and Unit Price Columns
    if MonetaryValue == "":
        df["MonetaryValue"] = df.Quantity * df.UnitPrice
    
    
    #define the maximum date to calculate the recency
    now = max(df[InvoiceDate])
    
    # grouping customers and calculating their recency drequency and monetary values
    rfm = df.groupby(CustomerID).agg({InvoiceDate : lambda day : (now - day.max()).days,
                               InvoiceNo: pd.Series.nunique,
                              MonetaryValue: lambda price : price.sum()})
    
    #renaming the column names of rfm dataframe
    col_list = ['Recency','Frequency','Monetary']
    rfm.columns = col_list
    
    
    #giving ranks based on csutomer rfm values
    rfm["R"] = pd.qcut(rfm["Recency"],5,labels=[5,4,3,2,1])
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method = "first"),5,labels=[1,2,3,4,5])
    rfm["M"] = pd.qcut(rfm["Monetary"],5,labels=[1,2,3,4,5])
    
    #concatinating the RFM ranks to get the final RFM Score of customers
    rfm["RFM_Score"] = rfm["R"].astype(str)  + rfm["M"].astype(str) + rfm["F"].astype(str)
    
    
    #segmenting customers based on their ranks
    seg_map = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'Risky',
    r'[1-2]5': 'Can\'t Loose',
    r'3[1-2]': 'About to Sleep',
    r'33': 'Need Attention',
    r'[3-4][4-5]': 'Loyal Customers',
    r'41': 'Promising',
    r'51': 'New Customers',
    r'[4-5][2-3]': 'Potential Loyalists',
    r'5[4-5]': 'Champions'
    }
    
    rfm['Segment'] = rfm['R'].astype(str) + rfm['F'].astype(str)
    rfm['Segment'] = rfm['Segment'].replace(seg_map, regex=True)
    

    return rfm



