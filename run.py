# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import sys

seasons = {
        "Spring": ["March", "April", "May"],
        "Summer": ["June", "July", "August"],
        "Autumn": ["September", "October", "November"],
        "Winter": ["December", "January", "February"]
    }

def connect():
    SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
    global SHEET
    global time
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
    time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")



    data = sales.get_all_values()
    prices=pr.get_all_values()
    discounts=ds.get_all_values()

def insert_average(price,brand):
    wsheet1=SHEET.worksheet('average_price')
    newRow=[]
    newRow.append('Brand')
    newRow.append('Avg')
    wsheet1.append_row(newRow)
    newRow=[]
    newRow.append(brand)
    newRow.append(price)
    wsheet1.append_row(newRow)

def insert_SeasonRes(sumN,season):
 
    wsheet1=SHEET.worksheet('season')
    wsheet1.clear()
    newRow=[]
    if season not in seasons:
        raise ValueError("Invalid season name!!")
    newRow.append('season')
    newRow.append('sum')
    wsheet1.append_row(newRow)
    newRow=[]
    newRow.append(season)
    newRow.append(sumN)
    wsheet1.append_row(newRow)






def insert_minsales_row(brand,data):
    wsheet1=SHEET.worksheet('minsales')
    newRow=[]
    minValue=999999
    for i,brand in enumerate(data[0]):
        if brand.lower()==product:
            indexProduct=i
    if indexProduct==-1:
        raise ValueError("Invalid brand name!!")
    newRow.append(brand)
    text=''
    for index,month in enumerate(data[0]):
        text=text+month
        if index<len(data[0])-1:
            text=text+","
    newRow.append(data[1])
    newRow.append(text)
    newRow.append(time)
    wsheet1.append_row(newRow)

def insertMaxSaleRevenue(maxS):
    wsheet1=SHEET.worksheet('revenue_month')
    wsheet1.clear()
    newRow=[]
    if maxS[1]<=0:
        raise ValueError("No revenue!!")
    newRow.append('month')
    newRow.append('SUM')
    wsheet1.append_row(newRow)
    newRow=[]
    newRow.append(maxS[0])
    newRow.append(maxS[1])
    wsheet1.append_row(newRow)


def insert_order(data):
    wsheet1=SHEET.worksheet('ascending_order')
    newRow=[]
    newRow.append('Brand')
    newRow.append('Sum')
    wsheet1.append_row(newRow)
    for key,value in data.items():
        newRow=[]
        newRow.append(key)
        newRow.append(value)
        wsheet1.append_row(newRow)



def insert_price_row(dataI,worksheet):

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
    insert_price_row(newRow,'prices')
               
def min_sales(product,data):
    
    product=product.lower()
    indexProduct=-1
    for i,brand in enumerate(data[0]):
        if brand.lower()==product:
                indexProduct=i
    minValue=999999
    if indexProduct==-1:
        raise ValueError("Invalid brand name!!")
    for i,row in enumerate(data):
        if(i>0):
            if int(row[indexProduct])<minValue:
                minValue=int(row[indexProduct])
                rowMin=i
    result=[]           
    for i,row in enumerate(data):
        if(i>0):
            if int(row[indexProduct])==minValue:
                result.append(row[0])
    return [result,minValue]
    


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


    return dict(sorted(dictionary.items(), key=lambda item: item[1]))
    



def averagePricePerBrand(brand):
    for i,brand in enumerate(data[0]):
        if brand.lower()==product:
                indexProduct=i
    if indexProduct==-1:
        raise ValueError("Invalid brand name!!")
    index=0 
    for l,name in enumerate(data[0]):
        if name==brand:
            index=l
            break
        
    sumP=0
    for l,n in enumerate(data):
        if l>0:
            sumP=sumP+float(data[l][index])*(float(prices[1][index])*(1-float(discounts[l][index])))
    return sumP/(len(data)-1)
    



def sumSeason(season):

    sumS=0
    for l,month in enumerate(data):
        if l>0 and month[0] in seasons[season]:
            for j,d in enumerate(month):
                if j>0:
                    sumS=sumS+int(d)
    return sumS    
    

        
def monthly_sales_revenue(avg_sales,full_prices,discounts):

    mr={}
    for i in range(1,len(avg_sales)):
        month=avg_sales[i][0]
        s=0
        for j in range(1,len(avg_sales[0])):
            montly_sales=float(avg_sales[i][j])
            discount=float(discounts[i][j])
            fullprice_with_discount=float(full_prices[1][j])*(1-discount)
            s=s+montly_sales*fullprice_with_discount
        mr[month]=round(s,2)
    return mr    

def  maxSaleMonth(m):
    highest_month=max(m,key=monthly_sales_r.get)
    highest_revenue=m[highest_month]
    return highest_month,highest_revenue




if  __name__=="__main__":
    connect()
    max_demand(data)
    while True:
        try:
            brand=input("Enter brand for statistics")
            smSale=min_sales(brand,data)
            insert_minsales_row(brand,smSale)
            insert_order(ascendingOrder(data))
            insert_average(averagePricePerBrand(brand),brand)
            season=input("Enter season for summarize:")
            insert_SeasonRes(sumSeason(season),season)
            monthly_sales_r=monthly_sales_revenue(data,prices,discounts)
            maxS=maxSaleMonth(monthly_sales_r)
            insertMaxSaleRevenue(maxS)
            break
        except ValueError as e:
            print(f"Error: {e} Please Try again!!!")
   
