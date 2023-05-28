from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.html import escape
from django.utils.safestring import mark_safe
import os
from glob import glob
import yfinance as yf
import joblib
import pandas as pd
from arch import arch_model
import pickle
from datetime import datetime
import json
from .model_load import GarchModel   


# Base Page for pretrained models
def index(request):
    stocks={'S&P 500':'^GSPC', 'Sensex':'^BSESN', 'Dow Jones':'^DJI', 'Nikkie 255':'^N225', 'NASDAQ':'^IXIC'}
    messages.success(request, 'Click on Retrain models to get latest predictions')
    if request.method == 'GET':
        dates=[i*5 for i in range(0,11)]
        prediction={}
        avg_price_list={}
        sorted_pred=[]

        for stockname,stock in stocks.items():
            # Get the Models
            model_shop = GarchModel(ticker=stock)
            model_shop.wrangle_data()
            model_shop.load()


            #Get Price history
            data=model_shop.data
            price=list(data.tail(50).values)
            # Find average of val for every 5 days
            avg_price=[]
            avg_price.append(round(price[0],3))
            for i in range(0,50,5):
                avg_price.append(round(sum(price[i:i+5])/5,3))
            avg_price_list[stockname]=avg_price

            # Predict here
            pred=model_shop.predict_volatility(horizon=5)
            pred_values=[]
            for value in pred.values():
                pred_values.append(round(value,3))
            
            sorted_pred.append([stockname]+pred_values)
            prediction[stockname] = pred_values

        days=[]
        for d in pred.keys():
            d=d[:d.index('T')]
            date_obj = datetime.strptime(d, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%b %d')
            days.append(formatted_date)
            
        
        sorted_pred = sorted(sorted_pred, key=lambda x: (sum(x[1:])/len(x[1:])))
        
        context = {
            'prediction': prediction,
            'days':days,
            'allstocks':False,
            'returns':avg_price_list,
            'days1':dates,
            'stocknames':sorted_pred
        }
        
        html_value =mark_safe('If you are looking for a long-term investment, <strong>'+sorted_pred[0][0]+'</strong> is a less volatile option. For more risky/day-trading opportunities, consider investing in <strong>'+sorted_pred[-1][0]+'</strong>.')
        #html_value = escape(html_value)
        messages.success(request, html_value)
        return render(request, 'prediction/index.html',context)
    
    
# Code to retrain the models
def train(request):
    # Get the Models
    stocks=['^GSPC', '^BSESN', '^DJI', '^N225', '^IXIC']

    for stock in stocks:
        model_shop = GarchModel(ticker=stock)
        # Wrangle the data
        model_shop.wrangle_data()

        # Fit GARCH(1,1) model to data
        model_shop.fit(p=1, q=1)

        # Check model parameters
        #print(model_shop.model.summary())

        # Dump the model
        str=model_shop.dump()
        print(str)
    messages.success(request, 'Models Re-trained Successfully')
    return redirect('prediction')


# Code to predict volatility for custom stocks
def allstocks(request):
    if (request.method == 'GET'):
        return render(request, 'prediction/allstocks.html')
    elif (request.method == 'POST'):
        stocks = request.POST['stocks'].strip().split(',')
        stock_dict={}
        prediction={}
        avg_price_list={}
        sorted_pred=[]
        dates=[i*5 for i in range(0,11)]
        for stock in stocks:
            stock=stock.strip()
            stockname=yf.Ticker(stock).info['shortName']
            stock_dict[stockname]=stock
            model_shop = GarchModel(ticker=stock)
            # Wrangle the data
            model_shop.wrangle_data()
            model_shop.fit(1,1)
            #Get Price history
            data=model_shop.data
            price=list(data.tail(50).values)
            # Find average of val for every 5 days
            avg_price=[]
            avg_price.append(round(price[0],3))
            for i in range(0,50,5):
                avg_price.append(round(sum(price[i:i+5])/5,3))
            avg_price_list[stockname]=avg_price

            # Predict here
            pred=model_shop.predict_volatility(horizon=5)
            pred_values=[]
            for value in pred.values():
                pred_values.append(round(value,3))
            
            sorted_pred.append([stockname]+pred_values)
            prediction[stockname] = pred_values

        days=[]
        for d in pred.keys():
            d=d[:d.index('T')]
            date_obj = datetime.strptime(d, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%b %d')
            days.append(formatted_date)
            
        
        sorted_pred = sorted(sorted_pred, key=lambda x: (sum(x[1:])/len(x[1:])))
        
        context = {
            'prediction': prediction,
            'days':days,
            'allstocks':True,
            'returns':avg_price_list,
            'days1':dates,
            'stocknames':sorted_pred
        }

        html_value =mark_safe('If you are looking for a long-term investment, <strong>'+sorted_pred[0][0]+'</strong> is a less volatile option. For more risky/day-trading opportunities, consider investing in <strong>'+sorted_pred[-1][0]+'</strong>.')
        #html_value = escape(html_value)
        messages.success(request, html_value)
        return render(request, 'prediction/index.html',context)




    
