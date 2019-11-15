from django.shortcuts import render, redirect
from . models import Stock,TickerModel
from . forms import StockForm, Editprofile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.core import serializers
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
                
@login_required
def home(request):
    import requests
    import json
    if request.method == 'POST':
        ticker = request.POST['ticker_symbol_hidden']
        api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" +
                                    ticker + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
        try:
            api = json.loads(api_requests.content)
        except Exception as e:
            api = "Error.. Make sure you have entered a correct ticker"
        return render(request, 'homepage.html', {'api': api})
    else:
        ticker = Stock.objects.filter(user=request.user)
        output = []
        for ticker_item in ticker:
            api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(
                ticker_item) + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
            try:
                api = json.loads(api_requests.content)
                output.append(api)
            except Exception as e:
                api = "Error.. Make sure you have entered a correct ticker"
        return render(request, 'homepage.html', {'ticker': ticker, 'output': output})

@login_required
def about(request):
    return render(request, 'about.html', {})

@login_required
def profile(request):
    return render(request, 'profile.html', {})

@login_required
def add_stock(request):
    import requests
    import json
    import operator
    import collections
    #Similar suggestion
    all_stocks =  Stock.objects.select_related('user').all()
    print("all Stocks", all_stocks)
    not_current_user = []
    current_user_stocks = all_stocks.filter(user=request.user)
    current_user_ticker_list = []
    for stock in current_user_stocks:
        current_user_ticker_list.append(stock.ticker)    
    ticker_all = all_stocks.exclude(user=request.user)
    for stock in ticker_all:   
        not_current_user.append(stock.user) 
    users_name = set(not_current_user)
    # print(user_name)
    ticker_users = []
    #fetch all users as queryset
    for users in users_name:
        ticker_users.append(all_stocks.select_related('user').filter(user=users))
    sugesstion_ticker = []   
    print (ticker_users) 
    for users in ticker_users :
        print("users", users)
        for individual_user in users: 
            print ("individual user", individual_user) 
            if  individual_user.ticker in current_user_ticker_list:
                sugesstion_ticker.append(all_stocks.filter(user=individual_user.user))
    all_suggestions = []
    for stock in sugesstion_ticker:
        for suggestion in stock:
            all_suggestions.append(suggestion.ticker)
    # print(all_suggestions)
    dictionary = {}
    for stock in all_suggestions:
        dictionary.update({stock : all_suggestions.count(stock)})
    # print(dictionary)
    # print(current_ticker_list)    
    for stock in current_user_ticker_list:
        try:
            del dictionary[stock]
        except Exception as e:
            print("item not found")
    suggestion_ticker = {}
    for key, value in dictionary.items():
        company_name = requests.get("https://cloud.iexapis.com/stable/stock/" +
                                        key + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
        try:
            api = json.loads(company_name.content)
        except Exception as e:
            print("error loading company details")
        print(api['companyName'])
        suggestion_ticker.update({api['companyName'] : value})
    sorted_dict = sorted(suggestion_ticker.items(), key=operator.itemgetter(1), reverse=True)
    dictionary = collections.OrderedDict(sorted_dict)

    #add stock to favorites   
    if request.method == 'POST':
        stock_form = StockForm(request.POST or None)
        if stock_form.is_valid():
            ticker = request.POST['ticker']
            api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" +
                                        ticker + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
            try:
                api = json.loads(api_requests.content)
            except Exception as e:
                messages.success(
                    request, ("Invalid entry!! Please check the ticker symbol"))
                return redirect('add_stock')
            try:
                current_user = request.user
                stock = stock_form.save(commit=False)
                stock.user = current_user
                stock.save()
            except Exception as e:
                messages.success(request, ("Please enter a unique ticker"))
                return redirect('add_stock')
            messages.success(
                request, ("Stock has been added sucessfully, if not please check the input"))
            return redirect('add_stock')
        else:
            return redirect('add_stock')
    else:
        print("finished ticker")
        ticker = Stock.objects.select_related('user').filter(user=request.user)
        output = []
        if ticker:
            for ticker_item in ticker:
                api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(
                    ticker_item) + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
                try:
                    api = json.loads(api_requests.content)
                    output.append(api)
                except Exception as e:
                    api = "Error.. Make sure you have entered a correct ticker"
            return render(request, 'add_stock.html', {'ticker': ticker, 'output': output, 'dict': dictionary})
        else:
            return render(request, 'add_stock.html', {'ticker': ticker, 'dict': dictionary})

@login_required
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect(delete_stock)

@login_required
def delete_stock(request):
    ticker = Stock.objects.filter(user=request.user)
    return render(request, 'delete_stock.html', {'ticker': ticker})

@login_required
def news(request):
    import requests
    import json
    main_url = " https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=3d414a52d86c431bbd60cdc6cee48fff"
    open_bbc_page = requests.get(main_url).json()
    newsdata = []
    linkdata = []
    for i in range(20):
        article = {
            'a': open_bbc_page["articles"][i]['title'],
            'url': open_bbc_page['articles'][i]['url'],
            'image': open_bbc_page['articles'][i]['urlToImage'],
            'details': open_bbc_page['articles'][i]['description'],
        }
        newsdata.append(article)
    paginator = Paginator(newsdata, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        newsdata = paginator.page(page)
    except(EmptyPage, InvalidPage):
        newsdata = paginator.page(paginator.num_pages)
    context = {'newsdata': newsdata}
    return render(request, 'news.html', context)

@login_required
def edit(request):
    if request.method == 'POST':
        form = Editprofile(request.POST, instance=request.user)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.email = request.user.email
            form_instance.save()
            print("valid")
            return redirect('profile')
    else:
        form = Editprofile(instance=request.user)
    return render(request, 'edit.html', {'form': form})

@login_required
def graph(request, ticker):
    import requests
    import pandas as pd
    import math
    import datetime
    from bokeh.plotting import figure, save, output_file
    #Code to obtain trade data for AAPL
    API_KEY = 'V81XUIFVLP1JZ9KB'
    stock_name = ticker
    json_stock_price = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_name + '&apikey=' + API_KEY)
    result = json_stock_price.json()
    dataForAllDays = result['Time Series (Daily)']
    #convert to dataframe
    dataForAllDays_df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 
    dataForAllDays_df = dataForAllDays_df.reset_index()
    #rename columns
    dataForAllDays_df = dataForAllDays_df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})
    #Changing to datetime
    dataForAllDays_df['date'] = pd.to_datetime(dataForAllDays_df['date'])
    #Sort according to date
    dataForAllDays_df = dataForAllDays_df.sort_values(by=['date'])
    #Changing the datatype 
    dataForAllDays_df.open = dataForAllDays_df.open.astype(float)
    dataForAllDays_df.close = dataForAllDays_df.close.astype(float)
    dataForAllDays_df.high = dataForAllDays_df.high.astype(float)
    dataForAllDays_df.low = dataForAllDays_df.low.astype(float)
    dataForAllDays_df.volume = dataForAllDays_df.volume.astype(int)
    #check the data
    dataForAllDays_df.head()
    #Check the datatype
    dataForAllDays_df.info()
    gain = dataForAllDays_df.close > dataForAllDays_df.open
    loss = dataForAllDays_df.open > dataForAllDays_df.close
    half_day_in_ms = 12*60*60*1000 # half day in ms
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    title = stock_name + ' Chart'
    graph_plot = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = title, x_axis_label= "Date", y_axis_label= "Stock Price")
    graph_plot.xaxis.major_label_orientation = math.pi/4
    graph_plot.grid.grid_line_alpha=0.3
    graph_plot.segment(dataForAllDays_df.date, dataForAllDays_df.high, dataForAllDays_df.date, dataForAllDays_df.low, color="black")
    graph_plot.vbar(dataForAllDays_df.date[gain], half_day_in_ms, dataForAllDays_df.open[gain], dataForAllDays_df.close[gain], fill_color="#D5E1DD", line_color="black")
    graph_plot.vbar(dataForAllDays_df.date[loss], half_day_in_ms, dataForAllDays_df.open[loss], dataForAllDays_df.close[loss], fill_color="#F2583E", line_color="black")
    #Store as a HTML file
    output_file("quotes/templates/stock_information.html", title="candlestick.py example")
    save(graph_plot)
    # return render(request, 'stock_information.html', {})
    return render(request, 'graph_view.html', {})

class TickerAutocomplete(View):
    def get(self,request):
        tickers = TickerModel.objects.all()
        search_entry = request.GET.get('search_entry','')
        # print("-- ",request.GET)
        try:
            if search_entry[0]!='':
                search_result = tickers.filter(company_name__icontains=search_entry)
                if len(search_result)>20:
                    search_result = search_result[0:20]
            # print(tickers)
            return JsonResponse(serializers.serialize('json',search_result),safe=False)
        except IndexError:
            return JsonResponse({})