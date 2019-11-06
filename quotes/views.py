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


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user.is_active:    
        # Redirecting to the required login according to user status.
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('/admin/')  # or your url name
            else:
                login(request, user)
                return redirect('/') 
                
@login_required
def home(request):
    import requests
    import json
    if request.method == 'POST':
        # losers_response = request.get("https://cloud.iexapis.com/stable/stock/market/list/losers/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
        # losers = json.loads(losers_response.content)
        # gainers_response = request.get("https://cloud.iexapis.com/stable/stock/market/list/gainers/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
        # gainers = json.loads(gainers_response.content)
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

    not_current_user = []
    ticker = Stock.objects.filter(user=request.user)
    current_ticker_list = []
    for tic in ticker:
        current_ticker_list.append(tic.ticker)
    ticker_all = Stock.objects.all()
    for i in ticker_all:
        if (i in ticker):
            print ("")
        else :
            # print (i.user)
            not_current_user.append(i.user)
    
    user_name = set(not_current_user)
    print (user_name)
    ticker_users = []
    for p in user_name :
        ticker_users.append(Stock.objects.filter(user=p))
    sugesstion_ticker = []
    
    for r in ticker_users:
        for u in r:
            for l in ticker:
                
                if l.ticker == u.ticker:
                    sugesstion_ticker.append(Stock.objects.filter(user=u.user))
    all_suggestions = []
    for j in sugesstion_ticker:
        for i in j:
            all_suggestions.append(i.ticker)
    # print(all_suggestions)
    dictionary = {}
    for tickers in all_suggestions:
        dictionary.update({tickers : all_suggestions.count(tickers)})
    # print(dictionary)
    print(current_ticker_list)
    
    for item in current_ticker_list:
        try:
            del dictionary[item]
        except Exception as e:
            print("item not found")

    suggestion_ticker = {}
    # print(dictionary)
    for key, value in dictionary.items():
        print(key)
        company_name = requests.get("https://cloud.iexapis.com/stable/stock/" +
                                        key + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
        try:
            api = json.loads(company_name.content)
        except Exception as e:
            print("error")
        print(api['companyName'])
        suggestion_ticker.update({api['companyName'] : value})
    #     dictionary[api['companyName']] = dictionary.pop(key)
    sorted_dict = sorted(suggestion_ticker.items(), key=operator.itemgetter(1), reverse=True)
    dictionary = collections.OrderedDict(sorted_dict)
    print("Company name:",suggestion_ticker)
        

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
        ticker = Stock.objects.filter(user=request.user)
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
            form.save()
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
    API_KEY = ' V81XUIFVLP1JZ9KB'
    stock_name = ticker
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_name + '&apikey=' + API_KEY)
    print(r.status_code)
    result = r.json()
    dataForAllDays = result['Time Series (Daily)']
    #convert to dataframe
    df = pd.DataFrame.from_dict(dataForAllDays, orient='index') 
    df = df.reset_index()
    #rename columns
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low", "4. close": "close","5. volume":"volume"})
    #Changing to datetime
    df['date'] = pd.to_datetime(df['date'])
    #Sort according to date
    df = df.sort_values(by=['date'])
    #Changing the datatype 
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.volume = df.volume.astype(int)
    #check the data
    df.head()
    #Check the datatype
    df.info()
    inc = df.close > df.open
    dec = df.open > df.close
    w = 12*60*60*1000 # half day in ms
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    title = stock_name + ' Chart'
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = title, x_axis_label= "Date", y_axis_label= "Stock Price")
    p.xaxis.major_label_orientation = math.pi/4
    p.grid.grid_line_alpha=0.3
    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")
    #Store as a HTML file
    output_file("quotes/templates/stock_information.html", title="candlestick.py example")
    save(p)
    # return render(request, 'stock_information.html', {})
    return render(request, 'graph_view.html', {})

class TickerAutocomplete(View):
    def get(self,request):
        qs = TickerModel.objects.all()
        q = request.GET.get('q','')
        print("-- ",request.GET)
        try:
            if q[0]!='':
                qs = qs.filter(company_name__icontains=q)
                if len(qs)>20:
                    qs = qs[0:20]
            # print(qs)
            return JsonResponse(serializers.serialize('json',qs),safe=False)
        except IndexError:
            return JsonResponse({})
def test(request):
    not_current_user = []
    ticker = Stock.objects.filter(user=request.user)
    current_ticker_list = []
    for tic in ticker:
        current_ticker_list.append(tic.ticker)
    print("current users tickers b4 cleaning", current_ticker_list)
    ticker_all = Stock.objects.all()
    for i in ticker_all:
        if (i in ticker):
            print ("")
        else :
            # print (i.user)
            not_current_user.append(i.user)
    user_name = set(not_current_user)
    print ("All users except current",user_name)
    ticker_users = []
    for p in user_name :
        ticker_users.append(Stock.objects.filter(user=p))
    sugesstion_ticker = []   
    for r in ticker_users:
        for u in r:
            for l in ticker:
                
                if l.ticker == u.ticker:
                    sugesstion_ticker.append(Stock.objects.filter(user=u.user))
    all_suggestions = []
    for j in sugesstion_ticker:
        for i in j:
            all_suggestions.append(i.ticker)
    print("all suggestions",all_suggestions)
    dictionary = {}
    for tickers in all_suggestions:
        dictionary.update({tickers : all_suggestions.count(tickers)})
    print("all tickers and their count",dictionary)
    # del dictionary('FB')
    print("dict after del", dictionary)
    print (current_ticker_list)
    try:
        for item in current_ticker_list:
            print (item)
            print("ticker to be deleted", item)
            dictionary.pop[item]
    except Exception as e:
        print("item not found")
    print("tickers after cleaning", dictionary)
    print("value of FB",dictionary['FB'])

    sorted(dictionary.items(), key=lambda x:x[1])
    print(dictionary)
    if not dictionary:
        print("Dictionary in if")
    else:
        print("else")
    return render(request , 'test.html', {'dict': dictionary})       