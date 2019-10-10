from django.shortcuts import render, redirect
from . models import Stock
from . forms import StockForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction

@login_required
def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker_symbol']
        api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
        try:
            api = json.loads(api_requests.content)
        except Exception as e:
            api = "Error.. Make sure you have entered a correct ticker"
        return render(request, 'homepage.html', {'api': api})
    else:
        ticker = Stock.objects.filter(user=request.user)
        output = []

        for ticker_item in ticker:

            api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
            try:
                api = json.loads(api_requests.content)
                output.append(api)
            except Exception as e:
                api = "Error.. Make sure you have entered a correct ticker"
        return render(request, 'homepage.html', {'ticker':ticker, 'output':output})
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

    if request.method == 'POST':
        stock_form = StockForm(request.POST or None)

        if stock_form.is_valid():
            ticker = request.POST['ticker']
            api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
            try:
                api = json.loads(api_requests.content)
            except Exception as e:
                messages.success(request, ("Invalid entry!! Please check the ticker symbol"))
                return redirect('add_stock')
            try:  
                current_user = request.user 
                stock = stock_form.save(commit=False)
                stock.user = current_user
                stock.save()
            except Exception as e:
                messages.success(request, ("Please enter a unique ticker"))
                return redirect('add_stock')
            messages.success(request, ("Stock has been added sucessfully, if not please check the input"))
            return redirect('add_stock')
        else:
            return redirect('add_stock')
    else:
        print("finished ticker")
        ticker = Stock.objects.filter(user=request.user)
        output = []
        if ticker:
            for ticker_item in ticker:

                api_requests = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_10c8988d72794440b4f9bba3e0cde284")
                try:
                    api = json.loads(api_requests.content)
                    output.append(api)
                except Exception as e:
                    api = "Error.. Make sure you have entered a correct ticker"
                
            return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})
        else:
            return render(request, 'add_stock.html', {'ticker':ticker})
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
    main_url = " https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=4dbc17e007ab436fb66416009dfb59a8"
    open_bbc_page = requests.get(main_url).json() 
    newsdata=[]
    linkdata=[]
    for i in range(20):
        article = {
                    'a': open_bbc_page["articles"][i]['title'],
                    'url': open_bbc_page['articles'][i]['url'],
                    'image': open_bbc_page['articles'][i]['urlToImage']
                    }
        newsdata.append(article)
    context={'newsdata': newsdata} 
    return render(request, 'news.html', context)