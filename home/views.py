from django.shortcuts import render
from logicfiles.nsedata import *
from django.http import JsonResponse
import json,html
from urllib.parse import unquote

# Create your views here.

#loads the homepage html
def homepage(request):
    return render(request, 'homepage.html')

#api to return details of index
def indexdisplay(request):
    if request.method == 'GET':
        index = html.unescape(unquote(request.GET.get('index')))
        if index:
            currnifty = currniftystatus(index)
            return JsonResponse(currnifty, status = 200)
        else:
            return JsonResponse({'error': 'Stock parameter missing'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
#api to return the details of all stocks listed in 'home/static/home/nse_symbols_nifty50.txt'
def allstockdisplay(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            body = json.loads(request.body)
            stock_symbols = body.get('symbols', [])
            stock_data = {}
            for symbol in stock_symbols:
                ret = stockdata(symbol)
                if ret:
                    stock_data[symbol] = ret
            return JsonResponse(stock_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

#loads the page for each stock
def stockdisplay(request, symbol):
    context = {'symbol':symbol}
    return render(request, 'stockpage.html', context)

#api to return details of each stock
def stockreturn(request):
    if request.method == 'GET':
        symbol = html.unescape(unquote(request.GET.get('symbol')))
        print(symbol)
        if symbol:
            ret = stockdata(symbol)
            if ret:
                return JsonResponse(ret, status = 200)
            else:
                return JsonResponse({'error': f'Stock not found, please check the symbol({symbol})'}, status=404)
        else:
            return JsonResponse({'error': 'Symbol parameter missing'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def getstocknames(request):
    ret = {}
    with open('home/static/home/nse_symbols_nifty50.txt', 'r') as file:
        symbols = [line.strip() for line in file.readlines()]
        ret = getstockname(symbols)
    return ret