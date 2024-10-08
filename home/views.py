from django.shortcuts import render, redirect
from logicfiles.nsedata import *
from django.http import JsonResponse
import json,html
from urllib.parse import unquote
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

#loads the homepage html
@login_required(login_url='/login/')
def homepage(request):
    return render(request, 'homepage.html')

def login_page(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(username=email)
        if not user.exists():
            messages.info(request,'Email doesn\'t exist, Please register to proceed.')
            return redirect('/register/')
        else:
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request,'Wrong Username/Password')
                return redirect('/login/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')

def register_page(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(username=email)
        if user.exists():
            messages.info(request,'Email already in use')
            return redirect('/register/')

        user = User.objects.create(
            username = email
        )
        user.set_password(password)
        user.save()
        return redirect('/login/')

    return render(request,'register.html')

#api to return details of index
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
def stockdisplay(request, symbol):
    context = {'symbol':symbol}
    return render(request, 'stockpage.html', context)

#api to return details of each stock
@login_required(login_url='/login/')
def stockreturn(request):
    if request.method == 'GET':
        symbol = html.unescape(unquote(request.GET.get('symbol')))
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

@login_required(login_url='/login/')
def getstocknames(request):
    ret = {}
    with open('home/static/home/nse_symbols_nifty50.txt', 'r') as file:
        symbols = [line.strip() for line in file.readlines()]
        ret = getstockname(symbols)
    return ret