# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

def connect():
    SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
    global SHEET

    global data
    global prices
    global discounts
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('favorite_jeans')

    sales = SHEET.worksheet('sales')
    pr=SHEET.worksheet('prices')
    ds=SHEET.worksheet('discount')



    data = sales.get_all_values()
    prices=pr.get_all_values()
    discounts=ds.get_all_values()
    print(data)
    print(discounts)
    print(prices)


def insert_row(data,worksheet):
    wsheet=SHEET.worksheet(worksheet)
    wsheet.append_row(data)
    print(f" New row inserted in {worksheet}!!")


def max_demand(data):
    maxMonth=''
    indexMax=0
    maxS=0
    for index,row in  enumerate(data):
        if index>0:
            s=0
            for jindex,col in enumerate(row):
                if jindex>0:
                    s=s+int(col)
            if s>maxS:
                maxS=s
                indexMax=index
    newRow=[]
    newRow.append(data[indexMax][0])
    for index,row in  enumerate(discounts):
        if index==indexMax:
            for jindex,col in enumerate(row):
                if jindex>0:
                    newRow.append(int(prices[1][jindex])*(1-float(col)))
    insert_row(newRow,'prices')
               








if  __name__=="__main__":
    connect()
    max_demand(data)