from django.shortcuts import render
from logicfiles.nsedata import *
from django.http import JsonResponse

# Create your views here.

#loads the homepage html
def homepage(request):
    return render(request, 'homepage.html')

#api to return details of index
def indexdisplay(request):
    if request.method == 'GET':
        index = request.GET.get('index')
        if index:
            currnifty = currniftystatus(index)
            return JsonResponse(currnifty, status = 200)
        else:
            return JsonResponse({'error': 'Stock parameter missing'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
#api to return the details of all stocks listed in 'home/static/home/nse_symbols_nifty50.txt'
def allstockdisplay(request):
    with open('home/static/home/nse_symbols_nifty50.txt', 'r') as file:
        data = {}
        symbols = [line.strip() for line in file.readlines()]
        for symbol in symbols:
            ret = stockdata(symbol)
            if ret:
                data[symbol] = ret
    # print(data)
    return JsonResponse(data, status = 200)

#loads the page for each stock
def stockdisplay(request, symbol):
    context = {'symbol':symbol}
    return render(request, 'stockpage.html', context)

#api to return details of each stock
def stockreturn(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
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


