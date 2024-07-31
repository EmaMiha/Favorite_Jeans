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
  

def insert_row(dataI,worksheet):

    wsheet1=SHEET.worksheet(worksheet)
    pp=wsheet1.get_all_values()
    for i,row in enumerate(pp):
        if i>0:
            if (pp[i][0]==dataI[0]):
                print(i)
                wsheet1.delete_rows(i+1)
                break
    wsheet1.append_row(dataI)
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
                    newRow.append(float(prices[1][jindex])*(1-float(col)))
    insert_row(newRow,'prices')
               
def smallest_sales(product,percentage,data):
    for i,brand in enumerate(data[0]):
        if brand==product:
            indexProduct=i
    minValue=999999
    for i,row in enumerate(data):
        if(i>0):
            if int(row[indexProduct])<minValue:
                minValue=int(row[indexProduct])
                rowMin=i
    return [data[rowMin][0],minValue]
                


def descendingOrder(data):
    sumCol=[]
    brands=[]
    a=0
    for  k in range(len(data)-1):
        sumCol.append(a)
    
    for l,n in enumerate(data[0]):
        brands.append(n)
    
    for i,br in enumerate(data):
        if i>0:
            for j,val in enumerate(br):
                if j>0:
                    
                    l=sumCol[j]+int(data[i][j])
                    sumCol[j]=l

    dictionary=dict()

    for i,brand in enumerate(brands):
        if (i>0):
            dictionary[brand]=sumCol[i]


    output = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
    print(output)


def ascendingOrder(data):
    sumCol=[]
    brands=[]
    a=0
    for  k in range(len(data)-1):
        sumCol.append(a)
    
    for l,n in enumerate(data[0]):
        brands.append(n)
    
    for i,br in enumerate(data):
        if i>0:
            for j,val in enumerate(br):
                if j>0:
                    
                    l=sumCol[j]+int(data[i][j])
                    sumCol[j]=l

    dictionary=dict()

    for i,brand in enumerate(brands):
        if (i>0):
            dictionary[brand]=sumCol[i]


    output = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    print(output)



def averagePricePerBrand(brand):
    index=0 
    for l,name in enumerate(data[0]):
        if name==brand:
            index=l
            break
    sumP=0
    for l,n in enumerate(data):
        if l>0:
            sumP=sumP+float(data[l][index])*(float(prices[1][index])*(1-float(discounts[l][index])))
    averageP=sumP/(len(data)-1)
    print(averageP)










if  __name__=="__main__":
    connect()
    # max_demand(data)
    # smSale=smallest_sales("Levi's",0.1,data)
    #ascendingOrder(data)
    averagePricePerBrand("Replay")
