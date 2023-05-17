from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from glob import glob
import yfinance as yf
import pandas as pd
from datetime import datetime


def wrangle_data(ticker):
    # Get table from database
    df = yf.download(ticker,period = "2y")
    
    # Sort DataFrame ascending by date
    df.sort_index(ascending=True, inplace=True)

    # Create "return" column
    df['return'] = df['Close'].pct_change()*100

    # Return returns
    return df



# Create your views here.

# Initial Page for selecting stocks tickers
def index(request):
    if (request.method == 'GET'):
        return render(request, 'stockprice/index.html')
    
    elif(request.method == 'POST'):
        date_range=250
        #dates=[i for i in range(250)]
        avg_price_list={}
        stocks = request.POST['stocks'].split(',')
        stock_dict={}
        for stock in stocks:
            stock_name=yf.Ticker(stock).info['shortName']
            stock_dict[stock_name]=stock

        returns={}
        for stockname,stock in stock_dict.items():
           
            # Wrangle the data
            df=wrangle_data(stock)
            close_price=df['Close'].dropna()
            price=list(close_price.tail(date_range).values)
            ret=list(df['return'].tail(date_range).values)
            dates=list(df.tail(date_range).index)
            dates=[i.strftime("%d-%m-%Y") for i in dates]
             # get every 5th day from dates
            dates=dates[::5]
            # Find average of val for every 5 days
            avg_price=[]
            avg_price.append(round(price[0],3))
            avg_ret=[]
            avg_ret.append(round(ret[0],3))
            for i in range(0,date_range,5):
                avg_price.append(round(sum(price[i:i+5])/5,3))
                avg_ret.append(round(sum(ret[i:i+5])/5,3))

            avg_price_list[stockname]=avg_price
            returns[stockname]=avg_ret
            

        context = {
            'allstocks':False,
            'returns':returns,
            'price':avg_price_list,
            'days1':dates
        }
        return render(request, 'stockprice/values.html',context)
    
#Dashboard for stock price
def values(request):
    
    return render(request, 'stockprice/values.html')

    